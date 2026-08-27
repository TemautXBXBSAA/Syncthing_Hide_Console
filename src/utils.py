import sys
import subprocess
import ctypes
from ctypes import wintypes
import win32gui
import win32con

from .log import Logger

user32 = ctypes.windll.user32
kernel32 =  ctypes.windll.kernel32
logger = Logger("utils","log.log")
def hide_window(hwnd) -> bool:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        logger.info(f"Successfully hidden window with hwnd: {hwnd}")
        return True
    except Exception as e:
        logger.error(f"Failed to hide window with hwnd: {hwnd}, error: {str(e)}")
        return False

def show_window(hwnd) -> bool:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        logger.info(f"Successfully shown window with hwnd: {hwnd}")
        return True
    except Exception as e:
        logger.error(f"Failed to show window with hwnd: {hwnd}, error: {str(e)}")
        return False

def enum_hwnd() -> list:
    windows = []
    def callback(hwnd, lParam):
        windows.append(hwnd)
        return True
    result = user32.EnumWindows(
        ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(callback),
        0)
    if result:
        logger.debug(f"Enumerated {len(windows)} windows")
        return windows
    else:
        logger.warning("EnumWindows failed")
        return []

def hwnd_get_name(hwnd) -> str:
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buffer, length)
    return buffer.value

def hwnd_get_pid(hwnd:int) -> int:
    pid = ctypes.c_int(0)
    user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
    logger.debug(f"Got PID {pid.value} for hwnd {hwnd}")
    return pid.value

def pid_get_hwnd(pid: int) -> list:
    hwnds = enum_hwnd()
    rt_hwnds = []
    for hwnd in hwnds:
        if hwnd_get_pid(hwnd) == pid:
            rt_hwnds.append(hwnd)
    logger.debug(f"Found {len(rt_hwnds)} windows for PID {pid}")
    return rt_hwnds

def kill_process(pid,force:bool = False):
    cmd = ["taskkill", "/PID", str(pid)]
    if force:
        cmd = ["taskkill", "/F", "/PID", str(pid)]

    if not isinstance(pid, int) or pid <= 0:
        raise ValueError(f"Invalid PID: {pid}")
    if sys.platform != 'win32':
        raise OSError("This function is only supported on Windows")
    try:
        logger.info(f"Attempting to kill process with PID: {pid}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            logger.info(f"Successfully killed process with PID: {pid}")
            return True
        else:
            logger.error(f"Failed to kill process {pid} because: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout while trying to kill process {pid}")
    except FileNotFoundError:
        logger.error("taskkill command not found. Ensure you're running on Windows.")


def set_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwarenessContext(-4)
    except Exception as e:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception as e2:
            raise e2

# -*- coding: utf-8 -*-
# Platform: Windows only

import time
import threading
import subprocess

from src.utils import *
from src.tray import TrayApp
from src.log import Logger,INFO
from src.web import open_web
from PIL.Image import Image

set_dpi_awareness()
logger = Logger("HideApp","log.log")
class HideApp:
    def __init__(self,Icon:Image,cmd:str,name = "HideApp",web_url:str = ""):
        self.process = None
        self.pid = None
        self.hwnds = None
        self.cmd = cmd
        self.web_url = web_url

        self.running = False
        self.monitor_thread = None

        self.app = TrayApp(Icon,name)
        self.app.add_menu("Show Windows",self.show_window)
        self.app.add_menu("Hide Windows",self.hide_window)
        if web_url:
            self.app.add_menu("Open Web",self.open_web)
        self.app.add_exit(self.exit)

        self.app.start()

    def open_web(self):
        logger.info(f"Open web: {self.web_url}")
        open_web(self.web_url)

    def start(self):
        self.running = True
        self.process = subprocess.Popen(
            self.cmd.strip().split(" "),
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
)
        self.pid = self.process.pid

        self.monitor_thread = threading.Thread(target=self.monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        get_hwnd = False
        for i in range(10):
            hwnds = pid_get_hwnd(self.pid)
            if len(hwnds) > 0:
                get_hwnd = True
                self.hwnds = hwnds
                break
            time.sleep(0.5)
        logger.info(f"Process started with PID: {self.pid}")
        if get_hwnd:
            logger.info(f"Window found for HWND: {self.hwnds}")
        else:
            logger.error("No window found for the given PID.")
            logger.warning("Window control will be disabled as no HWND was found.")
            self.hwnds = None
            
    def monitor(self):
        while self.running:
            poll_result = self.process.poll()
            if poll_result is not None:
                logger.info(f"Process has ended with return code: {poll_result}")
                self.running = False
                self.app.exit()
                return
            time.sleep(0.5)
    def exit(self):
        logger.info("Exiting...")
        self.running = False
        self.show_window()
        if self.process.poll() is None:
            kill_process(self.pid)
        time.sleep(0.5)
        if self.process.poll() is None:
            kill_process(self.pid,force=True)
    def hide_window(self):
        if self.hwnds:
            for i in self.hwnds:
                hide_window(i)
                logger.info(f"Hidden window with HWND: {i}")
        else:
            logger.error("No window found to hide.")
            return
    def show_window(self):
        if self.hwnds:
            for i in self.hwnds:
                show_window(i)
                logger.info(f"Shown window with HWND: {i}")
        else:
            logger.error("No window found to show.")
            return
    def wait(self):
        if self.app.thread:
            self.app.thread.join()
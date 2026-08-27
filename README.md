# Syncthing Hide Console

[简体中文](./doc/README_CN.md)

**Syncthing Hide Console** is a lightweight, modular utility designed specifically for Windows. Its purpose is to hide the console window of **Syncthing** (`syncthing.exe`) and run it as a system tray icon.

With this tool, you can run Syncthing silently in the background. You can easily show, hide, exit, or open the web GUI via the tray icon in the bottom-right corner, keeping your desktop clean and clutter-free.

In theory, any console application can be hidden using this tool, but please note that it is currently only applicable to **Windows** systems.

## Prerequisites

- **Operating System**: Windows (relies on `ctypes.windll`, `pywin32`, and Windows API)
- **Python Environment**: Python 3.6+
- **Dependencies**: See `requirements.txt`

## Quick Start

### 1. Install Dependencies

In the project directory, install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 2. Prepare Syncthing

Ensure `syncthing.exe` is located in the same directory as `main.py`. Alternatively, you can modify the `EXE_FILE_NAME` in the generated `config.json` to point to your Syncthing executable path.

### 3. Run the Program

Execute the main script directly:

```bash
python main.py
```

On the first run, the program will automatically generate a `config.json` configuration file and start logging to `log.log`.

## Features

- **Modular Architecture**: Refactored into clean modules (`src/log`, `src/icon`, `src/tray`, etc.) for better maintainability.
- **PID-Based Window Hiding**: Uses precise Process ID (PID) matching instead of fragile window title matching, ensuring reliability even if window titles change.
- **System Tray Integration**: Displays an icon in the taskbar notification area with a context menu.
- **Enhanced Control**:
  - **Show/Hide Windows**: Toggle the visibility of the Syncthing console.
  - **Open Web**: Quickly open the Syncthing Web GUI in your default browser.
  - **Exit**: Gracefully terminates the Syncthing process and closes the utility.
- **Advanced Logging**:
  - Color-coded console output for easy debugging.
  - Detailed file logging with exception stack traces.
- **Embedded Icon**: The app icon is embedded as Base85 encoded data, requiring no external image files.

## Pros & Cons

### Pros

1.  **Clean Interface**: Eliminates the default Syncthing console window without modifying the binary.
2.  **Robust Detection**: Uses PID to track the window, avoiding issues with dynamic window titles or multiple instances.
3.  **Convenient Operation**: Quick access to Show/Hide/Web GUI/Exit via the tray icon.
4.  **Zero Intrusiveness**: Operates as an external wrapper; does not alter Syncthing's core files.
5.  **Developer Friendly**: Modular code structure makes it easy to extend or integrate into other projects.

### Cons

1.  **Platform Limitation**: Supports **Windows** only.
2.  **Dependencies**: Requires Python environment and third-party libraries (`pystray`, `Pillow`, `pywin32`).
3.  **Process Lifecycle**: If this utility crashes, the Syncthing window may reappear (though the process continues running).

## Compile to Standalone Executable (.exe)

To use this on computers without Python or to **completely hide the console window**, compile it using `PyInstaller`.

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Compilation Command

Since the project is now modular (uses `src` package), we need to ensure all modules are included.

```bash
pyinstaller --noconsole --onefile --name "SyncthingTray" main.py
```

**Parameter Explanation:**
- `--noconsole`: **Critical**. Prevents the black command-line window from appearing.
- `--onefile`: Packages everything into a single `.exe`.
- `--name`: Sets the output executable name.

*Note: If you encounter issues with missing modules during execution, you might need to add `--hidden-import src` or explicitly include the `src` folder depending on your PyInstaller version.*

### 3. Retrieve Output

Locate `SyncthingTray.exe` in the `dist` folder. Place it in the same directory as `syncthing.exe` (or update `config.json` accordingly) and run it.

## File Structure

```text
.
├── main.py              # Entry point
├── src/                 # Source modules
│   ├── __init__.py
│   ├── log.py           # Logging handler with color support
│   ├── icon.py          # Icon encoding/decoding utilities
│   ├── config.py        # Configuration management
│   ├── hide_windows.py  # Core logic for hiding/showing windows
│   ├── tray.py          # System tray implementation
│   ├── utils.py         # Windows API wrappers (HWND, PID, etc.)
│   └── web.py           # Web browser opener
├── requirements.txt     # Python dependencies
├── config.json          # (Auto-generated) Configuration file
├── log.log              # (Auto-generated) Runtime logs
└── syncthing.exe        # (User-provided) Syncthing executable
```

## Configuration (`config.json`)

The configuration is simple and focused. Edit `config.json` if needed:

```json
{
    "EXE_FILE_NAME": "syncthing.exe"
}
```

- `EXE_FILE_NAME`: The filename or path of the executable you want to hide. Defaults to `syncthing.exe`.

*(Note: Previous versions supported `PART_OF_TITLE` and `FORCE_EXIT`. These have been removed or integrated into the core logic for better stability.)*

## Notes

- **Icon Extraction**: If you are curious about the icon data in `main.py`, you can decode it using the provided utility:
  ```python
  from src.icon import decode_icon
  # Assuming ICON is the string variable from main.py
  decode_icon(ICON).save("icon.png")
  ```
- **Graceful Exit**: When exiting via the tray menu, the tool attempts to close Syncthing gracefully. If it fails, it will force kill the process.
- **Web URL**: Currently, the "Open Web" feature opens the default Syncthing address (usually `http://127.0.0.1:8384`). You can customize this in the code if your Syncthing runs on a different port.

## License

The code for this project is open source under an MIT-style license. Syncthing itself follows the MPLv2 license.

---

*Made with ❤️ for a cleaner desktop.*

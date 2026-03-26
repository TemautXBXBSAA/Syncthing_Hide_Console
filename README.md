# Syncthing Hide Console
[[doc/README_CN.md|简体中文]]
**Syncthing Hide Console** is a lightweight utility designed specifically for Windows. Its purpose is to hide the console window of **Syncthing** (`syncthing.exe`) and run it as a system tray icon.

With this tool, you can run Syncthing silently in the background. You can easily show, hide, or exit the application via the tray icon in the bottom-right corner, keeping your desktop clean and clutter-free.

In theory, any console window can be hidden using this tool, but please note that this tool is only applicable to Windows systems.

## ⚠️ Prerequisites

- **Operating System**: Windows (relies on `ctypes.windll` and Windows API)
- **Python Environment**: Python 3.6+
- **Dependencies**: See `requirements.txt`

## 🚀 Quick Start

### 1. Install Dependencies

In the project directory, install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 2. Prepare Syncthing

Ensure `syncthing.exe` is located in the same directory as this script. Alternatively, modify the `EXE_FILE_NAME` path in the generated `config.json` to point to your Syncthing executable.

### 3. Run the Program

Execute the main script directly:

```bash
python main.py
```

On the first run, the program will automatically generate a `config.json` configuration file and a `latest_log.log` log file.

## ✨ Features

- **Auto-Hide**: Automatically detects the Syncthing process window upon startup and hides it immediately.
- **System Tray Integration**: Displays an icon in the taskbar notification area with a right-click context menu.
- **Flexible Control**:
  - **Show**: Temporarily display the Syncthing console window.
  - **Hide**: Hide the window again.
  - **Exit**: Gracefully terminate the Syncthing process and close this utility.
- **Persistent Configuration**: Supports customizing the Syncthing path and window title matching keywords via `config.json`.
- **Logging**: Detailed runtime status is recorded in `latest_log.log`, while error messages are saved to `error.log`.

## ⚖️ Pros & Cons

### ✅ Pros

1.  **Clean Interface**: Eliminates the default Syncthing console window without requiring reinstallation, preventing workspace distraction.
2.  **Convenient Operation**: Quickly show/hide the console or exit the program without needing to open a browser to access the GUI.
3.  **Zero Intrusiveness**: Does not modify Syncthing's core binary files; operates solely as an external wrapper.
4.  **Minimal Resource Usage**: Consumes negligible memory and CPU to maintain the tray icon and monitor window handles.
5.  **Easy Configuration**: Supports custom Syncthing paths, catering to users with non-standard installations.

### ❌ Cons

1.  **Platform Limitation**: Supports **Windows** only (due to Win32 API dependency); incompatible with macOS or Linux.
2.  **Dependencies**: Requires a Python environment and third-party libraries (`pystray`, `Pillow`), which is less convenient than a standalone executable unless compiled.
3.  **Title Matching Mechanism**: The program locates the Syncthing window based on its title (`PART_OF_TITLE`). If a Syncthing update significantly changes the window title format, manual adjustment of the configuration file may be required.
4.  **Process Lifecycle**: If this utility crashes unexpectedly, the Syncthing window may reappear (although the process continues running), requiring manual intervention or a script restart.

## 🛠️ Compile to Standalone Executable (.exe)

If you wish to use this on computers without Python installed, or if you want to **completely hide the console window during runtime**, it is recommended to compile using `PyInstaller`.

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Compilation Command (Critical Step)

To **hide the console**, you must use the `--noconsole` (or `--windowed`) flag. Additionally, to ensure the tray icon and dependencies work correctly, it is advisable to include `--onefile`.

```bash
pyinstaller --noconsole --onefile main.py
```

**Parameter Explanation:**
- `--noconsole`: **Critical parameter**. Instructs PyInstaller not to spawn a black command-line window. The program will run in the background, displaying only the system tray icon.
- `--onefile`: Packages all dependencies into a single `.exe` file for easy distribution.
- `--name`: Specifies the name of the generated executable.

### 3. Retrieve Output

After compilation, locate `main.exe` in the `dist` folder. You can rename this file and place it in the same directory as `syncthing.exe` to run directly.

## 📂 File Structure

```text
.
├── main.exe              # Main program script
├── requirements.txt     # List of Python dependencies
├── config.json          # (Auto-generated) Config file; editable for EXE path
├── latest_log.log       # (Auto-generated) Runtime logs
├── error.log            # (Auto-generated) Error logs
└── syncthing.exe        # (User-provided) Syncthing main program
```

## 🔧 Configuration (`config.json`)

If the default settings do not meet your needs, you can edit `config.json`:

```json
{
    "EXE_FILE_NAME": ".\\syncthing.exe",
    "PART_OF_TITLE": ""
}
```

- `EXE_FILE_NAME`: Relative or absolute path to the Syncthing executable.
- `PART_OF_TITLE`: Keyword used to match the window title. If left empty, it defaults to matching the filename of `EXE_FILE_NAME` (e.g., `syncthing.exe`). If your Syncthing window title has been customized, enter part of that title text here.

## 📝 Notes

- The tool includes the Syncthing icon embedded within the code (encoded in Base85), so no extra icon files need to be downloaded.
- When exiting, this tool attempts to terminate the Syncthing process, which may cause temporarily unsynced data to remain locked.

## 📄 License

The code for this project is open source under an MIT-style license (please refer to your project's actual license for specifics). Syncthing itself follows the MPLv2 license.

---

*Made with ❤️ for a cleaner desktop.*

# Syncthing Hide Console

[简体中文](./doc/README_CN.md)

**Syncthing Hide Console** is a lightweight utility designed specifically for Windows. Its purpose is to hide the console window of **Syncthing** (`syncthing.exe`) and manage it via a system tray icon.

With this tool, you can run Syncthing silently in the background. You can easily show, hide, or exit the application via the tray icon in the bottom-right corner, keeping your desktop clean and clutter-free.

> **Note:** While designed for Syncthing, this tool can theoretically hide any Windows console application by matching its window title.

## ⚠️ Prerequisites

- **Operating System**: Windows 10/11 (Relies on Win32 API via `pywin32`)
- **Python Environment**: Python 3.6+
- **Dependencies**: See `requirements.txt`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Path

Ensure `syncthing.exe` is located in the same directory as this script. 
*If your Syncthing executable is located elsewhere, you can modify the path in the `config.json` file generated after the first run.*

### 3. Run the Program

```bash
python main.py
```

On the first run, the program will automatically generate a `config.json` configuration file and a `log.log` file.

## ✨ Features

- **Auto-Hide**: Automatically detects the target process window upon startup and hides it immediately.
- **System Tray Integration**: Displays an icon in the taskbar notification area with a context menu.
- **Flexible Control**:
  - **Show**: Temporarily display the hidden console window.
  - **Hide**: Hide the window again.
  - **Exit**: Gracefully terminates the target process and closes the utility.
- **Smart Process Matching**: Uses both window title keywords and exact executable path matching to prevent accidental hiding of unrelated processes.
- **Graceful Shutdown**: Attempts to close the target application gracefully via `WM_CLOSE` before forcing termination if necessary.
- **Persistent Configuration**: Supports customizing the executable path, title matching keywords, and force-exit behavior via `config.json`.

## ⚖️ Pros & Cons

### ✅ Pros

1.  **Clean Interface**: Eliminates the persistent console window without modifying the original binary.
2.  **Non-Intrusive**: Operates as an external wrapper; does not inject code into Syncthing.
3.  **Safe Termination**: Prioritizes graceful shutdown signals to minimize data corruption risks.
4.  **Minimal Resource Usage**: Lightweight footprint, consuming negligible memory and CPU.

### ❌ Cons

1.  **Windows Only**: Incompatible with macOS or Linux due to Win32 API dependencies.
2.  **Title Dependency**: Relies on window titles for detection. If the target application significantly changes its window title format in updates, manual configuration adjustment may be required.
3.  **Process State**: If this utility crashes unexpectedly, the hidden window may reappear, though the underlying process will continue running.

## 📂 File Structure

```text
.
├── main.py              # Main source code
├── requirements.txt     # Python dependencies
├── config.json          # (Auto-generated) User configuration
├── log.log              # (Auto-generated) Runtime logs
├── error.log            # (Auto-generated) Error logs (if any)
└── syncthing.exe        # (User-provided) The target application
```

## 🔧 Configuration (`config.json`)

You can edit `config.json` to customize behavior:

```json
{
    "EXE_FILE_NAME": ".\\syncthing.exe",
    "PART_OF_TITLE": "",
    "FORCE_EXIT": false
}
```

| Key | Description |
| :--- | :--- |
| `EXE_FILE_NAME` | Relative or absolute path to the target executable. |
| `PART_OF_TITLE` | Keyword used to match the window title. If empty, defaults to the basename of `EXE_FILE_NAME` (e.g., `syncthing.exe`). Use this if the window title differs from the filename. |
| `FORCE_EXIT` | If `true`, the tool will forcefully kill the process if it doesn't close gracefully within a timeout. Default is `false`. |

## 📝 Notes

- **Icon Embedding**: The tray icon is embedded directly in the source code (Base85 encoded PNG), so no external image files are required.
- **Logging**: Detailed runtime logs are saved to `log.log`. Check `error.log` if the application fails to start.
- **Data Safety**: When exiting, the tool attempts to send a close signal to the target application. Ensure your data is synced before forcing an exit if `FORCE_EXIT` is enabled.

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

*Made with ❤️ for a cleaner desktop.*

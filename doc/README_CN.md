# Syncthing Hide Console

**Syncthing Hide Console** 是一个专为 Windows 设计的轻量级实用工具，旨在将 **Syncthing** (`syncthing.exe`) 的控制台窗口隐藏，并将其转换为系统托盘（System Tray）图标运行。

通过本工具，您可以在后台静默运行 Syncthing，并通过右下角的托盘图标轻松控制其显示、隐藏或退出，保持桌面整洁。

理论上，任何控制台窗口都可以通过本工具进行隐藏，但请务必注意，本工具仅适用于 Windows 系统。

## ⚠️ 前置要求

- **操作系统**: Windows (因为使用了 `ctypes.windll` 和 Windows API)
- **Python 环境**: Python 3.6+
- **依赖库**: 见 `requirements.txt`

## 🚀 快速开始

### 1. 安装依赖

在项目目录下，首先安装所需的 Python 库：

```bash
pip install -r requirements.txt
```

### 2. 准备 Syncthing

确保 `syncthing.exe` 位于本脚本同一目录下，或者修改生成的 `config.json` 中的 `EXE_FILE_NAME` 路径指向您的 Syncthing 可执行文件。

### 3. 运行程序

直接运行主脚本：

```bash
python main.py
```

首次运行时，程序会自动生成 `config.json` 配置文件和 `latest_log.log` 日志文件。

## ✨ 功能特点

- **自动隐藏**: 启动后自动查找 Syncthing 进程窗口并立即隐藏。
- **系统托盘集成**: 在任务栏右侧显示图标，提供右键菜单。
- **灵活控制**:
  - **Show**: 临时显示 Syncthing 控制台窗口。
  - **Hide**: 再次隐藏窗口。
  - **Exit**: 优雅地关闭 Syncthing 进程并退出本工具。
- **配置持久化**: 支持通过 `config.json` 自定义 Syncthing 路径和窗口标题匹配关键字。
- **日志记录**: 详细记录运行状态到 `latest_log.log`，错误信息记录到 `error.log`。

## ⚖️ 优缺点

### ✅ 优点

1.  **界面整洁**: 无需重新安装，彻底消除 Syncthing 默认的控制台窗口，避免干扰工作区。
2.  **操作便捷**: 无需打开浏览器访问 GUI 即可快速显示/隐藏控制台或退出程序。
3.  **零侵入性**: 不需要修改 Syncthing 的核心二进制文件，仅作为外部包装器（Wrapper）运行。
4.  **资源占用极低**: 仅占用极少的内存和 CPU 来维持托盘图标和窗口句柄监控。
5.  **易于配置**: 支持自定义 Syncthing 路径，方便非标准安装用户。

### ❌ 缺点

1.  **平台限制**: 仅支持 **Windows** 系统（依赖 Win32 API），不支持 macOS 或 Linux。
2.  **依赖关系**: 需要安装 Python 环境及第三方库 (`pystray`, `Pillow`)，不如单文件 exe 方便（除非编译）。
3.  **标题匹配机制**: 程序通过窗口标题（`PART_OF_TITLE`）来定位 Syncthing 窗口。如果 Syncthing 版本更新导致窗口标题格式大幅变化，可能需要手动调整配置文件。
4.  **进程生命周期**: 如果本工具意外崩溃，Syncthing 窗口可能会重新显示（虽然进程仍在运行），需要手动处理或通过脚本重启。

## 🛠️ 编译为独立可执行文件 (.exe)

如果您希望在没有安装 Python 环境的电脑上使用，或者想要**彻底隐藏运行时的控制台窗口**，建议使用 `PyInstaller` 进行编译。

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 编译命令 (关键步骤)

为了**隐藏控制台**，必须使用 `--noconsole` (或 `--windowed`) 参数。同时，为了确保托盘图标和依赖库正常工作，建议加上 `--onefile`。

```bash
pyinstaller --noconsole --onefile main.py
```

**参数说明：**
- `--noconsole`: **关键参数**。告诉 PyInstaller 不要弹出黑色的命令行窗口，程序将在后台运行，仅显示系统托盘图标。
- `--onefile`: 将所有依赖打包成一个单独的 `.exe` 文件，方便分发。
- `--name`: 生成的可执行文件名。

### 3. 获取输出

编译完成后，在 `dist` 文件夹下找到 `main.exe`。您重命名此文件，可以将此文件和 `syncthing.exe` 放在同一目录下直接运行。

## 📂 文件结构说明

```text
.
├── main.exe              # 主程序脚本
├── requirements.txt     # Python 依赖列表
├── config.json          # (自动生成) 配置文件，可编辑 EXE 路径
├── latest_log.log       # (自动生成) 运行日志
├── error.log            # (自动生成) 错误日志
└── syncthing.exe        # (需自备) Syncthing 主程序
```

## 🔧 配置说明 (`config.json`)

如果默认设置不满足需求，可以编辑 `config.json`：

```json
{
    "EXE_FILE_NAME": ".\\syncthing.exe",
    "PART_OF_TITLE": ""
}
```

- `EXE_FILE_NAME`: Syncthing 可执行文件的相对或绝对路径。
- `PART_OF_TITLE`: 用于匹配窗口标题的关键字。留空则默认使用 `EXE_FILE_NAME` 的文件名（例如 `syncthing.exe`）进行匹配。如果您的 Syncthing 窗口标题被自定义过，请在此填写部分标题文字。

## 📝 注意事项

- 本工具内置了 Syncthing 的图标（以 Base85 编码形式存储在代码中），无需额外下载图标文件。
- 退出程序时，本工具会尝试终止 Syncthing 进程，可能会导致出现未同步的数据暂时锁定。

## 📄 许可证

本项目代码基于 MIT 风格开源（具体请参考您项目的实际许可证）。Syncthing 本身遵循 MPLv2 许可证。

---

*Made with ❤️ for a cleaner desktop.*
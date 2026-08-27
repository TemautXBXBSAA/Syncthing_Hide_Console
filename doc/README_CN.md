# Syncthing Hide Console

[English](./README.md)

**Syncthing Hide Console** 是一个专为 Windows 设计的轻量级工具。它的主要目的是隐藏 **Syncthing** (`syncthing.exe`) 的控制台窗口，并将其作为系统托盘图标运行。

使用此工具，您可以在后台静默运行 Syncthing。通过右下角的托盘图标，您可以轻松地显示、隐藏窗口、打开网页管理界面或退出程序，保持桌面整洁清爽。

理论上，该工具可以隐藏任何控制台程序，但请注意目前仅支持 **Windows** 系统。

## 前置要求

- **操作系统**: Windows (依赖 `ctypes.windll`, `pywin32` 和 Windows API)
- **Python 环境**: Python 3.6+
- **依赖库**: 见 `requirements.txt`

## 快速开始

### 1. 安装依赖

在项目目录下安装所需的 Python 库：

```bash
pip install -r requirements.txt
```

### 2. 准备 Syncthing

确保 `syncthing.exe` 位于与 `main.py` 相同的目录中。或者，您可以修改生成的 `config.json` 中的 `EXE_FILE_NAME` 路径，指向您的 Syncthing 可执行文件。

### 3. 运行程序

直接执行主脚本：

```bash
python main.py
```

首次运行时，程序会自动生成 `config.json` 配置文件，并开始记录日志到 `log.log`。

## 功能特性

- **模块化架构**：代码重构为清晰的模块 (`src/log`, `src/icon`, `src/tray` 等)，易于维护和扩展。
- **PID 精确匹配**：使用进程 ID (PID) 精确关联窗口句柄，取代了脆弱的标题匹配机制，即使窗口标题变化也能稳定工作。
- **系统集成托盘**：在任务栏通知区域显示图标，并提供右键上下文菜单。
- **增强控制功能**：
  - **显示/隐藏窗口**：随时切换 Syncthing 控制台的可见性。
  - **打开网页**：一键在默认浏览器中打开 Syncthing Web 管理界面。
  - **退出**：优雅地终止 Syncthing 进程并关闭本工具。
- **高级日志系统**：
  - 控制台输出支持彩色区分（INFO, WARNING, ERROR）。
  - 文件日志包含详细的异常堆栈信息，便于调试。
- **内置图标**：应用图标以 Base85 编码形式嵌入代码中，无需额外的图片文件。

## 优缺点

### 优点

1.  **界面整洁**：无需修改二进制文件即可消除 Syncthing 默认的黑色控制台窗口。
2.  **稳定可靠**：基于 PID 的窗口查找机制，避免了因窗口标题动态变化或多实例导致的匹配错误。
3.  **操作便捷**：通过托盘菜单即可快速完成显示、隐藏、打开网页和退出操作。
4.  **零侵入性**：作为外部包装器运行，不修改 Syncthing 的核心文件。
5.  **开发者友好**：模块化代码结构清晰，方便二次开发或集成到其他项目中。

### 缺点

1.  **平台限制**：仅支持 **Windows** 系统。
2.  **依赖环境**：需要 Python 环境和第三方库 (`pystray`, `Pillow`, `pywin32`)，除非编译为 exe，否则部署稍显麻烦。
3.  **进程生命周期**：如果本工具意外崩溃，Syncthing 窗口可能会重新出现（尽管进程仍在运行），需要手动干预或重启脚本。

## 编译为独立可执行文件 (.exe)

如果您希望在未安装 Python 的电脑上使用，或者想**彻底隐藏运行时的控制台窗口**，建议使用 `PyInstaller` 进行编译。

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 编译命令

由于项目现在是模块化结构（使用了 `src` 包），我们需要确保所有模块都被包含。

```bash
pyinstaller --noconsole --onefile --name "SyncthingTray" main.py
```

**参数说明：**
- `--noconsole`: **关键参数**。指示 PyInstaller 不要生成黑色的命令行窗口。程序将在后台运行，仅显示系统托盘图标。
- `--onefile`: 将所有依赖打包成一个单独的 `.exe` 文件，便于分发。
- `--name`: 指定生成的可执行文件名称。

*注意：如果在运行时遇到缺少模块的错误，可能需要添加 `--hidden-import src` 或根据 PyInstaller 版本显式包含 `src` 文件夹。*

### 3. 获取输出

编译完成后，在 `dist` 文件夹中找到 `SyncthingTray.exe`。将其重命名并放置在与 `syncthing.exe` 相同的目录中（或相应更新 `config.json`）即可直接运行。

## 文件结构

```text
.
├── main.py              # 程序入口
├── src/                 # 源代码模块
│   ├── __init__.py
│   ├── log.py           # 支持彩色输出的日志处理模块
│   ├── icon.py          # 图标编码/解码工具
│   ├── config.py        # 配置管理模块
│   ├── hide_windows.py  # 隐藏/显示窗口的核心逻辑
│   ├── tray.py          # 系统托盘实现
│   ├── utils.py         # Windows API 封装 (HWND, PID 等)
│   └── web.py           # 网页浏览器打开工具
├── requirements.txt     # Python 依赖列表
├── config.json          # (自动生成) 配置文件
├── log.log              # (自动生成) 运行日志
└── syncthing.exe        # (用户提供) Syncthing 主程序
```

## 配置 (`config.json`)

配置非常简单。如有需要，可编辑 `config.json`：

```json
{
    "EXE_FILE_NAME": "syncthing.exe"
}
```

- `EXE_FILE_NAME`: 您要隐藏的可执行文件的文件名或路径。默认为 `syncthing.exe`。

*(注意：旧版本支持的 `PART_OF_TITLE` 和 `FORCE_EXIT` 已被移除或整合到核心逻辑中，以提高稳定性。)*

## 注意事项

- **图标提取**：如果您对 `main.py` 中的图标数据感到好奇，可以使用提供的工具将其解码：
  ```python
  from src.icon import decode_icon
  # 假设 ICON 是 main.py 中的字符串变量
  decode_icon(ICON).save("icon.png")
  ```
- **优雅退出**：通过托盘菜单退出时，工具会尝试优雅地关闭 Syncthing。如果失败，它将强制杀死进程。
- **网页地址**：目前“打开网页”功能打开的是默认的 Syncthing 地址（通常是 `http://127.0.0.1:8384`）。如果您的 Syncthing 运行在不同端口，可以在代码中进行自定义。

## License

本项目代码遵循 MIT 风格许可证开源。Syncthing 本身遵循 MPLv2 许可证。

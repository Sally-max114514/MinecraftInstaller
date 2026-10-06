# Minecraft 安装器

> 一个帮助同学们快速安装 Java 和 Minecraft(HMCL 启动器)的小工具。
> 作者:**weijianyu**

---

## 项目简介

本工具可以自动检测你的电脑上是否安装了 **Java** 和 **Minecraft**,
没有安装的话可以一键帮你下载安装,支持 **Windows / macOS / Linux** 三个平台。

目前有两个版本:

| 版本 | 界面 | 特点 |
| --- | --- | --- |
| `MinecraftInstaller.py` | 命令行交互 | 1.0 初版,按提示输入 y/n 即可 |
| `MinecraftInstaller2.0.py` | 图形界面(Tkinter) | 2.0 升级版,详见下方功能 |

## 2.0 版本功能特性

- 🖥️ **图形化界面**:运行状态一目了然,一键安装,带下载进度条和实时日志
- ☕ **Java 版本统一管理**:下拉框可选 JDK 17 / 21 / 25,
  下载地址自动生成,自动检测本机 Java 及其版本
- 🚀 **HMCL 启动器版本统一管理**:版本号集中配置,
  支持"获取最新版本"一键联网查询,下载地址自动生成
- 🎯 **一键安装**:先检查/安装 Java,再检查/安装启动器,全程自动
- 🌍 **三平台支持**:Windows / macOS / Linux
- 🧩 **版本管理集中化**:所有版本号集中在文件顶部 `DEFAULT_CONFIG`,
  改一个地方,所有下载链接自动更新

## 目录结构

```
Minecraft安装/
├── MinecraftInstaller.py          # 1.0 命令行版
├── MinecraftInstaller2.0.py       # 2.0 图形界面版
├── MinecraftInstaller2.0.exe      # 2.0 打包好的 Windows 可执行文件
├── MinecraftInstaller.png         # 运行截图
├── icon.ico                       # exe 图标
├── make_icon.py                   # 图标生成脚本
├── version_info.txt               # exe 版本信息(作者署名)
├── build_exe.bat                  # Windows 一键打包脚本
├── 打包说明.md                     # 详细的打包教程
├── .github/workflows/             # GitHub Actions 云端打包
└── README.md                      # 本文件
```

## 使用方法

### 方式一:直接运行 Windows exe(推荐给同学)

把 `MinecraftInstaller2.0.exe` 拷到任意 64 位 Windows 电脑,
**双击运行**即可,无需安装 Python。

> 右键 exe → 属性 → 详细信息,可以看到作者署名 weijianyu。

### 方式二:用 Python 运行源码

运行 1.0(命令行版):

```bash
python3 MinecraftInstaller.py
```

运行 2.0(图形界面版):

```bash
python3 MinecraftInstaller2.0.py
```

> Linux 运行 2.0 前需要安装 Tkinter:
> `sudo apt install python3-tk`
> Windows / macOS 的官方 Python 一般自带,无需额外安装。

## 打包成 exe

三种打包方式(完整步骤见 `打包说明.md`):

1. **Windows 一键打包**:装好 Python 后双击 `build_exe.bat`
2. **GitHub Actions 云端打包**:推送到仓库后手动触发工作流
3. **Linux 交叉打包**:用 Wine + Windows Python + PyInstaller(本机已实测通过)

打包时程序会自动嵌入 `icon.ico` 图标和 `version_info.txt` 里的作者信息。

## 常见问题

| 问题 | 解决办法 |
| --- | --- |
| 杀毒软件误报 exe | PyInstaller 打包的程序偶会被误报,加入信任即可 |
| Linux 运行提示没有 tkinter | `sudo apt install python3-tk` |
| 安装 Java 后仍提示未检测到 | 重新打开终端/重启程序,或检查 PATH 环境变量 |
| Linux 安装 Java 需要密码 | 按提示输入 sudo 密码;失败可按日志里的手动命令操作 |
| macOS 提示需要 symlink | 按 Homebrew 输出里的 ln 命令复制执行 |
| 下载失败 | 检查网络连接,或到官网手动下载 |
| 想换 JDK / HMCL 版本 | 2.0 界面里直接选择/输入;改默认值改 `DEFAULT_CONFIG` |

## 版本历史

- **1.0**:命令行交互式安装器(检测系统 → 检测 Java → 检测 Minecraft)
- **2.0**:图形化界面 + Java/HMCL 版本统一管理 + 一键安装 + 进度条与日志

---

📝 作者:weijianyu | 项目初衷:让身边的同学都能轻松装上 Minecraft

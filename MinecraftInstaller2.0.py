"""
MinecraftInstaller 2.0
======================
在 MinecraftInstaller.py 的基础上新增:
1. Java 版本统一管理: JDK 版本集中配置/选择,所有平台的下载地址自动生成,
   并自动检测本机 Java 及其版本。
2. HMCL 启动器版本统一管理: 启动器版本集中配置/选择,支持联网获取最新版本,
   下载地址自动生成。
3. 图形化界面: 基于 Tkinter 的状态面板 + 一键安装 + 实时日志与下载进度条,
   下载安装全程不卡界面。

作者: weijianyu

运行前请确保已安装 Tkinter:
  Debian/Ubuntu: sudo apt install python3-tk
  Windows/macOS 的官方 Python 一般自带。
"""

import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import urllib.request

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ============================================================
# 统一版本管理: 需要更换版本时,只需修改/选择这里的配置,
# 所有下载地址都会根据版本号自动生成。
# ============================================================
DEFAULT_CONFIG = {
    "JDK_VERSION": "25",            # 统一管理的 Java 主版本
    "HMCL_VERSION": "3.17.0.357",   # 统一管理的 HMCL 启动器版本
}
JDK_CHOICES = ("25", "21", "17")   # Oracle 提供 /latest/ 稳定链接的版本
HMCL_DOWNLOAD_BASE = "https://hmcl.glavo.site/download"
GITHUB_LATEST_API = "https://api.github.com/repos/huanghongxun/HMCL/releases/latest"
HMCL_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(\.\d+)?$")


# ============================================================
# 检测相关
# ============================================================
def get_os_name():
    """返回当前操作系统名称。"""
    if sys.platform == "win32":
        return "Windows"
    if sys.platform == "darwin":
        return "macOS"
    if sys.platform == "linux":
        return "Linux"
    return f"其他({sys.platform})"


def get_java_info():
    """检测本机 Java,返回版本字符串;未安装返回 None。"""
    java = shutil.which("java")
    if not java:
        return None
    try:
        result = subprocess.run([java, "-version"], capture_output=True,
                                text=True, timeout=10)
        first_line = (result.stdout + result.stderr).splitlines()[0]
        match = re.search(r'version "([^"]+)"', first_line)
        return match.group(1) if match else "未知版本"
    except Exception:
        return "未知版本"


def get_minecraft_path():
    """返回当前平台下 Minecraft 数据目录的真实路径。"""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(appdata, ".minecraft")
    return os.path.expanduser("~/.minecraft")


def get_downloads_dir():
    """返回"下载"文件夹路径(不存在则创建)。"""
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads, exist_ok=True)
    return downloads


def jdk_download_info(jdk_version):
    """根据统一管理的 JDK 版本,生成对应平台的下载地址与文件名。
    macOS 走 Homebrew,不需要下载安装包,返回 None。"""
    if sys.platform == "win32":
        return (f"https://download.oracle.com/java/{jdk_version}/latest/"
                f"jdk-{jdk_version}_windows-x64_bin.exe",
                f"jdk-{jdk_version}_windows-x64_bin.exe")
    if sys.platform == "linux":
        return (f"https://download.oracle.com/java/{jdk_version}/latest/"
                f"jdk-{jdk_version}_linux-x64_bin.deb",
                f"jdk-{jdk_version}_linux-x64_bin.deb")
    return None


def query_latest_hmcl_version():
    """从 GitHub Releases 查询 HMCL 最新稳定版本号,失败返回 None。"""
    request = urllib.request.Request(
        GITHUB_LATEST_API, headers={"User-Agent": "MinecraftInstaller2.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    tag = str(data.get("tag_name", "")).lstrip("v")
    return tag if HMCL_VERSION_PATTERN.match(tag) else None


# ============================================================
# 下载与安装
# ============================================================
def download_file(url, dest, log, set_progress):
    """下载文件,并通过回调实时汇报日志与进度(0~100)。"""
    log(f"正在下载: {url}")

    def hook(count, block_size, total_size):
        if total_size and total_size > 0:
            set_progress(min(100, int(count * block_size * 100 / total_size)))

    try:
        urllib.request.urlretrieve(url, dest, reporthook=hook)
    except Exception as e:
        raise RuntimeError(f"下载失败,请检查网络连接或手动下载: {e}") from e
    set_progress(100)
    log(f"下载完成: {dest}")


def install_java(jdk_version, log, set_progress):
    """按照统一管理的 JDK 版本安装 Java(三平台)。"""
    log(f"开始安装 Java {jdk_version} ...")
    if sys.platform == "win32":
        url, fname = jdk_download_info(jdk_version)
        dest = os.path.join(get_downloads_dir(), fname)
        download_file(url, dest, log, set_progress)
        log("正在打开安装向导,请在向导中完成安装...")
        os.startfile(dest)
        log("安装完成后,请重新运行本程序检测 Java。")
    elif sys.platform == "linux":
        url, fname = jdk_download_info(jdk_version)
        dest = os.path.join(os.path.expanduser("~"), fname)
        download_file(url, dest, log, set_progress)
        log("正在安装 deb 包,如果弹出密码提示请输入密码...")
        result = subprocess.call(["sudo", "dpkg", "-i", dest])
        if result != 0:
            log(f"安装失败(退出码 {result})。请在终端手动执行: sudo dpkg -i {dest}")
        else:
            log("Java 安装成功!")
    elif sys.platform == "darwin":
        log(f"正在通过 Homebrew 安装 openjdk@{jdk_version} ...")
        result = subprocess.call(["brew", "install", f"openjdk@{jdk_version}"])
        if result != 0:
            log(f"安装失败(退出码 {result}),请检查网络或手动安装。")
        else:
            log("Homebrew 安装完成。如果提示需要 symlink,请按提示复制执行 ln 命令。")
    else:
        log("当前操作系统不受支持。")


def install_hmcl(hmcl_version, log, set_progress):
    """按照统一管理的 HMCL 版本安装启动器(三平台)。"""
    log(f"开始安装 HMCL {hmcl_version} 启动器 ...")
    if sys.platform == "win32":
        url = f"{HMCL_DOWNLOAD_BASE}/HMCL-{hmcl_version}.exe"
        dest = os.path.join(get_downloads_dir(), f"HMCL-{hmcl_version}.exe")
        download_file(url, dest, log, set_progress)
        log("正在启动 HMCL 启动器...")
        os.startfile(dest)
    elif sys.platform in ("linux", "darwin"):
        if shutil.which("java") is None:
            log("警告: 还没有安装 Java,启动器可能无法运行。")
        url = f"{HMCL_DOWNLOAD_BASE}/HMCL-{hmcl_version}.jar"
        dest = os.path.join(os.path.expanduser("~"), f"HMCL-{hmcl_version}.jar")
        download_file(url, dest, log, set_progress)
        log("正在启动 HMCL 启动器...")
        subprocess.Popen(["java", "-jar", dest])
        log("启动器已在后台启动。")
    else:
        log("当前操作系统不受支持。")


def one_key_install(jdk_version, hmcl_version, log, set_progress):
    """一键安装: 先检查/安装 Java,再检查/安装 HMCL 启动器。"""
    log("========== 一键安装开始 ==========")
    java_info = get_java_info()
    if java_info:
        log(f"Java 已安装,版本: {java_info}")
    else:
        log("未检测到 Java,开始安装...")
        install_java(jdk_version, log, set_progress)

    minecraft_path = get_minecraft_path()
    if os.path.exists(minecraft_path):
        log(f"Minecraft 已安装(路径: {minecraft_path}),跳过启动器安装。")
    else:
        log("未检测到 Minecraft,开始安装启动器...")
        install_hmcl(hmcl_version, log, set_progress)
    log("========== 一键安装完成 ==========")


# ============================================================
# 图形化界面
# ============================================================
class MinecraftInstallerApp:
    def __init__(self, root):
        self.root = root
        self.config = dict(DEFAULT_CONFIG)
        self.msg_queue = queue.Queue()
        self.busy = False
        self._build_widgets()
        self.refresh_status()
        self.root.after(100, self._poll_queue)

    # ---------- 界面搭建 ----------
    def _build_widgets(self):
        self.root.title("Minecraft 安装器 2.0")
        self.root.geometry("680x620")
        self.root.resizable(True, True)

        title = ttk.Label(self.root, text="Minecraft 安装器 2.0",
                          font=("", 16, "bold"))
        title.pack(padx=10, pady=(6, 0))
        author = ttk.Label(self.root, text="作者: weijianyu", foreground="gray")
        author.pack(pady=(0, 6))

        # 运行状态
        status_frame = ttk.LabelFrame(self.root, text="运行状态")
        status_frame.pack(fill="x", padx=10, pady=4)
        self.os_label = ttk.Label(status_frame, text="")
        self.java_label = ttk.Label(status_frame, text="")
        self.mc_label = ttk.Label(status_frame, text="")
        for label in (self.os_label, self.java_label, self.mc_label):
            label.pack(anchor="w", padx=10, pady=2)

        # 统一版本管理
        ver_frame = ttk.LabelFrame(
            self.root, text="统一版本管理(所有下载地址由这里的版本自动生成)")
        ver_frame.pack(fill="x", padx=10, pady=4)
        row1 = ttk.Frame(ver_frame)
        row1.pack(fill="x", padx=10, pady=4)
        ttk.Label(row1, text="Java 版本:").pack(side="left")
        self.jdk_var = tk.StringVar(value=self.config["JDK_VERSION"])
        self.jdk_combo = ttk.Combobox(row1, textvariable=self.jdk_var,
                                      values=JDK_CHOICES, state="readonly",
                                      width=8)
        self.jdk_combo.pack(side="left", padx=6)
        self.jdk_combo.bind("<<ComboboxSelected>>", self._on_config_change)

        row2 = ttk.Frame(ver_frame)
        row2.pack(fill="x", padx=10, pady=4)
        ttk.Label(row2, text="HMCL 版本:").pack(side="left")
        self.hmcl_var = tk.StringVar(value=self.config["HMCL_VERSION"])
        self.hmcl_entry = ttk.Entry(row2, textvariable=self.hmcl_var, width=16)
        self.hmcl_entry.pack(side="left", padx=6)
        self.hmcl_entry.bind("<KeyRelease>", self._on_config_change)
        self.latest_btn = ttk.Button(row2, text="获取最新版本",
                                     command=self.on_fetch_latest)
        self.latest_btn.pack(side="left", padx=6)

        self.config_label = ttk.Label(ver_frame, text="", foreground="gray")
        self.config_label.pack(anchor="w", padx=10, pady=(0, 4))

        # 操作
        op_frame = ttk.LabelFrame(self.root, text="操作")
        op_frame.pack(fill="x", padx=10, pady=4)
        btn_row = ttk.Frame(op_frame)
        btn_row.pack(fill="x", padx=10, pady=4)
        ttk.Button(btn_row, text="安装 Java",
                   command=self.on_install_java).pack(side="left", padx=4)
        ttk.Button(btn_row, text="安装 HMCL 启动器",
                   command=self.on_install_hmcl).pack(side="left", padx=4)
        ttk.Button(btn_row, text="一键安装",
                   command=self.on_one_key).pack(side="left", padx=4)
        ttk.Button(btn_row, text="刷新状态",
                   command=self.refresh_status).pack(side="left", padx=4)
        ttk.Button(btn_row, text="退出",
                   command=self.root.destroy).pack(side="right", padx=4)
        self.progress = ttk.Progressbar(op_frame, maximum=100,
                                        mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(0, 8))

        # 日志
        log_frame = ttk.LabelFrame(self.root, text="日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10,
                                                  state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=8)

    # ---------- 状态与日志 ----------
    def refresh_status(self):
        self.os_label.config(text=f"当前操作系统: {get_os_name()}")
        java_info = get_java_info()
        if java_info:
            self.java_label.config(
                text=f'Java 状态: 已安装(java version "{java_info}")')
        else:
            self.java_label.config(text="Java 状态: 未安装")
        minecraft_path = get_minecraft_path()
        if os.path.exists(minecraft_path):
            self.mc_label.config(
                text=f"Minecraft 状态: 已安装(路径: {minecraft_path})")
        else:
            self.mc_label.config(
                text=f"Minecraft 状态: 未安装(路径: {minecraft_path})")
        self._on_config_change()

    def _on_config_change(self, event=None):
        self.config["JDK_VERSION"] = self.jdk_var.get()
        self.config["HMCL_VERSION"] = self.hmcl_var.get().strip()
        self.config_label.config(
            text=f"当前统一配置: JDK {self.config['JDK_VERSION']} "
                 f"/ HMCL {self.config['HMCL_VERSION']}")

    def log(self, text):
        self.msg_queue.put(("log", text))

    def set_progress(self, pct):
        self.msg_queue.put(("progress", pct))

    def _append_log(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _poll_queue(self):
        try:
            while True:
                kind, value = self.msg_queue.get_nowait()
                if kind == "log":
                    self._append_log(value)
                elif kind == "progress":
                    self.progress["value"] = value
                elif kind == "hmcl_version":
                    self.hmcl_var.set(value)
                elif kind == "done":
                    self.busy = False
                    self.progress["value"] = 0
                    self.refresh_status()
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    # ---------- 后台任务 ----------
    def run_async(self, worker):
        if self.busy:
            messagebox.showinfo("提示", "已有任务正在运行,请等待完成后再操作。")
            return
        self.busy = True
        self.progress["value"] = 0

        def _run():
            try:
                worker()
            except Exception as e:
                self.log(f"出错: {e}")
            finally:
                self.msg_queue.put(("done", None))

        threading.Thread(target=_run, daemon=True).start()

    # ---------- 按钮事件 ----------
    def on_install_java(self):
        version = self.jdk_var.get()
        self.run_async(lambda: install_java(version, self.log, self.set_progress))

    def on_install_hmcl(self):
        version = self.hmcl_var.get().strip()
        if not HMCL_VERSION_PATTERN.match(version):
            messagebox.showwarning("提示", "HMCL 版本号格式不正确,例如: 3.17.0.357")
            return
        self.run_async(lambda: install_hmcl(version, self.log, self.set_progress))

    def on_one_key(self):
        jdk = self.jdk_var.get()
        hmcl = self.hmcl_var.get().strip()
        if not HMCL_VERSION_PATTERN.match(hmcl):
            messagebox.showwarning("提示", "HMCL 版本号格式不正确,例如: 3.17.0.357")
            return
        self.run_async(
            lambda: one_key_install(jdk, hmcl, self.log, self.set_progress))

    def on_fetch_latest(self):
        self.run_async(self._fetch_latest_worker)

    def _fetch_latest_worker(self):
        self.log("正在获取 HMCL 最新版本...")
        version = query_latest_hmcl_version()
        if version:
            self.msg_queue.put(("hmcl_version", version))
            self.log(f"已获取最新版本: {version}")
            self.log("提示: 官网(hmcl.glavo.site)上可能还有更新的版本。")
        else:
            self.log("获取失败,请手动填写版本号"
                     "(可到官网 https://hmcl.huangyuhui.net 查看)。")


def main():
    try:
        if sys.platform == "win32":
            # Windows 控制台默认 GBK,避免打印中文乱码
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass
    root = tk.Tk()
    MinecraftInstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

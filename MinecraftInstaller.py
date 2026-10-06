import sys
import os
import shutil


def ask_yes_no(prompt):
    """询问用户 y/n，输入其他内容时提示并重新输入。"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "n"):
            return choice == "y"
        print("无效的选项，请你重新输入！")


def check_os():
    try:
        #检查操作系统类型
        if sys.platform == "win32":
            print("当前操作系统为Windows")
        elif sys.platform == "darwin":
            print("当前操作系统为MacOS")
        elif sys.platform == "linux":
            print("当前操作系统为Linux")
        else:
            print("当前操作系统不受支持")
            sys.exit(1)
    except Exception as e:
        print("检查操作系统时出现错误:", e)
        sys.exit(1)

def check_java():
    try:
        #检查本机是否安装了Java
        if shutil.which("java") is not None:
            print("你的电脑已经安装了Java")
            return
        if ask_yes_no("你的电脑还没有安装java,你是否需要安装java？(y/n)"):
            print("正在为你安装java...")#访问甲骨文官方网站，下载对应系统的java安装包
            if sys.platform == "win32":
                exit_code = os.system('curl -L -o jdk-25_windows-x64_bin.exe "https://download.oracle.com/java/25/latest/jdk-25_windows-x64_bin.exe"')
                if exit_code != 0:
                    print("下载java失败，请检查网络连接或手动下载java。")
                    sys.exit(1)
                print("下载完成，请运行 jdk-25_windows-x64_bin.exe 完成安装。")
            elif sys.platform == "darwin":
                exit_code = os.system("brew install openjdk@25")
                if exit_code != 0:
                    print("安装java失败，请检查网络连接或手动安装java。")
                    sys.exit(1)
                print(" Homebrew 给了提示，照抄就行\n装完 brew install openjdk@25 后，\n")
                print("终端通常会打印一段“For the system Java wrappers to find this JDK, symlink it with...”的提示，\n")
                print("里面就包含了你需要执行的那条 ln 命令。直接复制粘贴就好，不用自己拼路径。")
            elif sys.platform == "linux":
                exit_code = os.system("wget https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.deb -O ~/jdk-25_linux-x64_bin.deb && sudo dpkg -i ~/jdk-25_linux-x64_bin.deb")
                if exit_code != 0:
                    print("下载或安装java失败，请检查网络连接或手动安装java。")
                    sys.exit(1)
            else:
                print("当前操作系统不受支持，无法自动安装java。")
                sys.exit(1)
            #安装完成后重新检测一次
            if shutil.which("java") is not None:
                print("Java 安装成功！")
            else:
                print("暂时还没有检测到java，请确认安装完成并重新打开终端后再运行本程序。")
        else:
            sys.exit(0)
    except Exception as e:
        print("检查java安装时出现错误:", e)
        sys.exit(1)

def install_minecraft():
    try:
        #检查本机是否安装了Minecraft
        if sys.platform == "win32":
            appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
            minecraft_path = os.path.join(appdata, ".minecraft")
        else:
            minecraft_path = os.path.expanduser("~/.minecraft")
        print(f"Minecraft路径: {minecraft_path}")
        if not os.path.exists(minecraft_path):
            if ask_yes_no("你的电脑还没有安装Minecraft,你是否需要安装Minecraft启动器？(y/n)"):
                print("正在为你安装Minecraft启动器...")
                if sys.platform == "win32":
                    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                    launcher = os.path.join(downloads, "HMCL-3.17.0.357.exe")
                    exit_code = os.system(f'curl -L -o "{launcher}" https://hmcl.glavo.site/download/HMCL-3.17.0.357.exe')
                    if exit_code != 0:
                        print("下载Minecraft启动器失败，请检查网络连接或手动下载启动器。")
                        sys.exit(1)
                    os.system(f'"{launcher}"')
                elif sys.platform == "darwin":
                    exit_code = os.system("curl https://hmcl.glavo.site/download/HMCL-3.17.0.357.jar -o ~/HMCL.jar")
                    if exit_code != 0:
                        print("下载Minecraft启动器失败，请检查网络连接或手动下载启动器。")
                        sys.exit(1)
                    os.system("java -jar ~/HMCL.jar")
                elif sys.platform == "linux":
                    exit_code = os.system("wget https://hmcl.glavo.site/download/HMCL-3.17.0.357.jar -O ~/HMCL.jar")
                    if exit_code != 0:
                        print("下载Minecraft启动器失败，请检查网络连接或手动下载启动器。")
                        sys.exit(1)
                    os.system("java -jar ~/HMCL.jar")
                else:
                    print("当前操作系统不受支持，无法自动安装Minecraft启动器。")
                    sys.exit(1)
            else:
                sys.exit(0)
        else:
            print("你的电脑已经安装了Minecraft,祝你游戏愉快！")
    except Exception as e:
        print("检查Minecraft安装时出现错误:", e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            #Windows 控制台默认 GBK，避免打印中文乱码
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass
    check_os()
    check_java()
    install_minecraft()

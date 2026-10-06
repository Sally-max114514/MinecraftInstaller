#!/bin/bash
# ============================================================
#  一键把本项目托管到 GitHub
#  作者: Sally-max114514
#
#  使用方法: 在终端里执行  bash 上传到GitHub.sh
#  1. 首次运行会提示登录:浏览器打开 github.com/login/device
#     输入终端里显示的 8 位验证码,并在网页上点"授权"。
#  2. 登录成功后,脚本会自动创建公开仓库 MinecraftInstaller
#     并推送全部代码。
#  如果想创建私有仓库,把下面第 2 步命令里的 --public 改成 --private。
# ============================================================
set -e
cd "$(dirname "$0")"

GH=~/.local/bin/gh
[ -x "$GH" ] || GH=gh

echo "================ GitHub 托管 ================"
echo "[1/3] 登录 GitHub ..."
echo "      如果浏览器没有自动打开,请手动访问: https://github.com/login/device"
$GH auth login --hostname github.com --git-protocol https --web
echo "      登录成功!"

echo "[2/3] 创建远程仓库 MinecraftInstaller 并推送 ..."
$GH repo create MinecraftInstaller --public --source=. --remote=origin --push \
    --description "Minecraft 安装器:图形化一键安装 Java 与 HMCL 启动器(作者 Sally-max114514)"

echo "[3/3] 完成!"
echo "      仓库地址已在上方输出,也可以运行: $GH repo view --web"
echo "      之后每次改完代码,提交推送只需要:"
echo "          git add -A"
echo "          git commit -m \"更新说明\""
echo "          git push"

@echo off
chcp 65001 >nul
title Minecraft 安装器 2.0 打包工具 - 作者 Sally-max114514
cd /d "%~dp0"

echo ==================================================
echo   Minecraft 安装器 2.0 - Windows EXE 打包工具
echo   作者: Sally-max114514
echo ==================================================
echo.

set "PY=python"
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo [错误] 没有检测到 Python!
        echo 请先到 https://www.python.org/downloads/ 下载安装 Python,
        echo 安装时请务必勾选 "Add python.exe to PATH"。
        echo.
        pause
        exit /b 1
    )
    set "PY=py -3"
)

echo [1/3] 安装打包工具 PyInstaller ...
%PY% -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败,请检查网络后重试。
    pause
    exit /b 1
)

echo [2/3] 开始打包,请耐心等待几分钟 ...
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name MinecraftInstaller2.0 --icon icon.ico --version-file version_info.txt MinecraftInstaller2.0.py
if errorlevel 1 (
    echo [错误] 打包失败,请查看上方报错信息。
    pause
    exit /b 1
)

echo.
echo [3/3] 打包完成!
echo 生成文件: %CD%\dist\MinecraftInstaller2.0.exe
echo 作者: Sally-max114514
echo.
echo 右键 exe - 属性 - 详细信息,可以查看作者与版本信息。
echo.
pause

@echo off
chcp 65001 >nul
title 节拍器APK编译脚本

echo ============================================
echo    节拍器 - Android APK 编译工具
echo ============================================
echo.

REM 设置环境变量 (使用用户的SDK路径)
set ANDROID_HOME=E:\Android SDK\sdk
set ANDROID_SDK_ROOT=E:\Android SDK\sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools\bin

echo [1/4] 检查环境配置...
echo    ANDROID_HOME = %ANDROID_HOME%
echo.

REM 检查目录是否存在
if not exist "%ANDROID_HOME%\build-tools" (
    echo [错误] Android SDK Build-Tools 未找到！
    echo    请确保 Android SDK 已正确安装
    pause
    exit /b 1
)

echo [2/4] 检查Python和Buildozer...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装！
    echo    请先安装 Python 3.8-3.11
    pause
    exit /b 1
)

pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装 Buildozer...
    pip install buildozer kivy
)

echo [3/4] 编译APK（这可能需要10-30分钟）...
echo.
cd /d "%~dp0"
buildozer android debug

if errorlevel 1 (
    echo.
    echo [错误] 编译失败！
    echo    请检查上方的错误信息
    pause
    exit /b 1
)

echo [4/4] 编译完成！
echo.
echo ============================================
echo    恭喜！APK已成功生成！
echo ============================================
echo.
echo APK文件位置: bin\metronome-0.1-arm64-v8a_armeabi-v7a-debug.apk
echo.

REM 打开bin目录
explorer.exe "%~dp0bin"

pause
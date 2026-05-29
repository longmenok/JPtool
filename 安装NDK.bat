@echo off
chcp 65001 >nul
title Android NDK 安装工具

echo ============================================
echo    Android NDK 自动安装工具
echo ============================================
echo.

REM 设置SDK路径 (使用用户的SDK路径)
set ANDROID_HOME=E:\Android SDK\sdk
set SDK_MANAGER=%ANDROID_HOME%\tools\bin\sdkmanager.bat

echo [1/3] 检查SDK Manager...
if not exist "%SDK_MANAGER%" (
    echo [错误] 未找到SDK Manager！
    echo    请确保 Android SDK 已正确安装
    echo    预期位置: %SDK_MANAGER%
    pause
    exit /b 1
)

echo [2/3] 使用SDK Manager安装NDK...
echo    这可能需要5-15分钟，请耐心等待...
echo.

REM 列出可用的NDK版本
echo [信息] 可用的NDK版本:
"%SDK_MANAGER%" --list | findstr /C:"ndk"

echo.
echo [提示] 开始安装 NDK r25b (推荐版本)...
echo.

REM 安装NDK
"%SDK_MANAGER%" "ndk;25.2.9519653"

if errorlevel 1 (
    echo.
    echo [信息] 尝试安装其他版本...
    "%SDK_MANAGER%" "ndk;25.1.8937394"
)

echo [3/3] 安装完成！
echo.

REM 检查安装结果
if exist "%ANDROID_HOME%\ndk" (
    echo [成功] NDK已安装到: %ANDROID_HOME%\ndk
    echo.
    dir "%ANDROID_HOME%\ndk" /b
) else (
    echo [警告] NDK可能未正确安装
)

echo.
echo ============================================
echo    下一步：运行 编译APK.bat
echo ============================================
pause
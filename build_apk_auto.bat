@echo off
chcp 65001 >nul
title 节拍器APK自动打包工具

echo ========================================
echo    节拍器APK自动打包工具
echo ========================================
echo.

REM 设置环境变量
set ANDROID_HOME=E:\Android SDK\sdk
set ANDROID_SDK_ROOT=E:\Android SDK\sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools\bin

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot
set PATH=%JAVA_HOME%\bin;%PATH%

echo [1/5] 环境配置完成
echo    Java: %JAVA_HOME%
echo    Android: %ANDROID_HOME%
echo.

cd /d "%~dp0"

echo [2/5] 检查项目文件
if not exist "main.py" (
    echo [错误] 未找到main.py文件
    pause
    exit /b 1
)
echo    项目文件检查通过
echo.

echo [3/5] 开始打包（首次运行可能需要30-60分钟）
echo    正在初始化构建环境...
echo    请耐心等待，无需任何操作
echo.

REM 使用PowerShell自动输入确认
powershell -Command "$env:BUILDROOT_WARNING = 'skip'; 'y' | & buildozer android debug 2>&1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   [错误] 打包失败！
    echo ========================================
    echo.
    echo 请检查：
    echo 1. 网络连接是否正常
    echo 2. 磁盘空间是否充足（建议10GB以上）
    echo 3. 是否有杀毒软件拦截
    echo.
    pause
    exit /b 1
)

echo.
echo [4/5] 检查APK文件
if exist "bin\*.apk" (
    echo    APK生成成功！
    echo.
    echo ========================================
    echo    打包成功！
    echo ========================================
    echo.
    dir /b bin\*.apk
    echo.
    echo APK文件位置：%~dp0bin\
    echo.
    explorer bin
) else (
    echo [警告] 未找到APK文件，可能需要检查
    echo.
)

echo [5/5] 打包流程完成
echo.
pause

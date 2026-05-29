@echo off
chcp 65001 >nul
title 环境检查工具

echo ============================================
echo    节拍器 - 开发环境检查
echo ============================================
echo.

set ANDROID_HOME=E:\Android SDK\sdk
set JAVA_HOME_OLD=%JAVA_HOME%

REM 检查Java
echo [检查 1/4] Java JDK...
java -version >nul 2>&1
if errorlevel 1 (
    echo    [❌ 未找到] 请安装 Java JDK 11+
    echo    下载地址: https://adoptium.net/temurin/releases/?version=11
) else (
    echo    [✓ 已找到]
    java -version 2>&1 | findstr "version"
)

REM 检查Android SDK
echo.
echo [检查 2/4] Android SDK...
if exist "%ANDROID_HOME%" (
    echo    [✓ 已找到] %ANDROID_HOME%
    if exist "%ANDROID_HOME%\build-tools" (
        echo    Build Tools: [✓]
    ) else (
        echo    Build Tools: [❌ 缺失]
    )
    if exist "%ANDROID_HOME%\platforms" (
        echo    Platforms: [✓]
    ) else (
        echo    Platforms: [❌ 缺失]
    )
) else (
    echo    [❌ 未找到] 请安装 Android Studio
)

REM 检查NDK
echo.
echo [检查 3/4] Android NDK...
if exist "%ANDROID_HOME%\ndk" (
    echo    [✓ 已找到] NDK
    dir /b "%ANDROID_HOME%\ndk" 2>nul
) else (
    echo    [❌ 未找到] 运行 安装NDK.bat 来安装
)

REM 检查Buildozer
echo.
echo [检查 4/4] Buildozer...
pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo    [❌ 未安装] 运行: pip install buildozer
) else (
    echo    [✓ 已安装]
    pip show buildozer | findstr "Version:"
)

REM 总结
echo.
echo ============================================
echo    检查完成
echo ============================================
echo.

if exist "%ANDROID_HOME%\ndk" (
    if not errorlevel 1 (
        echo 所有必需组件已安装！
        echo.
        echo 现在可以运行 编译APK.bat 开始编译APK
        echo.
    )
)

echo 操作选项:
echo   1. 安装 Java JDK 11 (打开下载页面)
echo   2. 安装 Android NDK (自动下载)
echo   3. 安装 Buildozer (pip install)
echo   4. 编译 APK
echo   5. 退出
echo.

set /p choice=请选择 (1-5): 

if "%choice%"=="1" start https://adoptium.net/temurin/releases/?version=11
if "%choice%"=="2" call 安装NDK.bat
if "%choice%"=="3" pip install buildozer
if "%choice%"=="4" call 编译APK.bat
if "%choice%"=="5" exit

pause
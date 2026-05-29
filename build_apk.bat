@echo off
setlocal
title Build APK

echo ============================================
echo    Metronome - Build APK
echo ============================================
echo.

set ANDROID_HOME=E:\Android SDK\sdk
set ANDROID_SDK_ROOT=E:\Android SDK\sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools\bin

echo [1/4] Checking environment...
echo    ANDROID_HOME = %ANDROID_HOME%
echo.

if not exist "%ANDROID_HOME%\build-tools" (
    echo    [FAIL] Build Tools not found!
    pause
    exit /b 1
)

echo [2/4] Checking Python and Buildozer...
python --version >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Python not installed!
    pause
    exit /b 1
)

pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo    Installing Buildozer...
    pip install buildozer kivy
)

echo [3/4] Building APK (may take 10-30 minutes)...
echo.
cd /d "%~dp0"
buildozer android debug

if errorlevel 1 (
    echo.
    echo    [FAIL] Build failed!
    echo    Check error messages above.
    pause
    exit /b 1
)

echo [4/4] Build complete!
echo.
echo ============================================
echo    APK generated successfully!
echo ============================================
echo.
echo APK Location: bin\metronome-0.1-arm64-v8a_armeabi-v7a-debug.apk
echo.

explorer.exe "%~dp0bin"

pause
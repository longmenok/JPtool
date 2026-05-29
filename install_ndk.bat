@echo off
setlocal
title NDK Installer

echo ============================================
echo    Android NDK Installer
echo ============================================
echo.

set ANDROID_HOME=E:\Android SDK\sdk
set SDK_MANAGER=%ANDROID_HOME%\tools\bin\sdkmanager.bat

echo [1/3] Checking SDK Manager...
if not exist "%SDK_MANAGER%" (
    echo    [FAIL] SDK Manager not found!
    echo    Expected: %SDK_MANAGER%
    pause
    exit /b 1
)

echo [2/3] Installing NDK...
echo    This may take 5-15 minutes...
echo.

"%SDK_MANAGER%" "ndk;25.2.9519653"

if errorlevel 1 (
    echo.
    echo    Trying alternative version...
    "%SDK_MANAGER%" "ndk;25.1.8937394"
)

echo [3/3] Installation complete!
echo.

if exist "%ANDROID_HOME%\ndk" (
    echo    [OK] NDK installed to: %ANDROID_HOME%\ndk
    echo.
    dir "%ANDROID_HOME%\ndk" /b
) else (
    echo    [WARN] NDK may not be installed correctly
)

echo.
echo ============================================
echo    Next: Run build_apk.bat
echo ============================================
pause
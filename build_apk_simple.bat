@echo off
title Build Metronome APK

echo ========================================
echo    Build Metronome APK
echo ========================================
echo.

set ANDROID_HOME=E:\Android SDK\sdk
set ANDROID_SDK_ROOT=E:\Android SDK\sdk
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools\bin;%PATH%

cd /d "%~dp0"

echo [1/3] Environment configured
echo    Java: %JAVA_HOME%
echo    Android: %ANDROID_HOME%
echo.

echo [2/3] Starting build...
echo    This may take 30-60 minutes on first run
echo.

echo y | buildozer android debug

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo    Build failed!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Checking APK...
if exist "bin\*.apk" (
    echo    APK built successfully!
    echo.
    echo ========================================
    echo    Success!
    echo ========================================
    echo.
    dir /b bin\*.apk
    echo.
    echo APK location: %~dp0bin\
    echo.
    explorer bin
)

echo.
echo Done!
echo.
pause

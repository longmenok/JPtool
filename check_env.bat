@echo off
setlocal
title Environment Check

echo ============================================
echo    Metronome - Development Environment Check
echo ============================================
echo.

set ANDROID_HOME=E:\Android SDK\sdk

REM Check Java
echo [Check 1/4] Java JDK...
java -version >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Not found. Please install JDK 11+
    echo    Download: https://adoptium.net/temurin/releases/?version=11
) else (
    echo    [OK] Found
    java -version 2>&1 | findstr "version"
)

REM Check Android SDK
echo.
echo [Check 2/4] Android SDK...
if exist "%ANDROID_HOME%" (
    echo    [OK] Found: %ANDROID_HOME%
    if exist "%ANDROID_HOME%\build-tools" (
        echo    Build Tools: [OK]
    ) else (
        echo    Build Tools: [FAIL]
    )
    if exist "%ANDROID_HOME%\platforms" (
        echo    Platforms: [OK]
    ) else (
        echo    Platforms: [FAIL]
    )
) else (
    echo    [FAIL] Not found
)

REM Check NDK
echo.
echo [Check 3/4] Android NDK...
if exist "%ANDROID_HOME%\ndk" (
    echo    [OK] Found NDK
    dir /b "%ANDROID_HOME%\ndk" 2>nul
) else (
    echo    [FAIL] Not found. Run install_ndk.bat
)

REM Check Buildozer
echo.
echo [Check 4/4] Buildozer...
pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Not installed. Run: pip install buildozer
) else (
    echo    [OK] Installed
    pip show buildozer | findstr "Version:"
)

echo.
echo ============================================
echo    Check Complete
echo ============================================
echo.

echo Options:
echo   1. Open JDK download page
echo   2. Install NDK
echo   3. Install Buildozer
echo   4. Build APK
echo   5. Exit
echo.

set /p choice=Enter choice (1-5): 

if "%choice%"=="1" start https://adoptium.net/temurin/releases/?version=11
if "%choice%"=="2" call install_ndk.bat
if "%choice%"=="3" pip install buildozer
if "%choice%"=="4" call build_apk.bat
if "%choice%"=="5" exit

pause
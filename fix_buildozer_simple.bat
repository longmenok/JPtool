@echo off
title Fix Buildozer Android Support

echo ========================================
echo    Fix Buildozer Android Support
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Uninstalling current Buildozer...
pip uninstall -y buildozer
echo.

echo [2/4] Installing compatible version (1.5.0)...
pip install buildozer==1.5.0
echo.

echo [3/4] Installing python-for-android...
pip install python-for-android
echo.

echo [4/4] Verifying installation...
echo.
buildozer --version
echo.
buildozer --help
echo.

echo ========================================
echo    Fix complete!
echo ========================================
echo.
echo Now you can run: build_apk_auto.bat
echo.
pause

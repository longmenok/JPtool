@echo off
chcp 65001 >nul
title 修复Buildozer Android支持

echo ========================================
echo    修复 Buildozer Android 支持
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 卸载当前 Buildozer
pip uninstall -y buildozer
echo.

echo [2/4] 安装兼容版本 (1.5.0)
pip install buildozer==1.5.0
echo.

echo [3/4] 安装 python-for-android
pip install python-for-android
echo.

echo [4/4] 验证安装
echo.
buildozer --version
echo.
buildozer --help
echo.

echo ========================================
echo    修复完成！
echo ========================================
echo.
echo 现在可以尝试运行: build_apk_auto.bat
echo.
pause

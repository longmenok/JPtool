# Android APK 编译指南

## 当前环境状态

### ✅ 已安装
- Android SDK (E:\Android Studio\sdk)
  - Build Tools 14
  - Platform Android 14
  - Platform Tools
  - SDK Manager

### ❌ 需要安装

#### 1. Java JDK (必需)

**下载地址：** https://adoptium.net/temurin/releases/?version=11

**推荐版本：** Eclipse Temurin 11 LTS (JDK 11)

**安装步骤：**
1. 下载 Windows x64 JDK 11
2. 运行安装程序
3. 记住安装路径 (例如: C:\Program Files\Eclipse Adoptium\jdk-11.0.21.9-hotspot)
4. 安装完成后，Java会自动配置到PATH

**验证安装：**
```bash
java -version
javac -version
```

#### 2. Android NDK (推荐，用于编译Python原生代码)

**方法A：使用SDK Manager**
```bash
cd "E:\Android Studio\sdk\tools\bin"
sdkmanager "ndk;25.2.9519653"
```

**方法B：直接下载**
- 下载地址：https://developer.android.com/ndk/downloads/
- 选择 Windows 64-bit (LLVM) 或 Windows 64-bit (MingWear)

---

## 编译步骤

### 方法一：使用图形界面（推荐新手）

1. **安装Java JDK 11**
   - 访问 https://adoptium.net/temurin/releases/?version=11
   - 下载并安装 Windows x64 JDK

2. **双击运行 "安装NDK.bat"**
   - 这会自动下载并安装 Android NDK

3. **双击运行 "编译APK.bat"**
   - 等待编译完成
   - APK会生成在 bin\ 目录

### 方法二：使用命令行

```bash
# 1. 设置环境变量 (在命令行中)
set ANDROID_HOME=E:\Android Studio\sdk
set ANDROID_SDK_ROOT=E:\Android Studio\sdk
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.21.9-hotspot

# 2. 编译APK
cd 项目目录
buildozer android debug
```

---

## 常见问题

### Q1: "ANDROID_HOME" 未设置
**解决：** 运行 "编译APK.bat" 脚本，它会自动设置环境变量

### Q2: "JAVA_HOME" 未设置
**解决：** 安装Java JDK 11，并确保 JAVA_HOME 指向JDK安装目录

### Q3: Buildozer下载依赖太慢
**解决：** 使用国内镜像源
```bash
pip install buildozer -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: NDK下载失败
**解决：** 
1. 使用VPN或代理
2. 或手动下载NDK并解压到 `E:\Android Studio\sdk\ndk\` 目录

### Q5: 编译时间太长
**解决：** 
- 首次编译需要下载大量依赖，约10-30分钟
- 后续编译会快很多（因为依赖已缓存）

---

## 替代方案（无需配置环境）

如果环境配置太复杂，可以使用以下在线服务：

1. **FynMan** (https://fynman.com/)
   - 免费在线Python打包
   - 上传代码即可

2. **Google Colab**
   - 使用云端Python环境
   - 配置简单

---

## 编译产物

成功编译后，APK文件位于：
```
项目目录\bin\metronome-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

可以直接安装到Android手机测试！

---

## 文件清单

- `编译APK.bat` - 一键编译脚本（双击运行）
- `安装NDK.bat` - NDK自动安装脚本
- `README_编译指南.md` - 本文档
- `main.py` - 手机版应用代码
- `buildozer.spec` - Buildozer配置文件
# 节拍器APK打包指南

## 🚨 问题诊断

当前 Buildozer 1.6.0 只有 iOS 支持，没有 Android 目标！

---

## 🔧 方案1：修复 Buildozer（推荐）

### 步骤1：运行修复脚本
双击运行：`fix_buildozer.bat`

这个脚本会：
1. 卸载当前 Buildozer 1.6.0
2. 安装兼容的 Buildozer 1.5.0
3. 安装 python-for-android
4. 验证安装

### 步骤2：运行打包
修复完成后，运行：`build_apk_auto.bat`

---

## 🛡️ 方案2：使用 Python-for-Android 直接打包（备选）

如果方案1有问题，可以使用 p4a 直接打包：

```bash
# 安装依赖
pip install python-for-android cython

# 创建构建命令
p4a apk --package=org.metronome.metronome \
    --name="节拍器" \
    --version=0.1 \
    --bootstrap=sdl2 \
    --requirements=python3,kivy,numpy \
    --window \
    --icon=icon.png \
    --presplash=presplash.png \
    --sdk-dir="E:\Android SDK\sdk" \
    --ndk-dir="E:\Android SDK\sdk\ndk" \
    --android-api=33 \
    --ndk-api=24 \
    --add-assets=sounds/
```

---

## 📋 当前环境检查

| 组件 | 状态 | 版本 |
|------|------|------|
| Java JDK | ✅ | 17.0.19 |
| Android SDK | ✅ | E:\Android SDK\sdk |
| Android NDK | ✅ | 25.1.8937393 |
| Buildozer | ⚠️ | 1.6.0 (需要降级) |

---

## 📝 注意事项

1. **首次打包时间**：30-60分钟
2. **网络要求**：稳定网络，需要下载1-2GB依赖
3. **磁盘空间**：至少10GB可用空间
4. **杀毒软件**：可能需要临时关闭或添加信任

---

## 🔄 如果还是失败

尝试使用在线构建服务：
- GitHub Actions
- GitLab CI
- 或者使用 Kivy Launcher 直接在手机上测试

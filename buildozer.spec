[app]

title = 节拍器
package.name = metronome
package.domain = org.metronome
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,ogg,mp3
version = 0.1

android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b

requirements = python3,kivy,numpy

fullscreen = 0
android.backup = False
android.ndk_arch = armeabi-v7a

android.add_assets = sounds/

[buildozer]
log_level = 2

[app:android]
android.accept_sdk_license = True

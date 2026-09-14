[app]
title = PyWiFi Scanner
package.name = pywifiscanner
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ⚠️ 关键依赖：必须包含 pywifi 和 android 权限库
requirements = python3,kivy,pywifi,android

# ⚠️ 关键权限：缺少这些 APP 会闪退或无法扫描
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,INTERNET

# ⚠️ Android API 版本：pywifi 需要较新的 API
android.api = 31
android.minapi = 24
android.targetapi = 33

# 编译选项
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
log_level = 2
warn_on_root = 0

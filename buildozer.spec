[app]
title = PyWiFi Scanner
package.name = pywifiscanner
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 只保留 python3 和 kivy，pyjnius 和 android 会由 p4a 自动处理
requirements = python3,kivy

# 权限保持不变
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,INTERNET

# API 版本建议统一，避免兼容问题
android.api = 33
android.minapi = 24
android.targetapi = 33

android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
log_level = 2
warn_on_root = 0

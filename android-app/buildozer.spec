[app]
title = Daily Rise
package.name = dailyrise
package.domain = org.dailyrise

source.dir = .
source.include_exts = py,html,css,js,svg,json,db
source.exclude_exts = pyc,pyo,pyd

orientation = portrait

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

version = 0.1

requirements = python3,kivy==2.2.1,requests,urllib3

android.add_aars =
android.add_jars =

android.entrypoint = org.kivy.android.PythonActivity

p4a.source_dir =
p4a.branch = master

[buildozer]
profile = default
warn_on_root = 0

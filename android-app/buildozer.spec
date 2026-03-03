[app]
title = Daily Rise
package.name = dailyrise
package.domain = org.dailyrise

source.dir = ../app
source.include_exts = py,png,jpg,kv,html,css,js,svg,json,db
source.exclude_exts = pyc,pyo,pyd

orientation = portrait

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a

# Требования Python
requirements = python3,kivy==2.2.1,fastapi,uvicorn,sqlalchemy,aiosqlite,pydantic,pydantic-settings,jwt,cryptography

android.add_aars =
android.add_jars =

android.entrypoint = org.kivy.android.PythonActivity

p4a.source_dir =
p4a.branch = master

[buildozer]
profile = default
warn_on_root = 0

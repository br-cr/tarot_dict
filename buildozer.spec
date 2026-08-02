[app]

# (str) Title of your application
title = Tarot Dict

# (str) Package name
package.name = tarotdict

# (str) Package domain (needed for android/ios packaging)
package.domain = org.rcampos

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,json,ttf

# (list) List of directory to exclude
source.exclude_dirs = bin, .buildozer, .github, .git, __pycache__, src/__pycache__, venv, .venv

# (list) List of exclusions using pattern matching
source.exclude_patterns = .DS_Store, */.DS_Store, *.pyc, *.pyo

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.0

# (str) Rama/tag de python-for-android
# Fijado para evitar que buildozer use master y cambie
# de versión de Python/p4a inesperadamente.
p4a.branch = v2024.01.21


# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Minimum NDK API
android.ndk_api = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android build tools version
android.build_tools_version = 34.0.0

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (bool) If True, skip trying to update the Android sdk
android.skip_update = False

# (list) The Android arch to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 0
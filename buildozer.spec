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

# (list) List of directory to include
source.include_dirs = assets, src

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (str) Android build tools version (FIJADO para evitar el error de licencias en la v37)
# android.build_tools_version = 33.0.2

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version
# android.ndk = 25b

# (bool) If True, automatically accept SDK licenses
android.accept_sdk_licenses = True

# (bool) If True, skip trying to update the Android sdk
android.skip_update = False

# (list) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 0
[app]

# (str) Title of your application
title = Tarot Dict

# (str) Package name
package.name = tarotdict

# (str) Package domain (needed for android/ios packaging)
package.domain = org.rcampos

# (str) Source code where the main.py live
# IMPORTANTE: python-for-android exige un main.py EN ESTA CARPETA.
# El main.py de la raiz es un lanzador que importa src/main.py.
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,json,ttf

# (list) List of directory to exclude (let empty to not exclude anything)
# OJO: "source.include_dirs" NO existe en buildozer; con source.dir = . se
# incluye todo el arbol y lo que se hace es EXCLUIR lo que no debe ir al APK.
source.exclude_dirs = bin, .buildozer, .github, .git, __pycache__, src/__pycache__, venv, .venv

# (list) List of exclusions using pattern matching
source.exclude_patterns = .DS_Store, */.DS_Store, *.pyc, *.pyo

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.0

# (str) rama/tag de python-for-android a usar.
# CRITICO: por defecto buildozer NO usa una version publicada de p4a, clona
# 'master' de GitHub. O sea el build depende de lo que haya en master ESE DIA.
# Hoy master compila CPython 3.14, y el C que genera Cython 0.29.x para Kivy
# llama a _PyLong_AsByteArray con 5 argumentos cuando en 3.14 pasaron a ser 6
# -> "too few arguments to function call" y el build muere compilando kivy.
# Este tag trae CPython 3.11.5 + recipe de kivy 2.3.0 + NDK 25b, que es
# justo lo que declara este spec. NO quitar el pin: volveria a romperse solo.
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

# (int) Minimum NDK API (debe coincidir con minapi)
android.ndk_api = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android build tools version.
# FIJADO a proposito: si se deja vacio, buildozer instala la ultima disponible
# (36.x / 37.x preview) y el build revienta pidiendo licencias que no existen.
android.build_tools_version = 34.0.0

# (bool) If True, automatically accept SDK license
# OJO: la clave correcta es "accept_sdk_license" en SINGULAR. En plural
# buildozer la ignora sin avisar y el build se cuelga en el prompt de licencia.
android.accept_sdk_license = True

# (bool) If True, skip trying to update the Android sdk
android.skip_update = False

# (list) The Android arch to build for
# Solo arm64-v8a: cubre practicamente todo dispositivo actual y evita duplicar
# el tiempo de compilacion en CI. Para publicar en Play, agregar armeabi-v7a.
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 0

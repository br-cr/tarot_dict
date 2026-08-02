# -*- coding: utf-8 -*-
"""Punto de entrada de la aplicacion.

python-for-android (el motor de buildozer) EXIGE que exista un main.py en la
raiz del proyecto, es decir en la carpeta apuntada por `source.dir` del
buildozer.spec. El codigo real de la app vive en src/main.py; este archivo solo
lo arranca.

En escritorio se puede seguir usando cualquiera de las dos formas:
    python main.py
    python -m src.main
"""
import os
import sys

# En Android el CWD no siempre es la carpeta de la app, y en escritorio se
# puede invocar desde otro directorio. Anclamos sys.path a la raiz real del
# proyecto para que `import src.*` funcione en ambos casos.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import TarotApp

if __name__ == "__main__":
    TarotApp().run()

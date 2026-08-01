# -*- coding: utf-8 -*-
"""
Construye el mapeo {nombre_de_carta: ruta_relativa_de_imagen}.

IMPORTANTE sobre el JSON real (tarot_78_cartas_extenso.json):
    arcanos_mayores = {
        "El Loco": {"derecho": "...", "invertido": "..."},
        "El Mago": {...},
        ...
    }
    arcanos_menores = {
        "Bastos": {"As de Bastos": {...}, "2 de Bastos": {...}, ...},
        "Copas": {...},
        ...
    }

No hay campos "nombre" ni "numero" dentro de cada carta: el nombre es la
clave del diccionario, y el número/orden de los Arcanos Mayores se deduce
de la posición (0..21) en la que aparecen. Esa era la causa de que antes
nunca se encontraran ni el nombre ni la imagen de cada carta.
"""

import os
import glob
import json

CARPETA_ASSETS_REL = os.path.join("assets", "cartas")

# Carpeta raíz del proyecto (padre de "src/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_ASSETS_ABS = os.path.join(BASE_DIR, CARPETA_ASSETS_REL)
JSON_PATH = os.path.join(BASE_DIR, "tarot_78_cartas_extenso.json")

EXTENSIONES_VALIDAS = (".jpg", ".jpeg", ".png", ".webp")

MAPEO_ARCHIVOS_MAYORES = {
    0: "major_arcana_fool",
    1: "major_arcana_magician",
    2: "major_arcana_priestess",
    3: "major_arcana_empress",
    4: "major_arcana_emperor",
    5: "major_arcana_hierophant",
    6: "major_arcana_lovers",
    7: "major_arcana_chariot",
    8: "major_arcana_strength",
    9: "major_arcana_hermit",
    10: "major_arcana_fortune",
    11: "major_arcana_justice",
    12: "major_arcana_hanged",
    13: "major_arcana_death",
    14: "major_arcana_temperance",
    15: "major_arcana_devil",
    16: "major_arcana_tower",
    17: "major_arcana_star",
    18: "major_arcana_moon",
    19: "major_arcana_sun",
    20: "major_arcana_judgement",
    21: "major_arcana_world",
}

# Prefijo del nombre de la carta menor -> sufijo de archivo
PREFIJO_A_SUFIJO_MENORES = {
    "as": "ace",
    "2": "2", "3": "3", "4": "4", "5": "5",
    "6": "6", "7": "7", "8": "8", "9": "9", "10": "10",
    "sota": "page",
    "caballo": "knight",
    "reina": "queen",
    "rey": "king",
}

PALO_A_SUITE_ARCHIVO = {
    "bastos": "wands",
    "copas": "cups",
    "espadas": "swords",
    "oros": "pentacles",
}


def _buscar_imagen_por_base(nombre_base):
    """Busca en assets/cartas un archivo que empiece con nombre_base,
    sin importar la extensión. Devuelve la ruta RELATIVA (desde BASE_DIR)
    si la encuentra, o "" si no existe nada."""
    if not os.path.isdir(CARPETA_ASSETS_ABS):
        return ""

    # 1) intento directo con extensiones conocidas (rápido)
    for ext in EXTENSIONES_VALIDAS:
        candidato = os.path.join(CARPETA_ASSETS_ABS, nombre_base + ext)
        if os.path.exists(candidato):
            return os.path.join(CARPETA_ASSETS_REL, nombre_base + ext)

    # 2) búsqueda flexible por si la extensión/mayúsculas difieren
    patron = os.path.join(CARPETA_ASSETS_ABS, nombre_base + ".*")
    coincidencias = glob.glob(patron)
    if coincidencias:
        archivo = os.path.basename(coincidencias[0])
        return os.path.join(CARPETA_ASSETS_REL, archivo)

    return ""


def _nombre_base_mayor(indice):
    return MAPEO_ARCHIVOS_MAYORES.get(indice)


def _nombre_base_menor(nombre_carta, palo_key):
    # "As de Bastos" -> prefijo "as"
    prefijo = nombre_carta.split(" de ")[0].strip().lower()
    sufijo = PREFIJO_A_SUFIJO_MENORES.get(prefijo)
    suite_archivo = PALO_A_SUITE_ARCHIVO.get(palo_key.lower())
    if not sufijo or not suite_archivo:
        return None
    return f"minor_arcana_{suite_archivo}_{sufijo}"


def construir_ruta_imagen():
    ruta_imagen = {}

    if not os.path.exists(JSON_PATH):
        print(f"⚠️ No se encontró el JSON en: {JSON_PATH}")
        return ruta_imagen

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Arcanos Mayores ---
    arcanos_mayores = data.get("arcanos_mayores", {})
    for indice, nombre_carta in enumerate(arcanos_mayores.keys()):
        nombre_base = _nombre_base_mayor(indice)
        if nombre_base:
            ruta_imagen[nombre_carta] = _buscar_imagen_por_base(nombre_base)

    # --- Arcanos Menores ---
    arcanos_menores = data.get("arcanos_menores", {})
    for palo_key, cartas in arcanos_menores.items():
        if not isinstance(cartas, dict):
            continue
        for nombre_carta in cartas.keys():
            nombre_base = _nombre_base_menor(nombre_carta, palo_key)
            if nombre_base:
                ruta_imagen[nombre_carta] = _buscar_imagen_por_base(nombre_base)

    return ruta_imagen


RUTA_IMAGEN = construir_ruta_imagen()

if __name__ == "__main__":
    encontradas = sum(1 for v in RUTA_IMAGEN.values() if v)
    print(f"Mapeo generado: {len(RUTA_IMAGEN)} cartas, {encontradas} con imagen encontrada en disco")
    for nombre, ruta in RUTA_IMAGEN.items():
        if not ruta:
            print(f"  ❌ Sin imagen: {nombre}")
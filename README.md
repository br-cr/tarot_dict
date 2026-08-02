# ✦ Diccionario Tarot

Aplicación móvil hecha con [Kivy](https://kivy.org/) que funciona como diccionario de referencia rápida para las 78 cartas del Tarot (22 Arcanos Mayores + 56 Arcanos Menores). Pensada para consulta personal: elegís una categoría, tocás una carta y ves su significado en derecho e invertido.

## Características

- **Grilla responsive**: el número de columnas se recalcula solo según el ancho real de pantalla (2 a 8 columnas), así se ve bien tanto en un celular chico como en una tablet.
- **5 categorías**: Mayores, Bastos, Copas, Espadas y Oros, con navegación tipo "chips" (píldoras horizontales).
- **Pantalla de detalle**: imagen de la carta, significado en derecho y en invertido, con botón atrás y soporte para el botón físico ATRÁS de Android.
- **Tema visual propio**: paleta violeta noche + dorado, tipografía DejaVu Sans embebida (no depende de fuentes del sistema).
- **Carga por lotes**: las cartas se insertan de a poco en la grilla para no trabar la UI al decodificar muchas imágenes de golpe.
- **100% offline**: todos los datos (JSON) y las imágenes viven empaquetados dentro de la app; no requiere conexión a internet.

## Estructura del proyecto

```
tarot_dict/
├── main.py                      # Punto de entrada que exige Buildozer (arranca src/main.py)
├── buildozer.spec               # Configuración de compilación para Android
├── tarot_78_cartas_extenso.json # Datos: nombre, significado derecho/invertido de las 78 cartas
├── assets/
│   ├── cartas/                  # Imágenes de las cartas (una por carta)
│   └── fonts/                   # DejaVu Sans (regular, bold, italic, bold-italic)
├── src/
│   ├── __init__.py
│   ├── main.py                  # App real: pantallas, layout, lógica
│   └── ruta_imagenes.py         # Mapea cada nombre de carta a su archivo de imagen
└── .github/workflows/
    └── build-apk.yml            # CI que compila el APK automáticamente
```

### Formato del JSON de datos

```json
{
  "arcanos_mayores": {
    "El Loco": { "derecho": "...", "invertido": "..." },
    "El Mago": { "derecho": "...", "invertido": "..." }
  },
  "arcanos_menores": {
    "Bastos": {
      "As de Bastos": { "derecho": "...", "invertido": "..." },
      "2 de Bastos": { "derecho": "...", "invertido": "..." }
    },
    "Copas": { "...": "..." },
    "Espadas": { "...": "..." },
    "Oros": { "...": "..." }
  }
}
```

El nombre de cada carta es la **clave** del diccionario (no hay un campo `"nombre"` separado). El número de los Arcanos Mayores se deduce de su posición en el JSON.

### Convención de nombres de imágenes (`assets/cartas/`)

`src/ruta_imagenes.py` busca cada imagen por un nombre de archivo derivado del nombre de la carta:

- Mayores: `major_arcana_fool.jpg`, `major_arcana_magician.jpg`, ... (según posición 0-21)
- Menores: `minor_arcana_{palo}_{valor}.jpg`, donde `palo` es `wands` / `cups` / `swords` / `pentacles`, y `valor` es `ace`, `2`...`10`, `page`, `knight`, `queen`, `rey`

Acepta `.jpg`, `.jpeg`, `.png` o `.webp` indistintamente.

## Correr en escritorio (desarrollo)

Requiere Python 3.10+ y Kivy instalado.

```bash
pip install kivy
python -m src.main
```

La ventana de previsualización se ajusta automáticamente al tamaño de tu monitor y se puede redimensionar para probar que la grilla responsive se reacomode.

## Compilar el APK

El proyecto usa [Buildozer](https://buildozer.readthedocs.io/) para empaquetar la app como APK de Android.

### Automático (recomendado): GitHub Actions

Cada `git push` a `main` dispara el workflow en `.github/workflows/build-apk.yml`, que compila el APK en un runner Linux limpio y lo deja disponible como artefacto descargable en la pestaña **Actions** del repo (sección *Artifacts* de la ejecución correspondiente).

### Manual (local, en Linux)

```bash
pip install buildozer cython==0.29.36
buildozer android debug
```

El APK queda en `bin/`.

> **Nota para usuarios de Mac / Windows:** Buildozer solo compila para Android en Linux. En Mac se puede usar Docker con la imagen `kivy/buildozer`, pero es más lento y menos estable que compilar en GitHub Actions — este repo está configurado para usar Actions por esa razón.

### Notas de compatibilidad (por si tocás la configuración)

- `buildozer.spec` fija `android.build_tools_version = 33.0.2` y `android.accept_sdk_license = True` — **ojo con el nombre exacto de esta última clave** (sin la "s" al final de "license"); con la "s" de más, Buildozer la ignora silenciosamente y el build falla por licencias no aceptadas.
- El workflow de CI usa `ubuntu-22.04` explícitamente (no `ubuntu-latest`), porque el NDK que usa Buildozer (r25b) no es compatible con la `glibc` más nueva de Ubuntu 24.04.
- El workflow fuerza un entorno virtual con Python 3.10 explícito, porque el runner trae otras versiones de Python instaladas que pueden interferir con subprocesos internos de Buildozer.
- Por ahora `android.archs = arm64-v8a` (cubre prácticamente todos los celulares Android modernos). `armeabi-v7a` (32 bits) se puede volver a agregar más adelante si hace falta soporte para equipos muy viejos.

## Editar cartas

1. Edita `tarot_78_cartas_extenso.json` siguiendo el formato de arriba.
2. Si es una carta nueva, agrega su imagen a `assets/cartas/` con el nombre de archivo correspondiente (ver convención más arriba).
3. No hace falta tocar el código: `src/main.py` y `src/ruta_imagenes.py` leen el JSON dinámicamente.

## Tech stack

- [Kivy](https://kivy.org/) — framework de UI
- [Buildozer](https://buildozer.readthedocs.io/) / [python-for-android](https://python-for-android.readthedocs.io/) — empaquetado a APK
- Python 3.10+

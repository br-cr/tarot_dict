# -*- coding: utf-8 -*-
import os
import json

# IMPORTANTE — nitidez en pantallas de escritorio de alta densidad (Retina):
# Kivy por defecto asume densidad=1 (1dp = 1px), así que en un Mac Retina
# termina renderizando a una resolución más baja de la real y luego el SO
# la estira, lo que se ve borroso. La forma correcta de arreglarlo es simular
# una densidad de pantalla real usando estas variables de entorno ANTES de
# importar kivy.
# OJO: esto es SOLO para escritorio. En Android el dispositivo reporta su
# densidad real y forzarla a 2 rompe el escalado en pantallas de densidad 3
# o 3.5 (todo se veria mas chico de lo debido). p4a define ANDROID_ARGUMENT
# en el entorno, asi que lo usamos para detectar que corremos en el APK.
EN_ANDROID = "ANDROID_ARGUMENT" in os.environ

if not EN_ANDROID:
    os.environ["KIVY_DPI"] = "320"
    os.environ["KIVY_METRICS_DENSITY"] = "2"

from kivy.config import Config

<<<<<<< HEAD

def _tamano_pantalla():
    """Tamaño del monitor en PUNTOS (las mismas unidades en las que se pide el
    tamaño de ventana), o None si no se puede averiguar.

    Se consulta con tkinter ANTES de que exista la ventana SDL para no mezclar
    los dos toolkits. Es solo para escritorio; en el APK nunca se llama.
    """
    try:
        import tkinter
        raiz = tkinter.Tk()
        raiz.withdraw()
        medidas = (raiz.winfo_screenwidth(), raiz.winfo_screenheight())
        raiz.destroy()
        return medidas
    except Exception:
        return None


_PANTALLA = _tamano_pantalla() if not EN_ANDROID else None

if not EN_ANDROID:
    # Ventana de previsualizacion con forma de celular, medida en PUNTOS de
    # pantalla (la misma unidad que reporta el monitor).
    #
    # POR QUE SE RECORTA CONTRA LA PANTALLA: pedir una ventana mas grande que
    # el monitor NO la achica; el SO la crea igual y deja el sobrante fuera de
    # la pantalla. Un celular tiene ~780 dp de alto, que en un Mac Retina son
    # ~1560 px: mas del doble que una laptop. Por eso el layout se veia cortado.
    _ancho_preview, _alto_preview = 400, 820
    if _PANTALLA:
        _ancho_preview = min(_ancho_preview, int(_PANTALLA[0] * 0.90))
        _alto_preview = min(_alto_preview, int(_PANTALLA[1] * 0.85))

    Config.set("graphics", "width", str(_ancho_preview))
    Config.set("graphics", "height", str(_alto_preview))
    Config.set("graphics", "resizable", "1")
    # Minimo bajo a proposito: permite encoger la ventana para comprobar que la
    # grilla se reacomoda (es la forma de probar el diseño responsive en Mac).
    Config.set("graphics", "minimum_width", "360")
    Config.set("graphics", "minimum_height", "520")
=======
if not EN_ANDROID:
    # 720x1440 px reales = 360x720 dp logicos: proporcion 18:9, la de un
    # celular actual. El layout NO depende de este tamaño (es responsive),
    # esto es solo la ventana de previsualizacion en escritorio.
    Config.set("graphics", "width", "720")
    Config.set("graphics", "height", "1440")
    Config.set("graphics", "resizable", "1")
    # Minimo bajo a proposito: permite encoger la ventana para comprobar que la
    # grilla se reacomoda (es la forma de probar el diseño responsive en Mac).
    Config.set("graphics", "minimum_width", "400")
    Config.set("graphics", "minimum_height", "640")
>>>>>>> cf5b367a9b80dd4f40a5f3637d249835c7a3f8e1

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView


# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
COLOR_FONDO = (0.055, 0.043, 0.094, 1)          # violeta noche
COLOR_SUP = (0.106, 0.086, 0.161, 1)            # superficie (tarjetas)
COLOR_SUP_ALTA = (0.157, 0.129, 0.231, 1)       # superficie presionada
COLOR_BORDE = (0.83, 0.70, 0.33, 0.30)
COLOR_DORADO = (0.83, 0.70, 0.33, 1)
COLOR_TEXTO = (0.94, 0.93, 0.97, 1)
COLOR_TEXTO_TENUE = (0.62, 0.59, 0.69, 1)
COLOR_DERECHO = (0.42, 0.83, 0.55, 1)
COLOR_INVERTIDO = (0.93, 0.47, 0.47, 1)

Window.clearcolor = COLOR_FONDO

# Importamos el mapeo dinámico de imágenes
from src.ruta_imagenes import RUTA_IMAGEN, BASE_DIR, JSON_PATH


# ---------------------------------------------------------------------------
# Tipografia: DejaVu Sans desde assets/fonts
# ---------------------------------------------------------------------------
# Se registran las 4 variantes como UNA familia, para que bold/italic salgan
# del archivo correcto en vez de que Kivy los "falsee" deformando la regular.
DIR_FUENTES = os.path.join(BASE_DIR, "assets", "fonts")

_VARIANTES = {
    "fn_regular": os.path.join(DIR_FUENTES, "DejaVuSans.ttf"),
    "fn_bold": os.path.join(DIR_FUENTES, "DejaVuSans-Bold.ttf"),
    "fn_italic": os.path.join(DIR_FUENTES, "DejaVuSans-Oblique.ttf"),
    "fn_bolditalic": os.path.join(DIR_FUENTES, "DejaVuSans-BoldOblique.ttf"),
}

if all(os.path.exists(ruta) for ruta in _VARIANTES.values()):
    LabelBase.register(name="Tarot", **_VARIANTES)
    # Ademas pisamos el default de Kivy ("Roboto"), asi cualquier widget que no
    # declare font_name tambien queda con DejaVu y no hay mezcla de tipografias.
    LabelBase.register(name="Roboto", **_VARIANTES)
    FUENTE = "Tarot"
else:
    print("[aviso] No se encontraron las fuentes en assets/fonts; se usa la de Kivy.")
    FUENTE = "Roboto"


# ---------------------------------------------------------------------------
# Metricas del layout responsive
# ---------------------------------------------------------------------------
# Los JPG de las cartas miden ~405x700 px -> alto/ancho = 1.73. Usar el ratio
# real evita que la grilla deje franjas vacias o recorte la ilustracion.
RATIO_CARTA = 1.73

# Ancho objetivo por carta. Calibrado para que cualquier telefono actual
# (360-430 dp de ancho) caiga en 3 columnas, y tablets/escritorio crezcan solos.
ANCHO_TILE_IDEAL = dp(110)
MIN_COLUMNAS = 2
MAX_COLUMNAS = 8
<<<<<<< HEAD
ALTO_ETIQUETA = dp(32)       # espacio del nombre bajo cada carta (2 lineas)
# 60 y no 56: la barra del detalle apila titulo (17sp) + subtitulo (11sp), y con
# 56 dp menos el padding quedaban 20 dp por linea, que recorta el titulo.
ALTO_BARRA = dp(60)
=======
ALTO_ETIQUETA = dp(30)       # espacio del nombre bajo cada carta (2 lineas)
ALTO_BARRA = dp(56)
>>>>>>> cf5b367a9b80dd4f40a5f3637d249835c7a3f8e1
TOQUE_MINIMO = dp(48)        # area tactil minima recomendada en movil

# Solo simbolos presentes en DejaVu Sans. Los emoji tipo U+1F52E NO estan en
# esta familia y saldrian como cuadro vacio en el APK.
ICONO_CATEGORIA = {
    "Mayores": "✦",
    "Bastos": "♣",
    "Copas": "♥",
    "Espadas": "♠",
    "Oros": "♦",
}
ICONO_SIN_IMAGEN = "✦"


# ---------------------------------------------------------------------------
# Reglas KV
# ---------------------------------------------------------------------------
# Se interpolan los colores con f-string porque KV no ve las variables globales
# de este modulo (solo lo importado con #:import).
KV = f"""
<Chip@ButtonBehavior+BoxLayout>:
    activo: False
    texto: ""
    size_hint: None, None
    height: dp(38)
    width: max(dp(74), etiqueta.texture_size[0] + dp(28))
    canvas.before:
        Color:
            rgba: {COLOR_DORADO} if self.activo else ({COLOR_SUP_ALTA} if self.state == 'down' else {COLOR_SUP})
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height / 2.0]
        Color:
            rgba: (0, 0, 0, 0) if self.activo else {COLOR_BORDE}
        Line:
            rounded_rectangle: (self.x + 1, self.y + 1, self.width - 2, self.height - 2, self.height / 2.0)
            width: 1
    Label:
        id: etiqueta
        text: root.texto
        font_name: '{FUENTE}'
        font_size: '13sp'
        bold: root.activo
        color: {COLOR_FONDO} if root.activo else {COLOR_TEXTO_TENUE}

<BotonIcono@ButtonBehavior+BoxLayout>:
    texto: ""
    size_hint: None, None
    size: dp(44), dp(44)
    canvas.before:
        Color:
            rgba: {COLOR_SUP_ALTA} if self.state == 'down' else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(22)]
    Label:
        text: root.texto
        font_name: '{FUENTE}'
        font_size: '24sp'
        color: {COLOR_DORADO}

<Panel@BoxLayout>:
    canvas.before:
        Color:
            rgba: {COLOR_SUP}
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

<MarcoImagen@BoxLayout>:
    canvas.before:
        Color:
            rgba: {COLOR_DORADO}
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]

<CardTile>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: {COLOR_SUP_ALTA} if self.state == 'down' else {COLOR_SUP}
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: {COLOR_BORDE}
        Line:
            rounded_rectangle: (self.x + 1, self.y + 1, self.width - 2, self.height - 2, dp(12))
            width: 1
"""
Builder.load_string(KV)


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
def resolver_ruta_abs(ruta_relativa):
    """RUTA_IMAGEN ya guarda rutas relativas verificadas contra disco;
    si viene vacía, no hay imagen disponible para esa carta."""
    if not ruta_relativa:
        return ""
    abs_path = os.path.join(BASE_DIR, ruta_relativa)
    return abs_path if os.path.exists(abs_path) else ""


def cargar_y_organizar_datos():
    """
    Lee tarot_78_cartas_extenso.json con su estructura REAL:

        arcanos_mayores: { "El Loco": {"derecho": .., "invertido": ..}, ... }
        arcanos_menores: { "Bastos": { "As de Bastos": {...}, ... }, ... }

    (no hay "nombre"/"numero" anidados: el nombre es la clave del diccionario
    y el orden define el número).
    """
    if not os.path.exists(JSON_PATH):
        print(f"[ERROR] No se encontro el JSON en: {JSON_PATH}")
        return {}

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    categorias = {
        "Mayores": [],
        "Bastos": [],
        "Copas": [],
        "Espadas": [],
        "Oros": [],
    }

    # 1. Arcanos Mayores
    arcanos_mayores = data.get("arcanos_mayores", {})
    for indice, (nombre, significado) in enumerate(arcanos_mayores.items()):
        if not isinstance(significado, dict):
            continue
        categorias["Mayores"].append({
            "nombre": nombre,
            "subtitulo": f"Arcano Mayor {indice}",
            "derecho": significado.get("derecho", "Sin texto derecho"),
            "invertido": significado.get("invertido", "Sin texto invertido"),
            "imagen": resolver_ruta_abs(RUTA_IMAGEN.get(nombre, "")),
        })

    # 2. Arcanos Menores
    arcanos_menores = data.get("arcanos_menores", {})
    for palo, cartas in arcanos_menores.items():
        cat_nombre = palo if palo in categorias else palo.capitalize()
        if not isinstance(cartas, dict) or cat_nombre not in categorias:
            continue
        for nombre, significado in cartas.items():
            if not isinstance(significado, dict):
                continue
            categorias[cat_nombre].append({
                "nombre": nombre,
                "subtitulo": f"Arcano Menor · {cat_nombre}",
                "derecho": significado.get("derecho", "Sin texto derecho"),
                "invertido": significado.get("invertido", "Sin texto invertido"),
                "imagen": resolver_ruta_abs(RUTA_IMAGEN.get(nombre, "")),
            })

    total = sum(len(v) for v in categorias.values())
    con_imagen = sum(1 for lista in categorias.values() for c in lista if c["imagen"])
    print("\n==========================================")
    print(f"CARTAS CARGADAS: {total} de 78  |  con imagen: {con_imagen}")
    for cat, lista in categorias.items():
        print(f" - {cat}: {len(lista)} cartas")
    print("==========================================\n")

    return categorias


DATOS_TAROT = cargar_y_organizar_datos()
TOTAL_CARTAS = sum(len(v) for v in DATOS_TAROT.values())


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------
class CardTile(ButtonBehavior, BoxLayout):
    """Tarjeta de la grilla. Su ALTO se deriva del ancho que le asigne el
    GridLayout, usando el aspect ratio real de la ilustracion. Asi la grilla
    se adapta sola a cualquier ancho de pantalla sin numeros magicos."""

    def __init__(self, carta, al_tocar, **kwargs):
        super().__init__(orientation="vertical", padding=dp(6), spacing=dp(4),
                         size_hint_y=None, height=dp(180), **kwargs)
        self.carta = carta

        ruta = carta["imagen"]
        if ruta:
            self.visual = Image(source=ruta, size_hint_y=None,
                                fit_mode="contain", mipmap=True)
        else:
            # Marcador de posicion con un simbolo que SI existe en DejaVu.
            self.visual = Label(text=ICONO_SIN_IMAGEN, font_name=FUENTE,
                                font_size="30sp", size_hint_y=None,
                                color=COLOR_TEXTO_TENUE)
        self.add_widget(self.visual)

        self.etiqueta = Label(
            text=carta["nombre"],
            size_hint_y=None,
            height=ALTO_ETIQUETA,
            font_name=FUENTE,
            font_size="11sp",
            color=COLOR_TEXTO,
            halign="center",
            valign="middle",
            max_lines=2,
            shorten=True,
            shorten_from="right",
        )
        self.etiqueta.bind(width=lambda inst, val: setattr(inst, "text_size",
                                                           (val, ALTO_ETIQUETA)))
        self.add_widget(self.etiqueta)

        self.bind(width=self._recalcular_alto)
        self.bind(on_release=lambda *_: al_tocar(carta))
        self._recalcular_alto()

    def _recalcular_alto(self, *_):
        ancho_util = max(dp(1), self.width - self.padding[0] - self.padding[2])
        alto_imagen = ancho_util * RATIO_CARTA
        self.visual.height = alto_imagen
        self.height = (alto_imagen + ALTO_ETIQUETA + self.spacing
                       + self.padding[1] + self.padding[3])


class BarraSuperior(BoxLayout):
    """App bar fija, patron estandar en apps moviles."""

    def __init__(self, **kwargs):
        kwargs.setdefault("padding", (dp(14), 0))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(orientation="horizontal", size_hint_y=None,
                         height=ALTO_BARRA, **kwargs)


# ---------------------------------------------------------------------------
# Pantalla 1: grilla
# ---------------------------------------------------------------------------
class GridScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.categoria_actual = "Mayores"
        self.chips = {}
        self._evento_carga = None
        self._pendientes = []

        raiz = BoxLayout(orientation="vertical")

        # --- App bar ---
        barra = BarraSuperior()
        titulo = Label(
            text="✦  Diccionario Tarot",
            font_name=FUENTE,
            font_size="18sp",
            bold=True,
            color=COLOR_DORADO,
            halign="left",
            valign="middle",
        )
        titulo.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        barra.add_widget(titulo)

        self.lbl_contador = Label(
            text=f"{TOTAL_CARTAS}",
            size_hint_x=None,
            width=dp(46),
            font_name=FUENTE,
            font_size="12sp",
            color=COLOR_TEXTO_TENUE,
            halign="right",
            valign="middle",
        )
        self.lbl_contador.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        barra.add_widget(self.lbl_contador)
        raiz.add_widget(barra)

        # --- Chips de categoria (scroll horizontal, tipo pildora) ---
        chips_scroll = ScrollView(size_hint_y=None, height=dp(50),
                                  do_scroll_x=True, do_scroll_y=False,
                                  bar_width=0)
        self.fila_chips = BoxLayout(orientation="horizontal", size_hint_x=None,
                                    spacing=dp(8), padding=(dp(14), dp(6)))
        self.fila_chips.bind(minimum_width=self.fila_chips.setter("width"))

        from kivy.factory import Factory
        for categoria in DATOS_TAROT.keys():
            chip = Factory.Chip()
            chip.texto = f"{ICONO_CATEGORIA.get(categoria, '')} {categoria}".strip()
            chip.activo = (categoria == self.categoria_actual)
            chip.bind(on_release=lambda inst, c=categoria: self.cambiar_categoria(c))
            self.chips[categoria] = chip
            self.fila_chips.add_widget(chip)

        chips_scroll.add_widget(self.fila_chips)
        raiz.add_widget(chips_scroll)

        # --- Grilla responsive ---
        self.scroll_grid = ScrollView(size_hint_y=1, bar_width=dp(3),
                                      bar_color=COLOR_BORDE,
                                      bar_inactive_color=(0, 0, 0, 0))
        self.grid = GridLayout(cols=MIN_COLUMNAS, spacing=dp(10),
                               padding=(dp(14), dp(8), dp(14), dp(20)),
                               size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.grid.bind(width=self._ajustar_columnas)
        self.scroll_grid.add_widget(self.grid)
        raiz.add_widget(self.scroll_grid)

        self.add_widget(raiz)
        self.poblar_grid(self.categoria_actual)

    # -- responsive: el numero de columnas sale del ancho real disponible ----
    def _ajustar_columnas(self, *_):
        espacio = self.grid.spacing[0]
        disponible = self.grid.width - self.grid.padding[0] - self.grid.padding[2]
        # +0.5 = redondeo al entero mas cercano en vez de truncar: sin esto un
        # ancho de 2.9 columnas mostraria solo 2 y dejaria las cartas gigantes.
        columnas = int((disponible + espacio) / (ANCHO_TILE_IDEAL + espacio) + 0.5)
        columnas = max(MIN_COLUMNAS, min(MAX_COLUMNAS, columnas))
        if columnas != self.grid.cols:
            self.grid.cols = columnas

    def cambiar_categoria(self, categoria):
        if categoria == self.categoria_actual:
            return
        self.chips[self.categoria_actual].activo = False
        self.categoria_actual = categoria
        self.chips[categoria].activo = True
        self.poblar_grid(categoria)

    def poblar_grid(self, categoria):
        """Inserta las tarjetas por lotes (unas pocas por frame). Decodificar
        22 JPEG de golpe congela ~1s en un Android de gama baja; asi la UI
        responde de inmediato y la grilla se completa sola."""
        if self._evento_carga is not None:
            self._evento_carga.cancel()
            self._evento_carga = None

        self.grid.clear_widgets()
        self.scroll_grid.scroll_y = 1

        cartas = DATOS_TAROT.get(categoria, [])
        self.lbl_contador.text = f"{len(cartas)}"
        self._pendientes = list(cartas)
        self._evento_carga = Clock.schedule_interval(self._insertar_lote, 0)

    def _insertar_lote(self, _dt, tamano=6):
        for _ in range(tamano):
            if not self._pendientes:
                self._evento_carga = None
                return False
            self.grid.add_widget(CardTile(self._pendientes.pop(0), self.ver_detalle))
        return True

    def ver_detalle(self, carta):
        pantalla = self.manager.get_screen("detail")
        pantalla.actualizar_carta(carta)
        self.manager.transition.direction = "left"
        self.manager.current = "detail"


# ---------------------------------------------------------------------------
# Pantalla 2: detalle
# ---------------------------------------------------------------------------
class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from kivy.factory import Factory

        raiz = BoxLayout(orientation="vertical")

        # --- App bar con boton atras ---
        barra = BarraSuperior(padding=(dp(6), 0))
        btn_volver = Factory.BotonIcono()
        btn_volver.texto = "‹"          # ‹
        btn_volver.size = (TOQUE_MINIMO, TOQUE_MINIMO)
        btn_volver.bind(on_release=self.volver_grilla)
        barra.add_widget(btn_volver)

<<<<<<< HEAD
        cabecera_txt = BoxLayout(orientation="vertical", padding=(dp(4), dp(5)))
        self.lbl_titulo = Label(
            text="", font_name=FUENTE, font_size="17sp", bold=True,
            color=COLOR_DORADO, halign="left", valign="bottom",
            shorten=True, shorten_from="right", size_hint_y=0.58,
=======
        cabecera_txt = BoxLayout(orientation="vertical", padding=(dp(4), dp(8)))
        self.lbl_titulo = Label(
            text="", font_name=FUENTE, font_size="17sp", bold=True,
            color=COLOR_DORADO, halign="left", valign="bottom",
            shorten=True, shorten_from="right",
>>>>>>> cf5b367a9b80dd4f40a5f3637d249835c7a3f8e1
        )
        self.lbl_titulo.bind(size=lambda i, v: setattr(i, "text_size", v))
        self.lbl_subtitulo = Label(
            text="", font_name=FUENTE, font_size="11sp",
            color=COLOR_TEXTO_TENUE, halign="left", valign="top",
<<<<<<< HEAD
            size_hint_y=0.42,
=======
>>>>>>> cf5b367a9b80dd4f40a5f3637d249835c7a3f8e1
        )
        self.lbl_subtitulo.bind(size=lambda i, v: setattr(i, "text_size", v))
        cabecera_txt.add_widget(self.lbl_titulo)
        cabecera_txt.add_widget(self.lbl_subtitulo)
        barra.add_widget(cabecera_txt)
        raiz.add_widget(barra)

        # --- Contenido: TODO scrollea junto (patron movil) ---
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True,
                            bar_width=dp(3), bar_color=COLOR_BORDE,
                            bar_inactive_color=(0, 0, 0, 0))
        self.contenido = BoxLayout(orientation="vertical", size_hint_y=None,
                                   padding=(dp(14), dp(10), dp(14), dp(24)),
                                   spacing=dp(14))
        self.contenido.bind(minimum_height=self.contenido.setter("height"))

        # Imagen centrada con marco dorado, dimensionada de forma responsive
        centro = AnchorLayout(anchor_x="center", size_hint_y=None)
        self.marco = Factory.MarcoImagen(size_hint=(None, None), padding=dp(3))
        self.img_carta = Image(fit_mode="contain", mipmap=True)
        self.marco.add_widget(self.img_carta)
        centro.add_widget(self.marco)
        self.centro = centro
        self.contenido.add_widget(centro)

        self.contenido.add_widget(
            self._crear_bloque("↑  Derecho", COLOR_DERECHO, "lbl_derecho"))
        self.contenido.add_widget(
            self._crear_bloque("↓  Invertido", COLOR_INVERTIDO, "lbl_invertido"))

        scroll.add_widget(self.contenido)
        self.scroll = scroll
        raiz.add_widget(scroll)
        self.add_widget(raiz)

        # El tamaño de la imagen depende del ancho Y del alto de la ventana:
        # en pantallas bajas se achica para que el texto no quede empujado
        # fuera de la vista al abrir la carta.
        self.bind(size=self._redimensionar_imagen)
        self._redimensionar_imagen()

    def _redimensionar_imagen(self, *_):
        ancho_disp = max(dp(80), self.width - dp(28))
        # 62% del ancho, pero nunca mas alto que el 40% de la pantalla
        ancho = min(ancho_disp * 0.62, dp(240))
        ancho = min(ancho, (self.height * 0.40) / RATIO_CARTA)
        ancho = max(dp(90), ancho)
        alto = ancho * RATIO_CARTA
        self.marco.size = (ancho + dp(6), alto + dp(6))
        self.centro.height = alto + dp(6)

    def _crear_bloque(self, titulo_texto, color, attr_lbl):
        from kivy.factory import Factory

        panel = Factory.Panel(orientation="vertical", size_hint_y=None,
                              padding=(dp(14), dp(12)), spacing=dp(6))
        panel.bind(minimum_height=panel.setter("height"))

        titulo = Label(
            text=titulo_texto, size_hint_y=None, height=dp(20),
            font_name=FUENTE, font_size="13sp", bold=True, color=color,
            halign="left", valign="middle",
        )
        titulo.bind(size=lambda i, v: setattr(i, "text_size", v))
        panel.add_widget(titulo)

        cuerpo = Label(
            text="", size_hint_y=None, font_name=FUENTE, font_size="13sp",
            color=COLOR_TEXTO, halign="left", valign="top", line_height=1.35,
        )
        # text_size solo con ancho fijo -> el texto hace wrap; la altura la
        # dicta la textura resultante. Es lo que hace que el bloque crezca
        # solo, sin importar el largo del significado ni el ancho de pantalla.
        cuerpo.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        cuerpo.bind(texture_size=lambda i, v: setattr(i, "height", v[1]))
        panel.add_widget(cuerpo)
        setattr(self, attr_lbl, cuerpo)

        return panel

    def actualizar_carta(self, carta):
        self.lbl_titulo.text = carta["nombre"]
        self.lbl_subtitulo.text = carta.get("subtitulo", "")
        self.img_carta.source = carta["imagen"] or ""
        self.lbl_derecho.text = carta["derecho"]
        self.lbl_invertido.text = carta["invertido"]
        # Cada carta se abre desde arriba, no donde quedo la anterior.
        Clock.schedule_once(lambda *_: setattr(self.scroll, "scroll_y", 1), 0)

    def volver_grilla(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "grid"


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
class TarotApp(App):
    def build(self):
        self.title = "Diccionario Tarot"
        self.sm = ScreenManager(
            transition=SlideTransition(duration=0.20, direction="left"))
        self.sm.add_widget(GridScreen(name="grid"))
        self.sm.add_widget(DetailScreen(name="detail"))
        Window.bind(on_keyboard=self._tecla)
        return self.sm

    def _tecla(self, _window, key, *_args):
        """Boton fisico ATRAS de Android (llega como key 27, igual que ESC).
        Sin esto, tocar atras en el detalle cierra la app en vez de volver."""
        if key == 27 and self.sm.current != "grid":
            self.sm.transition.direction = "right"
            self.sm.current = "grid"
            return True
        return False


# El arranque en el APK lo hace main.py de la raiz (lo exige python-for-android).
# Esta guarda permite ademas lanzarlo en escritorio con `python -m src.main`.
if __name__ == "__main__":
    TarotApp().run()

# -*- coding: utf-8 -*-
import os
import json

# IMPORTANTE — nitidez en pantallas de escritorio de alta densidad (Retina):
# Kivy por defecto asume densidad=1 (1dp = 1px), así que en un Mac Retina
# termina renderizando a una resolución más baja de la real y luego el SO
# la estira, lo que se ve borroso. La forma correcta de arreglarlo (según
# la propia documentación de Kivy) es simular una densidad de pantalla
# real, como la de un celular de gama media/alta, usando estas variables
# de entorno ANTES de importar kivy. El layout lógico (360x640 "dp") se
# mantiene igual, pero se dibuja con más píxeles reales -> más nítido.
# En el APK real (Android) esto no hace falta: el propio dispositivo ya
# reporta su densidad real y Kivy la usa automáticamente.
os.environ["KIVY_DPI"] = "320"
os.environ["KIVY_METRICS_DENSITY"] = "2"

# La ventana de escritorio es redimensionable por defecto en Kivy. Si se
# arrastra/agranda durante las pruebas, Kivy puede además "recordar" ese
# tamaño en ~/.kivy/config.ini y reabrir la app así la próxima vez, aunque
# el código diga otra cosa. Fijamos el tamaño y desactivamos el resize
# ANTES de importar Window, para simular de forma fiel y estable una
# pantalla de celular. El tamaño ahora es el doble en píxeles reales
# (720x1280) porque la densidad simulada también se duplicó (2x), así que
# el layout se ve exactamente igual de "grande" en pantalla, solo que más
# nítido.
from kivy.config import Config
Config.set("graphics", "width", "720")
Config.set("graphics", "height", "1280")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.button import Button

# Redundante pero inofensivo: refuerza el tamaño fijo tipo celular.
Window.size = (720, 1280)
Window.resizable = False


# Paleta de la app (tema "tarot": violeta noche + dorado)
COLOR_FONDO = (0.07, 0.05, 0.11, 1)
COLOR_PANEL = (0.11, 0.08, 0.17, 1)
COLOR_DORADO = (0.78, 0.65, 0.27, 1)
COLOR_TEXTO = (0.92, 0.90, 0.95, 1)
COLOR_TEXTO_TENUE = (0.65, 0.62, 0.70, 1)
COLOR_DERECHO = (0.45, 0.85, 0.55, 1)
COLOR_INVERTIDO = (0.90, 0.45, 0.45, 1)

Window.clearcolor = COLOR_FONDO

# Importamos el mapeo dinámico de imágenes
from src.ruta_imagenes import RUTA_IMAGEN, BASE_DIR, JSON_PATH


KV = """
<TabButton@ButtonBehavior+BoxLayout>:
    activo: False
    texto: ""
    canvas.before:
        Color:
            rgba: (0.78, 0.65, 0.27, 1) if self.activo else (0.16, 0.12, 0.22, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]
    Label:
        text: root.texto
        color: (0.07, 0.05, 0.11, 1) if root.activo else (0.85, 0.83, 0.88, 1)
        bold: root.activo
        font_size: '13sp'

<CardTile>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: (0.14, 0.10, 0.19, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: (0.78, 0.65, 0.27, 0.55)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(12))
            width: 1

<DetailImageFrame@BoxLayout>:
    canvas.before:
        Color:
            rgba: (0.78, 0.65, 0.27, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
"""
Builder.load_string(KV)


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

    (no hay "nombre"/"numero"/"significado" anidados: el nombre es la
    clave del diccionario y el orden define el número).
    """
    if not os.path.exists(JSON_PATH):
        print(f"❌ ERROR CRÍTICO: No se encontró el JSON en: {JSON_PATH}")
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
        ruta_rel = RUTA_IMAGEN.get(nombre, "")
        categorias["Mayores"].append({
            "nombre": f"{indice}. {nombre}",
            "derecho": significado.get("derecho", "Sin texto derecho"),
            "invertido": significado.get("invertido", "Sin texto invertido"),
            "imagen": resolver_ruta_abs(ruta_rel),
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
            ruta_rel = RUTA_IMAGEN.get(nombre, "")
            categorias[cat_nombre].append({
                "nombre": nombre,
                "derecho": significado.get("derecho", "Sin texto derecho"),
                "invertido": significado.get("invertido", "Sin texto invertido"),
                "imagen": resolver_ruta_abs(ruta_rel),
            })

    # DEPURACIÓN EN CONSOLA
    total = sum(len(v) for v in categorias.values())
    con_imagen = sum(1 for lista in categorias.values() for c in lista if c["imagen"])
    print("\n==========================================")
    print(f"📊 CARTAS CARGADAS: {total} de 78  |  con imagen: {con_imagen}")
    for cat, lista in categorias.items():
        print(f" - {cat}: {len(lista)} cartas")
    print("==========================================\n")

    return categorias


DATOS_TAROT = cargar_y_organizar_datos()


class CardTile(ButtonBehavior, BoxLayout):
    """Tarjeta individual de la grilla: imagen + nombre, esquinas redondeadas."""

    def __init__(self, carta, on_press_callback, **kwargs):
        super().__init__(orientation="vertical", padding=dp(6), spacing=dp(4),
                          size_hint_y=None, height=dp(190), **kwargs)
        self.carta = carta

        img_path = carta["imagen"]
        if img_path:
            img = Image(source=img_path, size_hint_y=0.8, allow_stretch=True,
                        keep_ratio=True, mipmap=True)
        else:
            img = Label(text="🔮", font_size="34sp", size_hint_y=0.8,
                        color=COLOR_TEXTO_TENUE)
        self.add_widget(img)

        lbl = Label(
            text=carta["nombre"],
            size_hint_y=0.2,
            font_size="11sp",
            color=COLOR_TEXTO,
            halign="center",
            valign="middle",
            shorten=True,
            shorten_from="right",
        )
        lbl.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.add_widget(lbl)

        self.bind(on_release=lambda *_: on_press_callback(carta))


class GridScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.categoria_actual = "Mayores"
        self.tab_buttons = {}

        root = BoxLayout(orientation="vertical")

        # --- Encabezado ---
        header = BoxLayout(orientation="vertical", size_hint_y=None,
                            height=dp(56), padding=(dp(16), dp(8)))
        titulo = Label(
            text="✦ Diccionario Tarot ✦",
            font_size="19sp",
            bold=True,
            color=COLOR_DORADO,
        )
        header.add_widget(titulo)
        root.add_widget(header)

        # --- Barra de categorías (scroll horizontal, estilo pill) ---
        tabs_scroll = ScrollView(size_hint_y=None, height=dp(44),
                                  do_scroll_x=True, do_scroll_y=False,
                                  bar_width=0)
        tabs_row = BoxLayout(orientation="horizontal", size_hint_x=None,
                              spacing=dp(8), padding=(dp(12), dp(4)))
        tabs_row.bind(minimum_width=tabs_row.setter("width"))

        from kivy.factory import Factory
        for categoria in DATOS_TAROT.keys():
            btn = Factory.TabButton()
            btn.texto = categoria
            btn.activo = (categoria == self.categoria_actual)
            btn.size_hint = (None, None)
            btn.size = (dp(84), dp(34))
            btn.bind(on_release=lambda inst, c=categoria: self.cambiar_categoria(c))
            self.tab_buttons[categoria] = btn
            tabs_row.add_widget(btn)

        tabs_scroll.add_widget(tabs_row)
        root.add_widget(tabs_scroll)

        # --- Grilla de cartas (contenido cambia según categoría) ---
        self.scroll_grid = ScrollView(size_hint_y=1)
        self.grid = GridLayout(cols=3, spacing=dp(8), padding=dp(12),
                                size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll_grid.add_widget(self.grid)
        root.add_widget(self.scroll_grid)

        self.add_widget(root)
        self.poblar_grid(self.categoria_actual)

    def cambiar_categoria(self, categoria):
        if categoria == self.categoria_actual:
            return
        self.tab_buttons[self.categoria_actual].activo = False
        self.categoria_actual = categoria
        self.tab_buttons[categoria].activo = True
        self.poblar_grid(categoria)

    def poblar_grid(self, categoria):
        self.grid.clear_widgets()
        for carta in DATOS_TAROT.get(categoria, []):
            self.grid.add_widget(CardTile(carta, self.ver_detalle))
        self.scroll_grid.scroll_y = 1

    def ver_detalle(self, carta):
        detalle_screen = self.manager.get_screen("detail")
        detalle_screen.actualizar_carta(carta)
        self.manager.current = "detail"


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

        # Botón volver arriba (más natural en flujo móvil).
        # Se usa el Button estándar de Kivy (probado y confiable para tocar),
        # en vez de un widget compuesto a mano.
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
        btn_volver = Button(
            text="‹  Volver",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=COLOR_DORADO,
            bold=True,
            font_size="15sp",
            halign="left",
        )
        btn_volver.bind(on_release=self.volver_grilla)
        top_bar.add_widget(btn_volver)
        # espaciador para que el botón no ocupe todo el ancho de la fila
        top_bar.add_widget(BoxLayout())
        layout.add_widget(top_bar)

        self.lbl_titulo = Label(
            text="",
            size_hint_y=None,
            height=dp(30),
            font_size="19sp",
            bold=True,
            color=COLOR_DORADO,
            halign="left",
            valign="middle",
        )
        self.lbl_titulo.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        layout.add_widget(self.lbl_titulo)

        # Imagen ampliada con marco dorado
        from kivy.factory import Factory
        frame = Factory.DetailImageFrame()
        frame.size_hint_y = 0.42
        frame.padding = dp(3)
        self.img_carta = Image(size_hint_y=1, keep_ratio=True, allow_stretch=True, mipmap=True)
        frame.add_widget(self.img_carta)
        layout.add_widget(frame)

        # Scroll de significados (solo vertical: nunca debe permitir scroll
        # horizontal, así el texto siempre hace wrap al ancho real de pantalla)
        scroll = ScrollView(size_hint_y=1, do_scroll_x=False, do_scroll_y=True)
        desc_box = BoxLayout(orientation="vertical", spacing=dp(12),
                              size_hint_y=None, padding=(0, dp(8)))
        desc_box.bind(minimum_height=desc_box.setter("height"))

        desc_box.add_widget(self._crear_bloque("Derecho", COLOR_DERECHO, "lbl_derecho"))
        desc_box.add_widget(self._crear_bloque("Invertido", COLOR_INVERTIDO, "lbl_invertido"))

        scroll.add_widget(desc_box)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def _crear_bloque(self, titulo_texto, color, attr_name):
        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
        box.bind(minimum_height=box.setter("height"))

        titulo = Label(
            text=titulo_texto,
            size_hint_y=None,
            height=dp(22),
            color=color,
            bold=True,
            font_size="14sp",
            halign="left",
        )
        titulo.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        box.add_widget(titulo)

        lbl = Label(
            text="",
            size_hint_y=None,
            font_size="12sp",
            color=COLOR_TEXTO,
            halign="left",
            valign="top",
        )
        lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        lbl.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
        box.add_widget(lbl)
        setattr(self, attr_name, lbl)

        return box

    def actualizar_carta(self, carta):
        self.lbl_titulo.text = carta["nombre"]
        self.img_carta.source = carta["imagen"] if carta["imagen"] else ""
        self.lbl_derecho.text = carta["derecho"]
        self.lbl_invertido.text = carta["invertido"]

    def volver_grilla(self, instance):
        self.manager.current = "grid"


class TarotApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(GridScreen(name="grid"))
        sm.add_widget(DetailScreen(name="detail"))
        return sm


if __name__ == "__main__" or __name__ == "src.main":
    TarotApp().run()
import os
import flet as ft

RUTA_GUIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "pearls"))
os.makedirs(RUTA_GUIAS, exist_ok=True)

def listar_guias_md():
    archivos = []
    if os.path.exists(RUTA_GUIAS):
        for f in os.listdir(RUTA_GUIAS):
            if f.endswith(".md"):
                archivos.append(f)
    return archivos

def leer_guia_md(nombre_archivo):
    try:
        with open(os.path.join(RUTA_GUIAS, nombre_archivo), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo archivo: {e}"

def pantalla_home(page: ft.Page):
    # Envolver contenido principal en Container para separar bordes ventana
    contenido_principal = ft.Container(
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=30),  # Separación horizontal desde borde ventana
        expand=True,
    )

    seleccion_actual = {"archivo": None, "contenido": None}
    lista_tarjetas = ft.Column(spacing=10, expand=True)

    def construir_tarjetas(filtro=""):
        lista_tarjetas.controls.clear()
        archivos = listar_guias_md()

        if not archivos:
            lista_tarjetas.controls.append(
                ft.Text("No hay guías markdown en assets/guias", size=16, color=ft.Colors.RED)
            )
        else:
            filtro = filtro.lower()
            for archivo in archivos:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                if filtro in nombre_sin_ext.lower():
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(nombre_sin_ext, size=18, weight="bold"),
                                on_click=lambda e, a=archivo: ver_guia(a)
                            ),
                            padding=20
                        ),
                        expand=True,
                    )
                    lista_tarjetas.controls.append(
                        ft.Row([card], alignment=ft.MainAxisAlignment.CENTER, width=500,expand=True)
                    )
        page.update()


    def filtrar_guia(e):
        filtro = e.control.value
        construir_tarjetas(filtro)

    def mostrar_lista():
        contenido_principal.content.controls.clear()

        search_bar = ft.SearchBar(
            bar_hint_text="Buscar guía...",
            view_hint_text="Escribe el nombre de la guía",
            on_change=filtrar_guia,
            controls=[],
            expand=True,
        )

        titulo = ft.Text("Med Pearls", size=25, weight="bold", text_align=ft.TextAlign.CENTER)

        construir_tarjetas()

        contenido_principal.content.controls.extend([
            titulo,
            ft.Container(content=search_bar, padding=15, alignment=ft.alignment.center),
            lista_tarjetas
        ])
        page.update()

    def ver_guia(archivo_md):
        seleccion_actual["archivo"] = archivo_md
        seleccion_actual["contenido"] = leer_guia_md(archivo_md)

        contenido_principal.content.controls.clear()
        titulo = ft.Text(
            os.path.splitext(archivo_md)[0],
            size=20,
            weight="bold",
            text_align=ft.TextAlign.CENTER
        )
        md = ft.Markdown(seleccion_actual["contenido"], expand=True)

        contenedor_md = ft.Container(
            content=md,
            padding=ft.padding.all(20),
            width=700,
            expand=True,
        )

        btn_volver = ft.ElevatedButton("Volver a la lista", on_click=lambda e: mostrar_lista())

        contenido_principal.content.controls.extend([
            titulo,
            contenedor_md,
            ft.Row([btn_volver], alignment=ft.MainAxisAlignment.CENTER)
        ])
        page.update()

    mostrar_lista()
    return contenido_principal
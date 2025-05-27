import os
import flet as ft

RUTA_GUIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "guias"))

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
    contenido_principal = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
    seleccion_actual = {"archivo": None, "contenido": None}

    def mostrar_lista():
        contenido_principal.controls.clear()
        titulo = ft.Text("Guías Clínicas Markdown", size=22, weight="bold", text_align=ft.TextAlign.CENTER)
        lista = ft.Column(spacing=10, expand=True)

        archivos = listar_guias_md()
        if not archivos:
            lista.controls.append(ft.Text("No hay guías markdown en assets/guias", size=16, color=ft.Colors.RED))
        else:
            for archivo in archivos:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                btn_ver = ft.ElevatedButton(
                    f"Ver {nombre_sin_ext}",
                    on_click=lambda e, a=archivo: ver_guia(a),
                    width=300,
                    height=40
                )
                lista.controls.append(btn_ver)

        contenido_principal.controls.extend([titulo, lista])
        page.update()

    def ver_guia(archivo_md):
        seleccion_actual["archivo"] = archivo_md
        seleccion_actual["contenido"] = leer_guia_md(archivo_md)

        contenido_principal.controls.clear()
        titulo = ft.Text(os.path.splitext(archivo_md)[0], size=20, weight="bold", text_align=ft.TextAlign.CENTER)
        md = ft.Markdown(seleccion_actual["contenido"], expand=True)

        btn_editar = ft.ElevatedButton("Editar", on_click=lambda e: editar_guia(archivo_md))
        btn_volver = ft.ElevatedButton("Volver a la lista", on_click=lambda e: mostrar_lista())

        contenido_principal.controls.extend([titulo, md, ft.Row([btn_editar, btn_volver], alignment=ft.MainAxisAlignment.CENTER)])
        page.update()

    def editar_guia(archivo_md):
        contenido_principal.controls.clear()
        titulo = ft.Text(f"Editar: {os.path.splitext(archivo_md)[0]}", size=20, weight="bold", text_align=ft.TextAlign.CENTER)

        text_area = ft.TextField(
            value=leer_guia_md(archivo_md),
            multiline=True,
            expand=True,
            width=500,
            height=400
        )

        def guardar(e):
            exito, error = guardar_guia_md(archivo_md, text_area.value)
            if exito:
                ver_guia(archivo_md)
            else:
                contenido_principal.controls.append(ft.Text(f"Error guardando: {error}", color=ft.Colors.RED))
                page.update()

        btn_guardar = ft.ElevatedButton("Guardar", on_click=guardar)
        btn_cancelar = ft.ElevatedButton("Cancelar", on_click=lambda e: ver_guia(archivo_md))

        contenido_principal.controls.extend([titulo, text_area, ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER)])
        page.update()

    def guardar_guia_md(nombre_archivo, contenido):
        try:
            with open(os.path.join(RUTA_GUIAS, nombre_archivo), "w", encoding="utf-8") as f:
                f.write(contenido)
            return True, ""
        except Exception as e:
            return False, str(e)

    mostrar_lista()

    return contenido_principal


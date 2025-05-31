import os
import tempfile
import flet as ft
from pdf2image import convert_from_path
from PyPDF2 import PdfReader  # Asegúrate de tener instalado PyPDF2
import hashlib

# Carpeta donde se almacenan los PDFs
RUTA_PDFS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
os.makedirs(RUTA_PDFS, exist_ok=True)

def listar_pdfs():
    return [f for f in os.listdir(RUTA_PDFS) if f.lower().endswith(".pdf")]

def pantalla_home(page: ft.Page):
    contenido_principal = ft.Container(
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=30),
        expand=True,
    )

    lista_tarjetas = ft.Column(spacing=10, expand=True)

    def on_result(ev: ft.FilePickerResultEvent):
        if ev.files:
            for f in ev.files:
                destino = os.path.join(RUTA_PDFS, f.name)
                with open(destino, "wb") as out_file, open(f.path, "rb") as in_file:
                    out_file.write(in_file.read())
            construir_tarjetas()
            page.update()

    file_picker = ft.FilePicker(on_result=on_result)
    page.overlay.append(file_picker)

    def construir_tarjetas(filtro=""):
        lista_tarjetas.controls.clear()
        archivos = listar_pdfs()
        if not archivos:
            lista_tarjetas.controls.append(
                ft.Text("No tienes guias subidas", size=16, color=ft.Colors.RED)
            )
        else:
            filtro = filtro.lower()
            for archivo in archivos:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                if filtro in nombre_sin_ext.lower():
                    ruta_pdf = os.path.join(RUTA_PDFS, archivo)
                    # Generar un nombre único para la miniatura usando hash
                    hash_nombre = hashlib.md5(archivo.encode()).hexdigest()
                    temp_path = os.path.join(tempfile.gettempdir(), f"{hash_nombre}_preview.png")
                    # Si no existe la miniatura, créala
                    if not os.path.exists(temp_path):
                        try:
                            imagen = convert_from_path(ruta_pdf, first_page=1, last_page=1, dpi=50)[0]
                            imagen.save(temp_path, "PNG")
                        except Exception as e:
                            temp_path = None
                    # Crear la tarjeta con miniatura
                    miniatura = ft.Image(src=temp_path, width=60, height=80) if temp_path and os.path.exists(temp_path) else None
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                # Izquierda: miniatura + título
                                ft.Row([
                                    miniatura if miniatura else ft.Icon(ft.icons.PICTURE_AS_PDF, size=40),
                                    ft.ListTile(
                                        title=ft.Text(nombre_sin_ext, size=18, weight="bold"),
                                        on_click=lambda e, a=archivo: ver_pdf(a)
                                    ),
                                ], alignment=ft.MainAxisAlignment.START, expand=True),
                                # Derecha: botones
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Renombrar PDF",
                                        on_click=lambda e, archivo=archivo: renombrar_pdf(archivo)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED,
                                        tooltip="Eliminar PDF",
                                        on_click=lambda e, archivo=archivo: eliminar_pdf(archivo)
                                    ),
                                ], alignment=ft.MainAxisAlignment.END),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=20
                        ),
                        expand=True,
                    )
                    lista_tarjetas.controls.append(
                        ft.Row([card], alignment=ft.MainAxisAlignment.CENTER, width=700, expand=True)
                    )
        page.update()

    def filtrar_pdf(e):
        filtro = e.control.value
        construir_tarjetas(filtro)

    def mostrar_lista():
        contenido_principal.content.controls.clear()

        search_bar = ft.SearchBar(
            bar_hint_text="Buscar guía PDF...",
            view_hint_text="Escribe el nombre del PDF",
            on_change=filtrar_pdf,
            controls=[],
            expand=True,
        )

        btn_subir = ft.IconButton(
            icon=ft.Icons.UPLOAD_FILE,
            tooltip="Subir PDF",
            on_click=subir_pdf,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        titulo = ft.Text("Mis guias", size=25, weight="bold", text_align=ft.TextAlign.CENTER)

        construir_tarjetas()

        # Barra de búsqueda y botón subir en la misma fila
        barra_superior = ft.Row(
            controls=[
                ft.Container(content=search_bar, expand=True),
                btn_subir
            ],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        contenido_principal.content.controls.extend([
            titulo,
            barra_superior,
            lista_tarjetas
        ])
        page.update()

    def subir_pdf(e):
        file_picker.pick_files(allow_multiple=True, allowed_extensions=["pdf"])

    def ver_pdf(nombre_pdf):
        contenido_principal.content.controls.clear()

        ruta_pdf = os.path.join(RUTA_PDFS, nombre_pdf)

        # Intentamos obtener el total de páginas
        try:
            reader = PdfReader(ruta_pdf)
            total_paginas = len(reader.pages)
        except Exception as e:
            contenido_principal.content.controls.append(
                ft.Text(f"No se pudo leer el PDF: {e}", color=ft.Colors.RED)
            )
            page.update()
            return

        pagina_actual = {"index": 0}
        imagen_mostrada = ft.Ref[ft.Image]()
        indice_pagina = ft.Ref[ft.Text]()

        def render_pagina(index):
            try:
                # Convertir solo una página del PDF
                imagen = convert_from_path(ruta_pdf, first_page=index+1, last_page=index+1, dpi=150)[0]
                temp_path = os.path.join(tempfile.gettempdir(), f"{nombre_pdf}_pagina_{index}.png")
                imagen.save(temp_path, "PNG")
                imagen_mostrada.current.src = temp_path
                indice_pagina.current.value = f"Página {index + 1} de {total_paginas}"
                page.update()
            except Exception as e:
                imagen_mostrada.current.src = ""
                indice_pagina.current.value = f"Error cargando página: {e}"
                page.update()

        def siguiente(e):
            if pagina_actual["index"] < total_paginas - 1:
                pagina_actual["index"] += 1
                render_pagina(pagina_actual["index"])

        def anterior(e):
            if pagina_actual["index"] > 0:
                pagina_actual["index"] -= 1
                render_pagina(pagina_actual["index"])

        titulo = ft.Text(
            os.path.splitext(nombre_pdf)[0],
            size=20,
            weight="bold",
            text_align=ft.TextAlign.CENTER
        )

        imagen = ft.Image(ref=imagen_mostrada, fit=ft.ImageFit.CONTAIN, width=page.width * 0.9)

        imagen_interactiva = ft.InteractiveViewer(
            content=imagen,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            min_scale=1.0,
            max_scale=5.0
        )

        pagina_info = ft.Text(ref=indice_pagina)

        botones_nav = ft.Row([
            ft.ElevatedButton("Anterior", on_click=anterior),
            pagina_info,
            ft.ElevatedButton("Siguiente", on_click=siguiente)
        ], alignment=ft.MainAxisAlignment.CENTER)

        btn_volver = ft.ElevatedButton("Volver a la lista", on_click=lambda e: mostrar_lista())

        contenido_principal.content.controls.extend([
            titulo,
            imagen_interactiva,
            botones_nav,
            btn_volver
        ])

        render_pagina(pagina_actual["index"])  # Mostrar primera página
        page.update()

    def renombrar_pdf(archivo):
        nombre_actual = os.path.splitext(archivo)[0]
        nuevo_nombre = ft.TextField(label="Nuevo nombre", value=nombre_actual, expand=True)

        def confirmar_renombrar(ev):
            nuevo = nuevo_nombre.value.strip()
            if not nuevo:
                page.snack_bar = ft.SnackBar(ft.Text("El nombre no puede estar vacío."), bgcolor=ft.Colors.RED)
                page.snack_bar.open = True
                page.update()
                return
            nuevo_archivo = nuevo + ".pdf"
            destino = os.path.join(RUTA_PDFS, nuevo_archivo)
            if os.path.exists(destino):
                page.snack_bar = ft.SnackBar(ft.Text("Ya existe un PDF con ese nombre."), bgcolor=ft.Colors.RED)
                page.snack_bar.open = True
                page.update()
                return
            os.rename(os.path.join(RUTA_PDFS, archivo), destino)
            page.close(dialogo_renombrar)
            construir_tarjetas()
            page.update()

        dialogo_renombrar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Renombrar PDF"),
            content=nuevo_nombre,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_renombrar)),
                ft.TextButton("Renombrar", on_click=confirmar_renombrar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialogo_renombrar)

    def eliminar_pdf(archivo):
        ruta_pdf = os.path.join(RUTA_PDFS, archivo)

        def confirmar_eliminar(ev):
            os.remove(ruta_pdf)
            page.close(dialogo_eliminar)
            construir_tarjetas()
            page.update()

        dialogo_eliminar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar PDF"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar '{archivo}'?", size=16),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_eliminar)),
                ft.TextButton("Eliminar", on_click=confirmar_eliminar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialogo_eliminar)

    mostrar_lista()
    return contenido_principal

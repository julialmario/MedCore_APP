import os
import flet as ft

RUTA_HISTORIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "hc"))
os.makedirs(RUTA_HISTORIAS, exist_ok=True)

def pantalla_historia_clinica(page: ft.Page):
    mensaje = ft.Text("", color=ft.Colors.GREEN)
    vista_principal = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Campos del formulario
    campos = {
        "paciente": ft.TextField(label="Nombre del paciente"),
        "edad": ft.TextField(label="Edad", input_filter=ft.NumbersOnlyInputFilter()),
        "sexo": ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Femenino"),
                ft.dropdown.Option("Otro"),
            ],
        ),
        "motivo": ft.TextField(label="Motivo de consulta", multiline=True, max_lines=3),
        "antecedentes": ft.TextField(label="Antecedentes", multiline=True, max_lines=3),
        "examen": ft.TextField(label="Examen físico", multiline=True, max_lines=3),
        "diagnostico": ft.TextField(label="Impresión diagnóstica", multiline=True, max_lines=2),
        "plan": ft.TextField(label="Plan", multiline=True, max_lines=2),
    }

    def listar_archivos_md():
        archivos = []
        for f in os.listdir(RUTA_HISTORIAS):
            if f.endswith(".md"):
                archivos.append(f)
        return archivos

    def leer_archivo_md(nombre_archivo):
        try:
            with open(os.path.join(RUTA_HISTORIAS, nombre_archivo), "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error al leer el archivo: {e}"

    def ver_historia(nombre_archivo):
        contenido = leer_archivo_md(nombre_archivo)
        vista_principal.controls.clear()

        vista_principal.controls.append(ft.Text(os.path.splitext(nombre_archivo)[0], size=22, weight="bold"))
        vista_principal.controls.append(ft.Markdown(contenido, expand=True, selectable=True))
        vista_principal.controls.append(
            ft.ElevatedButton("Volver a la lista", icon=ft.Icons.ARROW_BACK, on_click=lambda e: mostrar_lista())
        )
        page.update()

    def mostrar_formulario(e=None):
        vista_principal.controls.clear()

        formulario = ft.Column(
            controls=[
                ft.Text("Nueva Historia Clínica", size=24, weight="bold"),
                *campos.values(),
                ft.ElevatedButton("Guardar historia clínica", icon=ft.Icons.SAVE, on_click=guardar_historia),
                ft.ElevatedButton("Volver a la lista", icon=ft.Icons.ARROW_BACK, on_click=lambda e: mostrar_lista()),
                mensaje,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        vista_principal.controls.append(
            ft.Container(content=formulario, padding=30, width=600, alignment=ft.alignment.center, expand=True)
        )
        page.update()

    def guardar_historia(e):
        nombre = campos["paciente"].value.strip()
        if not nombre:
            mensaje.value = "Debes ingresar el nombre del paciente."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        nombre_archivo = nombre.replace(" ", "_") + ".md"
        ruta_archivo = os.path.join(RUTA_HISTORIAS, nombre_archivo)

        contenido = f"""# Historia Clínica

**Paciente:** {campos["paciente"].value}  
**Edad:** {campos["edad"].value}  
**Sexo:** {campos["sexo"].value}

## Motivo de consulta
{campos["motivo"].value}

## Antecedentes
{campos["antecedentes"].value}

## Examen físico
{campos["examen"].value}

## Impresión diagnóstica
{campos["diagnostico"].value}

## Plan
{campos["plan"].value}
"""

        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido)
            mensaje.value = f"Historia guardada como {nombre_archivo}"
            mensaje.color = ft.Colors.GREEN

            for campo in campos.values():
                campo.value = ""
        except Exception as err:
            mensaje.value = f"Error al guardar: {err}"
            mensaje.color = ft.Colors.RED

        page.update()

    def mostrar_lista():
        vista_principal.controls.clear()

        # Contenedor superior con título y botón
        encabezado = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Historias clínicas", size=25, weight="bold", expand=True),
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                        on_click=mostrar_formulario,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=100),
                            padding=10
                        ),
                        tooltip="Crear nueva historia",
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(16),
            margin=ft.margin.only(top=10, bottom=20),
            width=300,
            alignment=ft.alignment.center
        )

        vista_principal.controls.append(encabezado)

        archivos = listar_archivos_md()
        if not archivos:
            vista_principal.controls.append(ft.Text("No hay historias clínicas guardadas."))
        else:
            for archivo in archivos:
                nombre = os.path.splitext(archivo)[0]
                card = ft.Card(
                    content=ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(nombre),
                            on_click=lambda e, a=archivo: ver_historia(a)
                        ),
                        padding=10
                    )
                )
                vista_principal.controls.append(card)

        page.update()

    mostrar_lista()
    return vista_principal



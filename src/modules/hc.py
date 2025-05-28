import os
import flet as ft

RUTA_HISTORIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "data", "historias_clinicas"))
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

    # Variable para almacenar el archivo actual que se está editando (None si es nuevo)
    archivo_actual = None

    def listar_archivos_md():
        archivos = []
        if not os.path.exists(RUTA_HISTORIAS):
            os.makedirs(RUTA_HISTORIAS)
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

    def mostrar_formulario(e=None, editar=False, archivo=None):
        nonlocal archivo_actual
        vista_principal.controls.clear()
        archivo_actual = archivo if editar else None

        if editar and archivo_actual:
            # Leer archivo y parsear contenido para llenar campos
            contenido = leer_archivo_md(archivo_actual)
            # Parsear contenido simple basado en el formato markdown que guardamos
            # Usaremos una forma simple con splitlines y buscamos líneas clave
            lines = contenido.splitlines()
            data = {
                "paciente": "",
                "edad": "",
                "sexo": "",
                "motivo": "",
                "antecedentes": "",
                "examen": "",
                "diagnostico": "",
                "plan": "",
            }
            # Extraemos valores
            for i, line in enumerate(lines):
                if line.startswith("**Paciente:**"):
                    data["paciente"] = line.split("**Paciente:**")[1].strip()
                elif line.startswith("**Edad:**"):
                    data["edad"] = line.split("**Edad:**")[1].strip()
                elif line.startswith("**Sexo:**"):
                    data["sexo"] = line.split("**Sexo:**")[1].strip()
                elif line.startswith("## Motivo de consulta"):
                    # Texto multilinea después de esta línea hasta la siguiente cabecera
                    motivo_lines = []
                    for j in range(i+1, len(lines)):
                        if lines[j].startswith("## "):
                            break
                        motivo_lines.append(lines[j])
                    data["motivo"] = "\n".join(motivo_lines).strip()
                elif line.startswith("## Antecedentes"):
                    antecedentes_lines = []
                    for j in range(i+1, len(lines)):
                        if lines[j].startswith("## "):
                            break
                        antecedentes_lines.append(lines[j])
                    data["antecedentes"] = "\n".join(antecedentes_lines).strip()
                elif line.startswith("## Examen físico"):
                    examen_lines = []
                    for j in range(i+1, len(lines)):
                        if lines[j].startswith("## "):
                            break
                        examen_lines.append(lines[j])
                    data["examen"] = "\n".join(examen_lines).strip()
                elif line.startswith("## Impresión diagnóstica"):
                    diag_lines = []
                    for j in range(i+1, len(lines)):
                        if lines[j].startswith("## "):
                            break
                        diag_lines.append(lines[j])
                    data["diagnostico"] = "\n".join(diag_lines).strip()
                elif line.startswith("## Plan"):
                    plan_lines = []
                    for j in range(i+1, len(lines)):
                        if lines[j].startswith("## "):
                            break
                        plan_lines.append(lines[j])
                    data["plan"] = "\n".join(plan_lines).strip()

            # Asignar datos a campos
            for k, v in data.items():
                if k == "sexo":
                    # Seleccionar la opción correcta del dropdown
                    for option in campos["sexo"].options:
                        if option.key == v or option.text == v:
                            campos["sexo"].value = option.text
                            break
                    else:
                        campos["sexo"].value = None
                else:
                    campos[k].value = v
        else:
            # Campos vacíos para nueva historia
            for campo in campos.values():
                if isinstance(campo, ft.Dropdown):
                    campo.value = None
                else:
                    campo.value = ""

        formulario = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Editar Historia Clínica" if editar else "Nueva Historia Clínica", size=24, weight="bold", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Volver a la lista",
                            on_click=lambda e: mostrar_lista(),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.SAVE,
                            tooltip="Guardar historia clínica",
                            on_click=guardar_historia,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                *campos.values(),
                mensaje,
            ],
            spacing=20,
        )

        contenedor_formulario = ft.Container(
            content=formulario,
            padding=20,
            margin=ft.margin.symmetric(horizontal=100),
            width=500,
            alignment=ft.alignment.center,
            expand=True
        )

        vista_principal.controls.append(
            ft.Row(
                controls=[contenedor_formulario],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )

        page.update()

    def guardar_historia(e):
        nonlocal archivo_actual

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
            # Si editamos, sobreescribimos el archivo original; si es nuevo, escribimos con el nombre nuevo
            if archivo_actual and archivo_actual != nombre_archivo:
                # Si el nombre paciente cambió, eliminamos el viejo para evitar duplicados
                os.remove(os.path.join(RUTA_HISTORIAS, archivo_actual))
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido)

            # Limpiar campos después de guardar
            for campo in campos.values():
                if isinstance(campo, ft.Dropdown):
                    campo.value = None
                else:
                    campo.value = ""

            archivo_actual = None
            mensaje.value = "Historia guardada correctamente."
            mensaje.color = ft.Colors.GREEN

            # Mostrar la lista actualizada
            mostrar_lista()

        except Exception as err:
            mensaje.value = f"Error al guardar: {err}"
            mensaje.color = ft.Colors.RED
            page.update()

    # Diálogo de confirmación eliminación (igual que antes)
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro que quieres eliminar esta historia clínica?"),
        actions=[
            ft.TextButton("No", on_click=lambda e: page.close(confirm_dialog)),
            ft.TextButton("Sí", on_click=None),  # Se asigna dinámicamente
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def eliminar_historia(nombre_archivo):
        try:
            os.remove(os.path.join(RUTA_HISTORIAS, nombre_archivo))
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Historia '{nombre_archivo}' eliminada"),
                bgcolor=ft.Colors.GREEN
            )
            page.snack_bar.open = True
            mostrar_lista()
        except Exception as err:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al eliminar: {err}"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
        page.update()

    def pedir_confirmacion_eliminar(nombre_archivo):
        def on_confirm(e):
            eliminar_historia(nombre_archivo)
            page.close(confirm_dialog)
            page.update()

        confirm_dialog.actions[1].on_click = on_confirm
        page.open(confirm_dialog)

    def mostrar_lista():
        vista_principal.controls.clear()

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
            vista_principal.controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("No hay historias clínicas guardadas."),
                            padding=10,
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            )
        else:
            for archivo in archivos:
                nombre = os.path.splitext(archivo)[0]

                # Creamos fila con botones ver, editar y eliminar
                fila = ft.Row(
                    controls=[
                        ft.Text(nombre, expand=True, size=16),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar historia",
                            on_click=lambda e, a=archivo: mostrar_formulario(e, editar=True, archivo=a),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar historia",
                            on_click=lambda e, a=archivo: pedir_confirmacion_eliminar(a),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                )

                card = ft.Card(
                    content=ft.Container(
                        content=fila,
                        padding=10
                    ),
                    margin=ft.margin.symmetric(vertical=5, horizontal=10),
                    elevation=2,
                )

                vista_principal.controls.append(card)

        page.update()

    mostrar_lista()
    return vista_principal



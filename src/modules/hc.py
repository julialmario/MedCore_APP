import os
import flet as ft

RUTA_HISTORIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "data", "historias_clinicas"))
os.makedirs(RUTA_HISTORIAS, exist_ok=True)

def pantalla_historia_clinica(page: ft.Page):
    mensaje = ft.Text("", color=ft.Colors.GREEN)
    vista_principal = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Campos del formulario según tu estructura
    campos = {
        "documento": ft.TextField(label="Documento"),
        "nombre": ft.TextField(label="Nombre y apellidos"),
        "estado_civil": ft.TextField(label="Estado civil"),
        "fecha_nacimiento": ft.TextField(label="Fecha de nacimiento"),
        "edad": ft.TextField(label="Edad", input_filter=ft.NumbersOnlyInputFilter()),
        "sexo": ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Femenino"),
                ft.dropdown.Option("Otro"),
            ],
        ),
        "hemoclasificacion": ft.TextField(label="Hemoclasificación"),
        "ocupacion": ft.TextField(label="Ocupación"),
        "escolaridad": ft.TextField(label="Escolaridad"),
        "direccion": ft.TextField(label="Dirección y Lugar de residencia"),
        "nombre_acompanante": ft.TextField(label="Nombre Acompañante"),
        "parentesco_acompanante": ft.TextField(label="Parentesco del acompañante"),
        "eps": ft.TextField(label="EPS"),
        "fuente_info": ft.TextField(label="Fuente de información y confiabilidad"),
        "motivo": ft.TextField(label="Motivo de consulta", multiline=True, max_lines=3),
        "enfermedad_actual": ft.TextField(label="Enfermedad actual", multiline=True, max_lines=3),

        # Antecedentes
        "patologicos": ft.TextField(label="Patológicos", multiline=True, max_lines=2),
        "infecciosos": ft.TextField(label="Infecciosos y no infecciosos", multiline=True, max_lines=2),
        "alergias": ft.TextField(label="Alergias", multiline=True, max_lines=2),
        "hospitalizaciones": ft.TextField(label="Hospitalizaciones previas", multiline=True, max_lines=2),
        "urgencias": ft.TextField(label="Consultas a urgencias", multiline=True, max_lines=2),
        "quirurgicos": ft.TextField(label="Quirúrgicos", multiline=True, max_lines=2),
        "transfusionales": ft.TextField(label="Transfusionales", multiline=True, max_lines=2),
        "traumaticos": ft.TextField(label="Traumáticos", multiline=True, max_lines=2),
        "zoo_contactos": ft.TextField(label="Zoo Contactos", multiline=True, max_lines=2),
        "epidemiologicos": ft.TextField(label="Epidemiológicos", multiline=True, max_lines=2),

        # No patológicos
        "prenatales": ft.TextField(label="Prenatales y perinatales", multiline=True, max_lines=2),
        "alimentacion": ft.TextField(label="Alimentación", multiline=True, max_lines=2),
        "crecimiento": ft.TextField(label="Crecimiento y desarrollo", multiline=True, max_lines=2),
        "inmunizaciones": ft.TextField(label="Inmunizaciones", multiline=True, max_lines=2),
        "sicosociales": ft.TextField(label="Sicosociales", multiline=True, max_lines=2),
        "escolaridad_no_pat": ft.TextField(label="Escolaridad (no patológicos)", multiline=True, max_lines=2),

        # Familiares
        "familiares_patologias": ft.TextField(label="Familiares - Patologías diagnosticadas", multiline=True, max_lines=2),
        "familiares_composicion": ft.TextField(label="Familiares - Composición familiar", multiline=True, max_lines=2),

        "revision_sistemas": ft.TextField(label="Revisión por sistemas", multiline=True, max_lines=4),

        # Examen físico
        "aspectos_generales": ft.TextField(label="Aspectos generales", multiline=True, max_lines=2),
        "signos_vitales": ft.TextField(label="Signos vitales (T, FC, FR, PA, SAO2, FIO2)", multiline=True, max_lines=2),
        "peso": ft.TextField(label="Peso"),
        "talla": ft.TextField(label="Talla"),
        "piel": ft.TextField(label="Piel", multiline=True, max_lines=2),
        "cabeza": ft.TextField(label="Cabeza", multiline=True, max_lines=2),
        "ojos": ft.TextField(label="Ojos", multiline=True, max_lines=2),
        "boca": ft.TextField(label="Boca", multiline=True, max_lines=2),
        "oidos": ft.TextField(label="Oidos", multiline=True, max_lines=2),
        "nariz": ft.TextField(label="Nariz", multiline=True, max_lines=2),
        "cuello": ft.TextField(label="Cuello", multiline=True, max_lines=2),
        "cardiopulmonar": ft.TextField(label="Cardiopulmonar", multiline=True, max_lines=2),
        "abdomen": ft.TextField(label="Abdomen", multiline=True, max_lines=2),
        "neuromuscular": ft.TextField(label="Neuromuscular", multiline=True, max_lines=2),
        "musculo_esqueletico": ft.TextField(label="Músculo esquelético", multiline=True, max_lines=2),
        "dx": ft.TextField(label="DX", multiline=True, max_lines=2),
        "analisis": ft.TextField(label="Analisis", multiline=True, max_lines=2),
        "plan_manejo": ft.TextField(label="Plan de manejo", multiline=True, max_lines=2),
        "t": ft.TextField(label="T", width=90),
        "fc": ft.TextField(label="FC", width=90),
        "fr": ft.TextField(label="FR", width=90),
        "pa": ft.TextField(label="PA", width=90),
        "sao2": ft.TextField(label="SAO2", width=90),
        "fio2": ft.TextField(label="FIO2", width=90),
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

        # Opcional: puedes agregar un separador visual arriba
        vista_principal.controls.append(
            ft.Text(os.path.splitext(nombre_archivo)[0], size=22, weight="bold", text_align=ft.TextAlign.CENTER)
        )

        # El Markdown se muestra centrado y con ancho fijo para mejor lectura
        vista_principal.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Markdown(
                            contenido,
                            expand=True,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="atom-one-light",  # O el tema que prefieras
                            on_tap_link=lambda e: page.launch_url(e.data)
                        ),
                        alignment=ft.alignment.center,
                        width=700,  # Puedes ajustar el ancho
                        padding=ft.padding.all(20),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

        vista_principal.controls.append(
            ft.ElevatedButton("Volver a la lista", icon=ft.Icons.ARROW_BACK, on_click=lambda e: mostrar_lista())
        )
        page.update()

    def mostrar_formulario(e=None, editar=False, archivo=None):
        nonlocal archivo_actual
        vista_principal.controls.clear()
        archivo_actual = archivo if editar else None

        if editar and archivo_actual:
            contenido = leer_archivo_md(archivo_actual)
            lines = contenido.splitlines()
            seccion = None
            for line in lines:
                line = line.strip()
                if line.startswith("## "):
                    seccion = line.replace("##", "").strip().lower()
                    continue
                if line.startswith("### "):
                    seccion = line.replace("###", "").strip().lower()
                    continue
                if line.startswith("**") and ":**" in line:
                    label, valor = line.split(":**", 1)
                    label = label.replace("**", "").strip()
                    valor = valor.strip()
                    # Buscar el campo por label
                    for k, campo in campos.items():
                        if campo.label == label:
                            campo.value = valor
                            break
                elif seccion == "motivo de consulta" and "motivo" in campos:
                    campos["motivo"].value += (line + "\n") if line else ""
                elif seccion == "enfermedad actual" and "enfermedad_actual" in campos:
                    campos["enfermedad_actual"].value += (line + "\n") if line else ""
                elif seccion == "revisión por sistemas" and "revision_sistemas" in campos:
                    campos["revision_sistemas"].value += (line + "\n") if line else ""
                elif seccion == "dx" and "dx" in campos:
                    campos["dx"].value += (line + "\n") if line else ""
                elif seccion == "análisis" and "analisis" in campos:
                    campos["analisis"].value += (line + "\n") if line else ""
                elif seccion == "plan de manejo" and "plan_manejo" in campos:
                    campos["plan_manejo"].value += (line + "\n") if line else ""
                elif seccion == "examen físico":
                    # Los campos de examen físico están como "**Label:** valor"
                    if line.startswith("**") and ":**" in line:
                        label, valor = line.split(":**", 1)
                        label = label.replace("**", "").strip()
                        valor = valor.strip()
                        for k, campo in campos.items():
                            if campo.label == label:
                                campo.value = valor
                                break
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
                        ft.Text("Historia Clínica", size=24, weight="bold", expand=True),
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
                ft.Text("Datos personales", weight="bold"),
                campos["documento"], campos["nombre"], campos["estado_civil"], campos["fecha_nacimiento"], campos["edad"], campos["sexo"],
                campos["hemoclasificacion"], campos["ocupacion"], campos["escolaridad"], campos["direccion"],
                campos["nombre_acompanante"], campos["parentesco_acompanante"], campos["eps"], campos["fuente_info"],

                ft.Text("Motivo de consulta", weight="bold"),
                campos["motivo"],

                ft.Text("Enfermedad actual", weight="bold"),
                campos["enfermedad_actual"],

                ft.Text("Antecedentes", weight="bold"),
                campos["patologicos"], campos["infecciosos"], campos["alergias"], campos["hospitalizaciones"], campos["urgencias"],
                campos["quirurgicos"], campos["transfusionales"], campos["traumaticos"], campos["zoo_contactos"], campos["epidemiologicos"],

                ft.Text("No patológicos", weight="bold"),
                campos["prenatales"], campos["alimentacion"], campos["crecimiento"], campos["inmunizaciones"], campos["sicosociales"], campos["escolaridad_no_pat"],

                ft.Text("Familiares", weight="bold"),
                campos["familiares_patologias"], campos["familiares_composicion"],

                ft.Text("Revisión por sistemas", weight="bold"),
                campos["revision_sistemas"],

                ft.Text("Examen físico", weight="bold"),
                campos["aspectos_generales"],
                ft.Text("Signos vitales", weight="bold"),
                ft.Row(
                    controls=[
                        campos["t"],
                        campos["fc"],
                        campos["fr"],
                        campos["pa"],
                        campos["sao2"],
                        campos["fio2"],
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=True,  # Esto permite que se acomoden en varias líneas si el espacio es pequeño
                ),
                campos["peso"], campos["talla"], campos["piel"], campos["cabeza"], campos["ojos"], campos["boca"],
                campos["oidos"], campos["nariz"], campos["cuello"], campos["cardiopulmonar"], campos["abdomen"],
                campos["neuromuscular"], campos["musculo_esqueletico"],

                ft.Text("DX", weight="bold"),
                campos["dx"],

                ft.Text("Análisis", weight="bold"),
                campos["analisis"],

                ft.Text("Plan de manejo", weight="bold"),
                campos["plan_manejo"],

                mensaje,
            ],
            spacing=15,
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
        datos = {k: v.value for k, v in campos.items()}

        # Validación básica
        nombre = campos["nombre"].value.strip()
        if not nombre:
            mensaje.value = "Debes ingresar el nombre y apellidos del paciente."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        nombre_archivo = nombre.replace(" ", "_") + ".md"
        ruta_archivo = os.path.join(RUTA_HISTORIAS, nombre_archivo)

        # Estructura Markdown
        contenido = f"# Historia Clínica\n\n"
        contenido += "## Datos personales\n"
        for k in [
            "documento", "nombre", "estado_civil", "fecha_nacimiento", "edad", "sexo", "hemoclasificacion",
            "ocupacion", "escolaridad", "direccion", "nombre_acompanante", "parentesco_acompanante", "eps", "fuente_info"
        ]:
            contenido += f"**{campos[k].label}:** {datos[k]}\n"

        contenido += "\n## Motivo de consulta\n"
        contenido += f"{datos['motivo']}\n"

        contenido += "\n## Enfermedad actual\n"
        contenido += f"{datos['enfermedad_actual']}\n"

        contenido += "\n## Antecedentes\n"
        for k in [
            "patologicos", "infecciosos", "alergias", "hospitalizaciones", "urgencias", "quirurgicos",
            "transfusionales", "traumaticos", "zoo_contactos", "epidemiologicos"
        ]:
            contenido += f"- **{campos[k].label}:** {datos[k]}\n"

        contenido += "\n### No patológicos\n"
        for k in [
            "prenatales", "alimentacion", "crecimiento", "inmunizaciones", "sicosociales", "escolaridad_no_pat"
        ]:
            contenido += f"- **{campos[k].label}:** {datos[k]}\n"

        contenido += "\n### Familiares\n"
        for k in ["familiares_patologias", "familiares_composicion"]:
            contenido += f"- **{campos[k].label}:** {datos[k]}\n"

        contenido += "\n## Revisión por sistemas\n"
        contenido += f"{datos['revision_sistemas']}\n"

        contenido += "\n## Examen físico\n"
        for k in [
            "aspectos_generales",
            "t", "fc", "fr", "pa", "sao2", "fio2",  # signos vitales individuales
            "peso", "talla", "piel", "cabeza", "ojos", "boca", "oidos", "nariz", "cuello",
            "cardiopulmonar", "abdomen", "neuromuscular", "musculo_esqueletico"
        ]:
            contenido += f"- **{campos[k].label}:** {datos[k]}\n"

        contenido += "\n## DX\n"
        contenido += f"{datos['dx']}\n"

        contenido += "\n## Análisis\n"
        contenido += f"{datos['analisis']}\n"

        contenido += "\n## Plan de manejo\n"
        contenido += f"{datos['plan_manejo']}\n"

        try:
            # Si editamos, sobreescribimos el archivo original; si es nuevo, escribimos con el nombre nuevo
            if archivo_actual and archivo_actual != nombre_archivo:
                os.remove(os.path.join(RUTA_HISTORIAS, archivo_actual))
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido)

            # Limpiar campos después de guardar
            for campo in campos.values():
                if isinstance(campo, ft.Dropdown):
                    campo.value = None
                else:
                    campo.value = ""

            mensaje.value = "Historia guardada correctamente."
            mensaje.color = ft.Colors.GREEN
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

                # El texto con on_click para mostrar la historia
                boton_nombre = ft.TextButton(
                    text=nombre,
                    expand=True,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                    on_click=lambda e, a=archivo: ver_historia(a),
                )

                fila = ft.Row(
                    controls=[
                        boton_nombre,
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



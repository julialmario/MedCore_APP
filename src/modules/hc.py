import os
import flet as ft
import asyncio
import re

RUTA_HISTORIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "data", "historias_clinicas"))
os.makedirs(RUTA_HISTORIAS, exist_ok=True)

def pantalla_historia_clinica(page: ft.Page):
    mensaje = ft.Text("", color=ft.Colors.GREEN, text_align=ft.TextAlign.CENTER)
    vista_principal = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    formulario_abierto = {"abierto": False}

    def on_fecha_change(e):
        valor = campos["fecha_historia"].value
        # Solo permite números y guiones, máximo 10 caracteres
        valor_filtrado = re.sub(r"[^\d-]", "", valor)[:10]
        # Detecta si el usuario está borrando
        if len(valor_filtrado) < len(getattr(on_fecha_change, "ultimo_valor", "")):
            # Si está borrando, no autocompleta guiones
            campos["fecha_historia"].value = valor_filtrado
        else:
            # Autocompleta los guiones solo al escribir
            if len(valor_filtrado) == 4 and not valor_filtrado.endswith("-"):
                valor_filtrado += "-"
            elif len(valor_filtrado) == 7 and valor_filtrado.count("-") == 1:
                valor_filtrado += "-"
            if len(valor_filtrado) > 4 and valor_filtrado[4] != "-":
                valor_filtrado = valor_filtrado[:4] + "-" + valor_filtrado[4:]
            if len(valor_filtrado) > 7 and valor_filtrado[7] != "-":
                valor_filtrado = valor_filtrado[:7] + "-" + valor_filtrado[7:]
            campos["fecha_historia"].value = valor_filtrado
        # Guarda el último valor para la próxima llamada
        on_fecha_change.ultimo_valor = campos["fecha_historia"].value
        page.update()

    # Campos del formulario según tu estructura
    campos = {
        "documento": ft.TextField(label="Documento", expand=True),
        "cama": ft.TextField(label="Cama", expand=True),
        "fecha_historia": ft.TextField(
            label="Fecha historia",
            hint_text="YYYY-MM-DD",
            expand=True,
            on_change=on_fecha_change,
        ),
        "nombre": ft.TextField(label="Nombre y apellidos"),
        "estado_civil": ft.TextField(label="Estado civil"),
        "fecha_nacimiento": ft.TextField(label="Fecha de nacimiento",expand=True),
        "edad": ft.TextField(label="Edad", input_filter=ft.NumbersOnlyInputFilter(),expand=True),
        "sexo": ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Femenino"),
                ft.dropdown.Option("Otro"),
            ],
            expand=True,
        ),
        "hemoclasificacion": ft.Dropdown(
            label="Hemoclasificación",
            options=[
                ft.dropdown.Option("A+"),
                ft.dropdown.Option("A-"),
                ft.dropdown.Option("B+"),
                ft.dropdown.Option("B-"),
                ft.dropdown.Option("AB+"),
                ft.dropdown.Option("AB-"),
                ft.dropdown.Option("O+"),
                ft.dropdown.Option("O-"),
            ],
            expand=True,
        ),
        "ocupacion": ft.TextField(label="Ocupación"),
        "escolaridad": ft.TextField(label="Escolaridad"),
        "direccion": ft.TextField(label="Dirección y Lugar de residencia"),
        "nombre_acompanante": ft.TextField(label="Nombre Acompañante"),
        "parentesco_acompanante": ft.Dropdown(
            label="Parentesco del acompañante",
            options=[
                ft.dropdown.Option("Madre"),
                ft.dropdown.Option("Padre"),
                ft.dropdown.Option("Hijo/a"),
                ft.dropdown.Option("Esposo/a"),
                ft.dropdown.Option("Amigo"),
            ],
            expand=True,
        ),
        "fuente_info": ft.Dropdown(
            label="Confiabilidad",
            options=[
                ft.dropdown.Option("Buena"),
                ft.dropdown.Option("Aceptable"),
                ft.dropdown.Option("Baja"),
            ],
            expand=True,
        ),
        "eps": ft.TextField(label="EPS"),
        "motivo": ft.TextField(label="Motivo de consulta", multiline=True, max_lines=3),
        "enfermedad_actual": ft.TextField(label="Enfermedad actual", multiline=True, max_lines=10),

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
        "peso": ft.TextField(label="Peso/Kg", width=100),
        "talla": ft.TextField(label="Talla/Cm", width=100),
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
        "plan_manejo": ft.TextField(label="Plan de manejo", multiline=True, max_lines=10),
        "t": ft.TextField(label="T", width=90),
        "fc": ft.TextField(label="FC", width=90),
        "fr": ft.TextField(label="FR", width=90),
        "pa": ft.TextField(label="PA", width=90),
        "sao2": ft.TextField(label="SAO2", width=90),
        "fio2": ft.TextField(label="FIO2", width=90),
    }

    # Define el texto por defecto al inicio de la función
    plan_manejo_default = """Hospitalizar
Toma de exámenes de laboratorio
Solicitar RX de torax
Toma de signos vitales cada 8-12 horas
mantener hidratacion V/O o VI
Oxigeno por canula nasal a 1 litro
manejo del dolor acetaminofén 15 mg/kg cada 6 horas
Aislamiento por gota
"""

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

        nombre_paciente = os.path.splitext(nombre_archivo)[0]

        # Título y botones en la parte superior, separados del borde lateral
        vista_principal.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            nombre_paciente,
                            size=22,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Volver a la lista",
                            on_click=lambda e: mostrar_lista()
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar historia",
                            on_click=lambda e: mostrar_formulario(e, editar=True, archivo=nombre_archivo)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=24),  # <-- Solo separación lateral
            )
        )

        # Contenedor responsivo para el Markdown
        vista_principal.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Markdown(
                            contenido,
                            expand=True,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="atom-one-light",
                            on_tap_link=lambda e: page.launch_url(e.data)
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(10),
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
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
                if (line.startswith("**") or line.startswith("- **")) and ":**" in line:
                    # Quita el guion si existe
                    clean_line = line.lstrip("- ").strip()
                    label, valor = clean_line.split(":**", 1)
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
            for k, campo in campos.items():
                if k == "plan_manejo":
                    campo.value = plan_manejo_default
                elif isinstance(campo, ft.Dropdown):
                    campo.value = None
                else:
                    campo.value = ""

        formulario = ft.Column(
            controls=[
                mensaje,  # Mensaje centrado arriba
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
                ft.Row(
                    controls=[
                        campos["documento"],
                        campos["cama"],
                        campos["fecha_historia"],
                    ],
                    spacing=10,
                    expand=True,
                ),
                campos["eps"],  # EPS debajo de la fila
                campos["nombre"], campos["estado_civil"],
                ft.Row(
                    controls=[
                        campos["fecha_nacimiento"],
                        campos["edad"],
                    ],
                    spacing=10,
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        campos["sexo"],
                        campos["hemoclasificacion"],
                    ],
                    spacing=10,
                    expand=True,
                ),
                campos["ocupacion"], campos["escolaridad"], campos["direccion"],
                campos["nombre_acompanante"],
                ft.Row(
                    controls=[
                        campos["parentesco_acompanante"],
                        campos["fuente_info"],
                    ],
                    spacing=10,
                    expand=True,
                ),
                campos["eps"],

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
                ft.Container(
                    content=ft.Row(
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
                        expand=True,
                        wrap=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    width=True,
                    padding=ft.padding.symmetric(vertical=5),
                ),
                ft.Text("Antropometría", weight="bold"),  # <-- Nuevo título
                ft.Container(
                    content=ft.Row(
                        controls=[
                            campos["peso"],
                            campos["talla"],
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                        wrap=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    width=True,
                    padding=ft.padding.symmetric(vertical=5),
                ),
                ft.Text("Examen físico por sistemas", weight="bold"),  # <-- Nuevo título
                campos["piel"], campos["cabeza"], campos["ojos"], campos["boca"],
                campos["oidos"], campos["nariz"], campos["cuello"], campos["cardiopulmonar"], campos["abdomen"],
                campos["neuromuscular"], campos["musculo_esqueletico"],

                ft.Text("DX", weight="bold"),
                campos["dx"],

                ft.Text("Análisis", weight="bold"),
                campos["analisis"],

                ft.Text("Plan de manejo", weight="bold"),
                campos["plan_manejo"],
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra los hijos del formulario
        )

        contenedor_formulario = ft.Container(
            content=formulario,
            padding=20,
            margin=ft.margin.symmetric(horizontal=20),
            width=20,
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

    async def ocultar_mensaje():
        await asyncio.sleep(1.5)  # Tiempo en segundos
        mensaje.value = ""
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

        # Validación de fecha
        fecha = campos["fecha_historia"].value.strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            mensaje.value = "La fecha debe tener el formato YYYY-MM-DD."
            mensaje.color = ft.Colors.RED
            page.update()
            return
        try:
            anio, mes, dia = map(int, fecha.split("-"))
            if not (1 <= mes <= 12):
                raise ValueError
            if not (1 <= dia <= 31):
                raise ValueError
        except Exception:
            mensaje.value = "La fecha debe ser válida (año, mes 1-12, día 1-31)."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        nombre_archivo = nombre.replace(" ", "_") + ".md"
        ruta_archivo = os.path.join(RUTA_HISTORIAS, nombre_archivo)

        # Estructura Markdown
        contenido = f"# Historia Clínica\n\n"
        contenido += f"## Datos personales\n\n"
        for k in [
            "documento", "cama", "fecha_historia", "eps",
            "nombre", "estado_civil", "fecha_nacimiento", "edad", "sexo", "hemoclasificacion",
            "ocupacion", "escolaridad", "direccion", "nombre_acompanante", "parentesco_acompanante", "fuente_info"
        ]:
            contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"

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
        for linea in datos['plan_manejo'].splitlines():
            if linea.strip():
                contenido += f"- {linea.strip()}\n"

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
            page.update()
            # Mostrar la lista inmediatamente después de guardar
            mostrar_lista()

            # Si quieres que el mensaje desaparezca después de volver a la lista:
            page.run_task(ocultar_mensaje)

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



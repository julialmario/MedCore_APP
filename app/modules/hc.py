import os
import flet as ft
import asyncio
import re

RUTA_HISTORIAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "historias_clinicas"))
os.makedirs(RUTA_HISTORIAS, exist_ok=True)

FORMATOS_HC = ["General", "Pediátrico"]
formato_seleccionado = {"valor": FORMATOS_HC[0]}

def pantalla_historia_clinica(page: ft.Page):
    mensaje = ft.Text("", color=ft.Colors.GREEN, text_align=ft.TextAlign.CENTER)
    vista_principal = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    autoguardado_activo = {"activo": False}

    async def autoguardado_loop():
        while autoguardado_activo["activo"]:
            guardar_historia(None, autoguardado=True)
            await asyncio.sleep(1)

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

    # Campos adicionales para pediatría
    campos.update({
        "hijo_de": ft.TextField(label="Hijo de"),
        "documento_ped": ft.TextField(label="Documento"),
        "episodio": ft.TextField(label="Episodio"),
        "edad_materna": ft.TextField(label="Edad materna"),
        "hemoclasificacion_ped": ft.TextField(label="Hemoclasificación"),
        "edad_gestacional": ft.TextField(label="Edad gestacional"),
        "fum": ft.TextField(label="FUM"),
        "gestaciones": ft.TextField(label="Gestaciones"),
        "controles_prenatales": ft.TextField(label="Controles prenatales"),
        "vacunacion": ft.TextField(label="Vacunación"),
        "ultima_ecografia": ft.TextField(label="Última ecografía"),
        "ag_shb": ft.TextField(label="Ag-SHB"),
        "vih": ft.TextField(label="VIH"),
        "prueba_no_treponemica": ft.TextField(label="Prueba no treponemica materna"),
        "prueba_treponemica": ft.TextField(label="Prueba treponemica materna"),
        "toxoplasma": ft.TextField(label="Toxoplasma"),
        "ptog": ft.TextField(label="PTOG"),
        "cultivo_estreptococo": ft.TextField(label="Cultivo rectovaginal para estreptococo B agalactiae"),
        "paraclinicos_maternos": ft.TextField(label="Paraclínicos maternos", multiline=True, max_lines=2),
        "ginecobstetricos": ft.TextField(label="Ginecobstetricos"),
        "patologicos_ped": ft.TextField(label="Patológicos"),
        "quirurgicos_ped": ft.TextField(label="Quirúrgicos"),
        "alergicos_ped": ft.TextField(label="Alérgicos"),
        "toxicos": ft.TextField(label="Tóxicos"),
        "farmacologicos": ft.TextField(label="Farmacológicos"),
        "familiares_ped": ft.TextField(label="Familiares"),
        "ruptura_membranas": ft.TextField(label="Ruptura de membranas"),
        "analgesia_epidural": ft.TextField(label="Analgesia epidural"),
        "medicamentos_ped": ft.TextField(label="Medicamentos"),
        "maduracion_fetal": ft.TextField(label="Maduración fetal"),
        "sexo_bebe": ft.TextField(label="Sexo del bebé"),
        "fecha_nacimiento_bebe": ft.TextField(label="Fecha de nacimiento"),
        "hora_nacimiento_bebe": ft.TextField(label="Hora de nacimiento"),
        "tipo_parto": ft.TextField(label="Tipo de parto"),
        "liquido_amniotico": ft.TextField(label="Líquido amniótico"),
        "adaptacion_neonatal": ft.TextField(label="Adaptación neonatal", multiline=True, max_lines=3),
        "apgar_minuto": ft.TextField(label="Apgar al minuto"),
        "apgar_5min": ft.TextField(label="Apgar a los 5 minutos"),
        "apgar_otros": ft.TextField(label="Apgar otros minutos"),
        "ballard": ft.TextField(label="Ballard (semanas)"),
        "peso_gramos": ft.TextField(label="Peso (g)"),
        "peso_percentil": ft.TextField(label="Peso (percentil)"),
        "talla_cm": ft.TextField(label="Talla (cm)"),
        "talla_percentil": ft.TextField(label="Talla (percentil)"),
        "pc_cm": ft.TextField(label="PC (cm)"),
        "pc_percentil": ft.TextField(label="PC (percentil)"),
        "pt_cm": ft.TextField(label="PT (cm)"),
        "pa_cm": ft.TextField(label="PA (cm)"),
        "diuresis": ft.TextField(label="Diuresis"),
        "meconio": ft.TextField(label="Meconio"),
        "diagnosticos_ped": ft.TextField(label="Diagnósticos", multiline=True, max_lines=2),
        "plan_ped": ft.TextField(label="Plan", multiline=True, max_lines=3),
    })

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

        # Mensaje informativo solo al crear una nueva historia
        if not editar:
            mensaje.value = "Para poder guardar automáticamente debes completar los datos personales obligatorios."
            mensaje.color = ft.Colors.BLUE
        else:
            mensaje.value = ""
            mensaje.color = ft.Colors.GREEN

        # Inicia el autoguardado
        autoguardado_activo["activo"] = True
        page.run_task(autoguardado_loop)

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
        if formato_seleccionado["valor"] == "General":
            formulario = ft.Column(
                controls=[
                    dropdown_formato,  # <-- Agrega esto arriba
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
        elif formato_seleccionado["valor"] == "Pediátrico":
            formulario = ft.Column(
                controls=[
                    dropdown_formato,
                    mensaje,
                    ft.Row(
                        controls=[
                            ft.Text("Historia Clínica Pediátrica", size=24, weight="bold", expand=True),
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
                    ft.Text("Datos maternos y perinatales", weight="bold"),
                    campos["hijo_de"], campos["documento_ped"], campos["episodio"], campos["edad_materna"], campos["hemoclasificacion_ped"],
                    campos["edad_gestacional"], campos["fum"], campos["gestaciones"], campos["controles_prenatales"], campos["vacunacion"],
                    ft.Text("Última ecografía", weight="bold"),
                    campos["ultima_ecografia"],
                    ft.Text("ETS maternas", weight="bold"),
                    campos["ag_shb"], campos["vih"], campos["prueba_no_treponemica"], campos["prueba_treponemica"], campos["toxoplasma"], campos["ptog"], campos["cultivo_estreptococo"],
                    campos["paraclinicos_maternos"],
                    ft.Text("Antecedentes personales", weight="bold"),
                    campos["ginecobstetricos"], campos["patologicos_ped"], campos["quirurgicos_ped"], campos["alergicos_ped"], campos["toxicos"], campos["farmacologicos"], campos["familiares_ped"],
                    campos["ruptura_membranas"], campos["analgesia_epidural"], campos["medicamentos_ped"], campos["maduracion_fetal"],
                    ft.Text("Nacimiento", weight="bold"),
                    campos["sexo_bebe"], campos["fecha_nacimiento_bebe"], campos["hora_nacimiento_bebe"], campos["tipo_parto"], campos["liquido_amniotico"],
                    ft.Text("Adaptación neonatal", weight="bold"),
                    campos["adaptacion_neonatal"],
                    ft.Text("Examen físico", weight="bold"),
                    campos["apgar_minuto"], campos["apgar_5min"], campos["apgar_otros"], campos["ballard"],
                    campos["peso_gramos"], campos["peso_percentil"], campos["talla_cm"], campos["talla_percentil"],
                    campos["pc_cm"], campos["pc_percentil"], campos["pt_cm"], campos["pa_cm"],
                    campos["diuresis"], campos["meconio"],
                    ft.Text("Diagnósticos", weight="bold"),
                    campos["diagnosticos_ped"],
                    ft.Text("Plan", weight="bold"),
                    campos["plan_ped"],
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

    def guardar_historia(e, autoguardado=False):
        datos = {k: v.value for k, v in campos.items()}
        formato = formato_seleccionado["valor"]

        if formato == "General":
            nombre = campos["nombre"].value.strip()
            edad = campos["edad"].value.strip()
            if not nombre or not edad:
                if not autoguardado:
                    mensaje.value = "Debes ingresar el nombre y apellidos del paciente y la edad."
                    mensaje.color = ft.Colors.RED
                    page.update()
                return
        elif formato == "Pediátrico":
            hijo_de = campos["hijo_de"].value.strip()
            edad_gestacional = campos["edad_gestacional"].value.strip()
            if not hijo_de or not edad_gestacional:
                if not autoguardado:
                    mensaje.value = "Debes ingresar los campos 'Hijo de' y 'Edad gestacional'."
                    mensaje.color = ft.Colors.RED
                    page.update()
                return
            nombre = hijo_de  # Para el nombre del archivo

        nombre_archivo = nombre.replace(" ", "_") + ".md"
        ruta_archivo = os.path.join(RUTA_HISTORIAS, nombre_archivo)

        # Estructura Markdown
        contenido = f"<!-- FORMATO: {formato} -->\n"  # <--- Guarda el formato aquí
        contenido += f"# Historia Clínica\n\n"

        if formato == "General":
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
        elif formato == "Pediátrico":
            contenido += f"## Datos maternos y perinatales\n"
            for k in [
                "hijo_de", "documento_ped", "episodio", "edad_materna", "hemoclasificacion_ped",
                "edad_gestacional", "fum", "gestaciones", "controles_prenatales", "vacunacion"
            ]:
                contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"
            contenido += "\n### Última ecografía\n"
            contenido += f"- **{campos['ultima_ecografia'].label}:** {datos.get('ultima_ecografia', '')}\n"
            contenido += "\n### ETS maternas\n"
            for k in [
                "ag_shb", "vih", "prueba_no_treponemica", "prueba_treponemica", "toxoplasma", "ptog", "cultivo_estreptococo"
            ]:
                contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"
            contenido += f"- **{campos['paraclinicos_maternos'].label}:** {datos.get('paraclinicos_maternos', '')}\n"
            contenido += "\n### Antecedentes personales\n"
            for k in [
                "ginecobstetricos", "patologicos_ped", "quirurgicos_ped", "alergicos_ped", "toxicos", "farmacologicos", "familiares_ped",
                "ruptura_membranas", "analgesia_epidural", "medicamentos_ped", "maduracion_fetal"
            ]:
                contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"
            contenido += "\n### Nacimiento\n"
            for k in [
                "sexo_bebe", "fecha_nacimiento_bebe", "hora_nacimiento_bebe", "tipo_parto", "liquido_amniotico"
            ]:
                contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"
            contenido += "\n### Adaptación neonatal\n"
            contenido += f"- **{campos['adaptacion_neonatal'].label}:** {datos.get('adaptacion_neonatal', '')}\n"
            contenido += "\n### Examen físico\n"
            for k in [
                "apgar_minuto", "apgar_5min", "apgar_otros", "ballard", "peso_gramos", "peso_percentil", "talla_cm", "talla_percentil",
                "pc_cm", "pc_percentil", "pt_cm", "pa_cm", "diuresis", "meconio"
            ]:
                contenido += f"- **{campos[k].label}:** {datos.get(k, '')}\n"
            contenido += "\n### Diagnósticos\n"
            contenido += f"{datos.get('diagnosticos_ped', '')}\n"
            contenido += "\n### Plan\n"
            contenido += f"{datos.get('plan_ped', '')}\n"

        try:
            if archivo_actual and archivo_actual != nombre_archivo:
                os.remove(os.path.join(RUTA_HISTORIAS, archivo_actual))
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido)

            # Limpiar mensaje después de guardar correctamente
            mensaje.value = ""
            page.update()

            if not autoguardado:
                mensaje.value = "Historia guardada correctamente."
                mensaje.color = ft.Colors.GREEN
                page.update()
                page.run_task(ocultar_mensaje)
            # Si es autoguardado, no mostrar mensaje

        except Exception as err:
            mensaje.value = f"Error al guardar: {err}"
            mensaje.color = ft.Colors.RED
            page.update()

    async def limpiar_mensaje_si_valido():
        await asyncio.sleep(1)
        mensaje.value = ""
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
        # Detiene el autoguardado al salir del formulario
        autoguardado_activo["activo"] = False
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

    def on_formato_change(e):
        formato_seleccionado["valor"] = e.control.value
        mostrar_formulario()  # Recarga el formulario con el nuevo formato

    dropdown_formato = ft.Dropdown(
        label="Formato de historia clínica",
        value=formato_seleccionado["valor"],
        options=[ft.dropdown.Option(f) for f in FORMATOS_HC],
        on_change=on_formato_change,
        expand=True
    )

    mostrar_lista()
    return vista_principal

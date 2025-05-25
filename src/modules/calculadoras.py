import flet as ft
from modules.navigation import *


PRIMARY_COLOR = ft.Colors.BLUE_GREY_900
SECONDARY_COLOR = ft.Colors.INDIGO_900
TEXT_COLOR = ft.Colors.CYAN_50

def imc():
    peso_field = ft.TextField(
        label="Peso (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )

    talla_field = ft.TextField(
        label="Talla (m)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )

    resultado_imc = ft.Text("IMC: -")
    categoria_imc = ft.Text("Categoría: -")

    def calcular_imc(e):
        try:
            peso = float(peso_field.value)
            talla = float(talla_field.value)
            imc_valor = peso / (talla ** 2)
            resultado_imc.value = f"IMC: {imc_valor:.2f}"

            # Clasificación según valor
            if imc_valor < 18.5:
                categoria = "Bajo peso"
            elif 18.5 <= imc_valor <= 24.9:
                categoria = "Normal"
            elif 25.0 <= imc_valor <= 29.9:
                categoria = "Sobrepeso"
            else:
                categoria = "Obesidad"

            categoria_imc.value = f"Categoría: {categoria}"
        except (ValueError, ZeroDivisionError):
            resultado_imc.value = "IMC: Valor inválido"
            categoria_imc.value = "Categoría: -"
        resultado_imc.update()
        categoria_imc.update()

    # Eventos de cambio
    peso_field.on_change = calcular_imc
    talla_field.on_change = calcular_imc

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        # El panel está expandido si su propiedad expanded es True
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        # Resetear campos al cerrar
        if not is_expanded:
            peso_field.value = ""
            talla_field.value = ""
            resultado_imc.value = "IMC: -"
            categoria_imc.value = "Categoría: -"
            peso_field.update()
            talla_field.update()
            resultado_imc.update()
            categoria_imc.update()


    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(title=ft.Text("IMC"),text_color=TEXT_COLOR),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            peso_field,
                            talla_field,
                            resultado_imc,
                            categoria_imc
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.symmetric(vertical=25),
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                expanded=False,
            )
        ],
    )


def regla_de_tres():
    a_field = ft.TextField(
        hint_text="A", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER
    )
    b_field = ft.TextField(
        hint_text="B", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER
    )
    y_field = ft.TextField(
        hint_text="Y", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER
    )
    resultado_x = ft.Text("X", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, size=20, text_align=ft.TextAlign.CENTER)

    enter = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER, size=0, text_align=ft.TextAlign.CENTER)

    formula_text = ft.Text(
        "Fórmula usada: X = (Y × B) / A",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )
    resultado_valor = ft.Text(
        "X: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_regla_de_tres(e):
        try:
            if not a_field.value or not b_field.value or not y_field.value:
                raise ValueError("Faltan valores")

            a = float(a_field.value)
            b = float(b_field.value)
            y = float(y_field.value)

            if a == 0:
                raise ZeroDivisionError

            x = (y * b) / a
            resultado_x.value = f"{x:.2f}"
            resultado_valor.value = f"X: {x:.2f}"
            formula_text.value = f"Fórmula usada: X = ({y} x {b}) / {a} = {x:.2f}"
        except (ValueError, ZeroDivisionError):
            resultado_x.value = "X"
            resultado_valor.value = "X: Valor inválido"
            formula_text.value = "Fórmula usada: X = (Y x B) / A"
        finally:
            if resultado_x.page:
                resultado_x.update()
            if resultado_valor.page:
                resultado_valor.update()
            if formula_text.page:
                formula_text.update()

    a_field.on_change = calcular_regla_de_tres
    b_field.on_change = calcular_regla_de_tres
    y_field.on_change = calcular_regla_de_tres

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            a_field.value = ""
            b_field.value = ""
            y_field.value = ""
            resultado_x.value = "X"
            resultado_valor.value = "X: -"
            formula_text.value = "Fórmula usada: X = (Y × B) / A"
            a_field.update()
            b_field.update()
            y_field.update()
            resultado_x.update()
            resultado_valor.update()
            formula_text.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(title=ft.Text("Regla de tres (Directa)", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        [a_field, b_field],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4
                                    ),
                                    ft.Container(
                                        content=ft.Text(" = ", size=25, color=TEXT_COLOR),
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Column(
                                        [y_field, enter, resultado_x],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(bottom=25)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )


def tfg_schwartz():
    altura_field = ft.TextField(
        label="Altura (cm)",
        hint_text="Ej: 60",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    creatinina_field = ft.TextField(
        label="Creatinina sérica (mg/dL)",
        hint_text="Ej: 0.8",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    k_selector = ft.Dropdown(
        label="Tipo de paciente",
        options=[
            ft.dropdown.Option("Término k = 0.33"),
            ft.dropdown.Option("Prematuro k = 0.45")
        ],
        value="Término k = 0.33",
        width=250
    )

    resultado_texto = ft.Text(
        "TFGe: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: TFGe = (k x Altura) / Creatinina",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_tfge(e):
        try:
            altura = float(altura_field.value)
            creatinina = float(creatinina_field.value)
            k = 0.33 if k_selector.value == "Término k = 0.33" else 0.45

            if creatinina == 0:
                raise ZeroDivisionError

            tfge = (k * altura) / creatinina
            resultado_texto.value = f"TFGe: {tfge:.2f} mL/min/1.73m²"
            formula_text.value = f"Fórmula usada: TFGe = ({k} × {altura}) / {creatinina} = {tfge:.2f}"
        except (ValueError, ZeroDivisionError):
            resultado_texto.value = "TFGe: Valor inválido"
            formula_text.value = "Fórmula usada: TFGe = k × Altura / Creatinina"

        resultado_texto.update()
        formula_text.update()

    altura_field.on_change = calcular_tfge
    creatinina_field.on_change = calcular_tfge
    k_selector.on_change = calcular_tfge

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            altura_field.value = ""
            creatinina_field.value = ""
            k_selector.value = "Término k = 0.33"
            resultado_texto.value = "TFGe: -"
            formula_text.value = "Fórmula usada: TFGe = (k x Altura) / Creatinina"
            altura_field.update()
            creatinina_field.update()
            k_selector.update()
            resultado_texto.update()
            formula_text.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("TFG Ecuación de Schwartz 2009", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column(
                                controls=[
                                    altura_field,
                                    creatinina_field,
                                    k_selector,
                                ],
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row([resultado_texto], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def talla_medioparental():
    tallapadre_field = ft.TextField(
        label="Talla del padre (cm)",
        hint_text="Ej: 170",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    tallamadre_field = ft.TextField(
        label="Talla de la madre (cm)",
        hint_text="Ej: 160",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    k_selector = ft.Dropdown(
        label="Sexo del paciente",
        options=[
            ft.dropdown.Option("Niño k = +6.5cm"),
            ft.dropdown.Option("Niña k = -6.5cm")
        ],
        value="Niño k = +6.5cm",
        width=250
    )

    resultado_texto = ft.Text(
        "Talla medioparental estimada",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_talla(e):
        try:
            talla_padre = float(tallapadre_field.value)
            talla_madre = float(tallamadre_field.value)
            k = 6.5 if "Niño" in k_selector.value else -6.5

            talla_mp = ((talla_padre + talla_madre) / 2) + k
            resultado_texto.value = f"Talla estimada: {talla_mp:.1f} cm"
            formula_text.value = (
                f"Fórmula usada: (({talla_padre} + {talla_madre}) / 2) {'+' if k > 0 else '-'} 6.5 = {talla_mp:.1f} cm"
            )
        except ValueError:
            resultado_texto.value = "Talla estimada: Valor inválido"
            formula_text.value = "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm"

        resultado_texto.update()
        formula_text.update()

    tallapadre_field.on_change = calcular_talla
    tallamadre_field.on_change = calcular_talla
    k_selector.on_change = calcular_talla

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            tallapadre_field.value = ""
            tallamadre_field.value = ""
            k_selector.value = "Niño k = +6.5cm"
            resultado_texto.value = "Talla medioparental estimada"
            formula_text.value = "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm"
            tallapadre_field.update()
            tallamadre_field.update()
            k_selector.update()
            resultado_texto.update()
            formula_text.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Talla medioparental", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column(
                                controls=[
                                    tallapadre_field,
                                    tallamadre_field,
                                    k_selector,
                                ],
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row([resultado_texto], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def slicc_page():
    criterios_clinicos = [
        "Lupus cutáneo agudo",
        "Lupus cutáneo crónico",
        "Úlceras orales o nasales",
        "Alopecia no cicatricial",
        "Artritis",
        "Serositis (pleuritis o pericarditis)",
        "Nefritis lúpica",
        "Alteración neurológica (convulsiones o psicosis)",
        "Anemia hemolítica",
        "Leucopenia (< 4000) o linfopenia (< 1000)",
        "Trombocitopenia (< 100,000)"
    ]

    criterios_inmunologicos = [
        "ANA positivo",
        "Anti-DNA positivo",
        "Anti-Sm positivo",
        "Antifosfolípidos positivos",
        "Disminución de C3 y/o C4",
        "Prueba de Coombs directa positiva (sin anemia hemolítica)"
    ]

    resultado = ft.Text(
        "Selecciona criterios para evaluar diagnóstico.",
        size=16,
        text_align=ft.TextAlign.CENTER,
        color=TEXT_COLOR
    )

    # Listas para almacenar checkboxes
    checks_clinicos = []
    checks_inmuno = []

    def evaluar(e=None):
        count_clinicos = sum(1 for c in checks_clinicos if c.value)
        count_inmuno = sum(1 for c in checks_inmuno if c.value)
        total = count_clinicos + count_inmuno

        # Validar si tiene Nefritis lúpica + ANA o Anti-DNA positivo
        tiene_nefritis = checks_clinicos[6].value  # Nefritis lúpica
        ana_positivo = checks_inmuno[0].value      # ANA positivo
        anti_dna = checks_inmuno[1].value          # Anti-DNA positivo

        if total >= 4 and count_clinicos >= 1 and count_inmuno >= 1:
            resultado.value = (
                f"✅ Diagnóstico posible de LES (criterios ≥4).\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "green"
        elif tiene_nefritis and (ana_positivo or anti_dna):
            resultado.value = (
                f"✅ Diagnóstico posible de LES (nefritis lúpica + ANA o Anti-DNA positivo).\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "green"
        else:
            resultado.value = (
                f"❌ No cumple criterios diagnósticos.\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "red"

        resultado.update()

    # Crear checkboxes con on_change automático
    checks_clinicos.extend([ft.Checkbox(label=c, on_change=evaluar) for c in criterios_clinicos])
    checks_inmuno.extend([ft.Checkbox(label=c, on_change=evaluar) for c in criterios_inmunologicos])

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for c in checks_clinicos + checks_inmuno:
                c.value = False
                c.update()
            resultado.value = "Selecciona criterios para evaluar diagnóstico."
            resultado.color = TEXT_COLOR
            resultado.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Criterios SLICC para diagnóstico de LES", color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("🩺 Criterios clínicos", weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                            ft.Column(controls=checks_clinicos, spacing=4),
                            ft.Divider(),
                            ft.Text("🧪 Criterios inmunológicos", weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                            ft.Column(controls=checks_inmuno, spacing=4),
                            ft.Divider(),
                            resultado
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def qsofa():
    switch_frecuencia = ft.Switch(value=False)
    switch_presion = ft.Switch(value=False)
    switch_estado_mental = ft.Switch(value=False)

    resultado_qsofa = ft.Text("Puntuación qSOFA: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_qsofa = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_qsofa(e):
        puntos = 0
        if switch_frecuencia.value:
            puntos += 1
        if switch_presion.value:
            puntos += 1
        if switch_estado_mental.value:
            puntos += 1

        resultado_qsofa.value = f"Puntuación qSOFA: {puntos}"

        if puntos >= 2:
            interpretacion = "Riesgo elevado de sepsis grave o muerte"
        else:
            interpretacion = "Riesgo bajo (seguir evaluando)"

        interpretacion_qsofa.value = f"Interpretación: {interpretacion}"

        resultado_qsofa.update()
        interpretacion_qsofa.update()

    switch_frecuencia.on_change = calcular_qsofa
    switch_presion.on_change = calcular_qsofa
    switch_estado_mental.on_change = calcular_qsofa

    def fila_criterio(texto, switch):
        return ft.Row(
            controls=[
                ft.Text(texto, expand=True, color=TEXT_COLOR),
                switch
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            switch_frecuencia.value = False
            switch_presion.value = False
            switch_estado_mental.value = False
            resultado_qsofa.value = "Puntuación qSOFA: -"
            interpretacion_qsofa.value = "Interpretación: -"
            switch_frecuencia.update()
            switch_presion.update()
            switch_estado_mental.update()
            resultado_qsofa.update()
            interpretacion_qsofa.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(title=ft.Text("qSOFA (Sepsis)", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            fila_criterio("Frecuencia respiratoria ≥ 22 rpm", switch_frecuencia),
                            fila_criterio("Presión sistólica ≤ 100 mmHg", switch_presion),
                            fila_criterio("Estado mental alterado (Glasgow < 15)", switch_estado_mental),
                            resultado_qsofa,
                            interpretacion_qsofa
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=100),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def sofa_score():
    opciones_sofa = {
        "PaO₂/FiO₂": ["≥400", "300–399", "200–299 (sin VM)", "100–199 (con VM)", "<100 (con VM)"],
        "Plaquetas (x10³/µL)": ["≥150", "100–149", "50–99", "20–49", "<20"],
        "Glasgow Coma Scale": ["15", "13–14", "10–12", "6–9", "<6"],
        "Bilirrubina (mg/dL)": ["<1.2", "1.2–1.9", "2.0–5.9", "6.0–11.9", "≥12.0"],
        "Presión media / Vasopresores": [
            "No hipotensión",
            "MAP <70 mmHg",
            "Dopamina ≤5 o Dobutamina (cualquier dosis)",
            "Dopamina >5 o Nor/Epinefrina ≤0.1",
            "Dopamina >15 o Nor/Epinefrina >0.1"
        ],
        "Creatinina / diuresis": [
            "<1.2 mg/dL o diuresis normal",
            "1.2–1.9 mg/dL",
            "2.0–3.4 mg/dL",
            "3.5–4.9 mg/dL o diuresis <500 mL/día",
            "≥5.0 mg/dL o diuresis <200 mL/día"
        ]
    }

    selectores = {}
    for criterio in opciones_sofa:
        selectores[criterio] = ft.Dropdown(
            options=[ft.dropdown.Option(opcion) for opcion in opciones_sofa[criterio]],
            label=criterio,
            width=400
        )

    resultado_sofa = ft.Text("Puntuación SOFA: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_sofa = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_sofa(e):
        puntuacion = 0
        for criterio, dropdown in selectores.items():
            indice = dropdown.options.index(next(opt for opt in dropdown.options if opt.key == dropdown.value)) if dropdown.value else 0
            puntuacion += indice

        resultado_sofa.value = f"Puntuación SOFA: {puntuacion}"

        if puntuacion >= 2:
            interpretacion = "Riesgo elevado de disfunción orgánica (evaluar sepsis)"
        else:
            interpretacion = "Riesgo bajo"

        interpretacion_sofa.value = f"Interpretación: {interpretacion}"
        resultado_sofa.update()
        interpretacion_sofa.update()

    for dropdown in selectores.values():
        dropdown.on_change = calcular_sofa

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for d in selectores.values():
                d.value = None
                d.update()
            resultado_sofa.value = "Puntuación SOFA: -"
            interpretacion_sofa.value = "Interpretación: -"
            resultado_sofa.update()
            interpretacion_sofa.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(title=ft.Text("SOFA Score (Sepsis)", color=TEXT_COLOR)),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [resultado_sofa, interpretacion_sofa],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )


calculadoras = [
        {
            "titulo": "Indice de masa corporal",
            "tags": ["imc", "peso", "altura", "nutrición", "bmi"],
            "componente": imc()
        },
        {
            "titulo": "Regla de tres (Directa)",
            "tags": ["proporciones", "aritmética", "matemática"],
            "componente": regla_de_tres()
        },
        {
            "titulo": "Talla medio parental",
            "tags": ["crecimiento", "niños", "pediatría", "estatura", "genética"],
            "componente": talla_medioparental()
        },
        {
            "titulo": "TFG Ecuación de Schwartz 2009",
            "tags": ["nefrología", "función renal", "schwartz", "creatinina", "riñón"],
            "componente": tfg_schwartz()
        },
        {
            "titulo": "Criterios SLICC para diagnóstico de LES",
            "tags": ["lupus", "inmunologia", "criterios"],
            "componente": slicc_page()
        },
        {
            "titulo": "qSOFA (Sepsis)",
            "tags": ["sepsis", "adultos", "criterios"],
            "componente": qsofa()
        },
        {
            "titulo": "Sofa Score (Sepsis)",
            "tags": ["sepsis", "adultos", "criterios"],
            "componente": sofa_score()
        },
    ]
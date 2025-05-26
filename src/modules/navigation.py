import flet as ft


def nav(page, page_change):
    drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        selected_index=0,
        on_change=page_change,
        controls=[
            ft.Container(width=10, height=10),
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.HOME),
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED_OUTLINED),
                label="Medicamentos",
                selected_icon=ft.Icons.FORMAT_LIST_BULLETED,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.CALCULATE_OUTLINED),
                label="Calculadoras",
                selected_icon=ft.Icons.CALCULATE,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Laboratorios",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
                ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Historias clinica",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Informacion",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
        ],
    )

    bar = ft.AppBar(
        leading=ft.Container(content=ft.Icon(ft.Icons.MEDICAL_SERVICES), padding=ft.padding.only(left=12)),
        leading_width=30,
        title=ft.Text("MedCore"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.Container(content=ft.Row(
        controls=[
            ft.IconButton(
                width=40,
                height=40,
                style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                content=ft.Row(
                   [ft.Icon(name=ft.Icons.FORMAT_LIST_BULLETED, color=ft.Colors.WHITE)],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND),
                on_click=lambda e: page.open(drawer)
            )
        ],
        alignment=ft.MainAxisAlignment.END
    ), padding=ft.padding.only(right=12))
        ]
    )
    return bar, drawer

def search_bar(filtrar, buscar, selecciona):
    search = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text=buscar,
        view_hint_text=selecciona,
        on_change=filtrar,
        controls=[],
        expand=True,
    )
    return ft.Container(
        content=search,
        expand=True,
        alignment=ft.alignment.center,
    )

def list_content_search(list_content):
    list_content.sort(key=lambda x: x["titulo"].lower())

    list_container = ft.Column(expand=True, spacing=20)
    buscar = "Buscar..."
    selecciona = "Selecciona..."

    def build_list(filtered_items):
        list_container.controls.clear()
        for cont in filtered_items:
            list_container.controls.append(cont["componente"])
        list_container.update()

    def filtrar_calculadoras(e):
        filtro = e.control.value.lower()
        filtered_items = []
        for cont in list_content:
            titulo = cont["titulo"].lower()
            tags = " ".join(cont["tags"]).lower()
            if filtro in titulo or filtro in tags:
                filtered_items.append(cont)
        build_list(filtered_items)


    for cont in list_content:
        list_container.controls.append(cont["componente"])

    return ft.Column(
        controls=[
            search_bar(filtrar_calculadoras, buscar, selecciona),
            list_container
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        height=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



def list_content_search2(list_content):
    list_content.sort(key=lambda x: x["titulo"].lower())

    list_container = ft.Column(expand=True, spacing=20)
    buscar = "Buscar..."
    selecciona = "Selecciona..."

    # Construcción dinámica con encabezados por letra
    def build_list(filtered_items):
        list_container.controls.clear()
        current_letter = ""
        for cont in filtered_items:
            titulo = cont["titulo"]
            first_letter = titulo[0].upper()
            if first_letter != current_letter:
                current_letter = first_letter
                list_container.controls.append(
                    ft.Text(
                        value=current_letter,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    )
                )
            list_container.controls.append(cont["componente"])
        list_container.update()

    # Filtro por título o tags
    def filtrar_calculadoras(e):
        filtro = e.control.value.lower()
        filtered_items = []
        for cont in list_content:
            titulo = cont["titulo"].lower()
            tags = " ".join(cont["tags"]).lower()
            if filtro in titulo or filtro in tags:
                filtered_items.append(cont)
        build_list(filtered_items)

    # Construcción inicial sin update
    current_letter = ""
    for cont in list_content:
        titulo = cont["titulo"]
        first_letter = titulo[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            list_container.controls.append(
                ft.Text(
                    value=current_letter,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                )
            )
        list_container.controls.append(cont["componente"])

    return ft.Column(
        controls=[
            search_bar(filtrar_calculadoras, buscar, selecciona),
            list_container
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        height=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

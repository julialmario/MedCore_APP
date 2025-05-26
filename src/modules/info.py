import flet as ft
import webbrowser

def info_page():
    def web(e):
        webbrowser.open("https://julialmario.github.io/")

    my_web = ft.GestureDetector(
        content=ft.Image(
            src="../assets/myweb.png",
            width=150,
            height=50,
        ),
        on_tap=web,
    )
    
    def repository(e):
        webbrowser.open("https://github.com/julialmario/MedCore_APP")

    repositorio = ft.GestureDetector(
        content=ft.Image(
            src="../assets/repository.png",
            width=150,
            height=50,
        ),
        on_tap=repository,
    )

    images_row = ft.Row(
        controls=[my_web, repositorio],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    creador_info = ft.Column(
        controls=[
            ft.Text("MedCore", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Created by Julian Almario Loaiza", size=18),
            images_row,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    referencias = [
        "- Huerta Aragonés J, Cela de Julián E. Hematología práctica: interpretación del hemograma y de las pruebas de coagulación. En: AEPap (ed.). Curso de Actualización Pediatría 2018. Madrid: Lúa Ediciones 3.0; 2018. p. 507-526.",
        "- Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315(8):801–810. doi:10.1001/jama.2016.0287",
        "- Charles K, Lewis MJ, Montgomery E, Reid M. The 2021 Chronic Kidney Disease Epidemiology Collaboration Race-Free Estimated Glomerular Filtration Rate Equations in Kidney Disease: Leading the Way in Ending Disparities. Health Equity. 2024 Jan 12;8(1):39-45. doi: 10.1089/heq.2023.0038. PMID: 38250300; PMCID: PMC10797164."
    ]

    referencias_panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.WHITE,
        elevation=8,
        divider_color=ft.Colors.WHITE,
        controls=[
            ft.ExpansionPanel(
                header= ft.ListTile(
                    title=ft.Text("📚 Referencias bibliográficas", text_align=ft.TextAlign.LEFT)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[ft.Text(ref, size=14) for ref in referencias],
                        spacing=6
                    ),
                padding=ft.padding.all(20)
                    ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            )
        ]
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                creador_info,
                ft.Divider(thickness=1),
                referencias_panel,
            ],
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
            height=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(20),
        expand=True
    )


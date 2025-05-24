<div align="center">
    <img width="250" src="/src/assets/icon.png"/>
</div>

# MedCore

**MedCore** es una aplicación multiplataforma para **móviles, web y escritorio**, desarrollada en Python utilizando el framework [Flet](https://flet.dev). Está diseñada para brindar acceso rápido, organizado y práctico a herramientas esenciales para la práctica clínica y el estudio de las ciencias médicas.

Su propósito es centralizar calculadoras clínicas, valores de referencia paraclínicos y otros recursos útiles en una plataforma intuitiva, modular y eficiente, accesible desde diferentes dispositivos y entornos.


## 🩺 Características

* 🚀 **Uso inmediato sin necesidad de inicio de sesión**: ingresa y accede a las herramientas al instante.
* 🔎 **Búsqueda interactiva** por nombre o etiquetas, rápida y eficiente.
* ⭐ **Sistema de favoritos** para guardar tus recursos más utilizados.
* 🧮 **Calculadoras médicas** de uso frecuente en la práctica clínica.
* 🧪 **Valores normales paraclínicos**, organizados por edad y tipo de análisis.
* 💻 **Interfaz moderna, fluida y responsiva**, optimizada para escritorio, web y dispositivos móviles.
* 🌙 **Modo oscuro permanente**, ideal para entornos clínicos y sesiones de estudio prolongadas.
* 🧩 **Diseño modular**, con componentes reutilizables que facilitan su expansión futura.


## 🧰 Tecnologías utilizadas

* **Python 3.10+**
* **[Flet](https://flet.dev/)** – Framework para construir interfaces web y de escritorio con Python.
* **Arquitectura modular** y escalable para fácil mantenimiento y crecimiento del proyecto.



## 🚀 Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/Julian-Almario/medcore_app.git
cd medcore_app
```

2. Instala las dependencias necesarias:

```bash
pip install flet
```

3. Ejecuta la aplicación:

```bash
python main.py
```



## 📁 Estructura del proyecto

```
medcore_app/
│
├── main.py                 # Punto de entrada de la aplicación
└── src/
    ├── modules/            # Componentes reutilizables (paneles, tarjetas, búsqueda)
    ├── assets/             # Imágenes e íconos
├── LICENSE
└── README.md
```



## 🧪 Estado actual

* [ ] Valores de paraclínicos normales
    * [x] Hemograma
    * [ ] LCR
    * [ ] Uroanalisis
* [ ] Calculadoras médicas más usadas
* [x] Búsqueda interactiva por nombre o etiqueta
* [ ] Newsletter de guías Americanas, Europeas y Colombianas
* [ ] Creador de historias clínicas



## 📌 Objetivo

**MedCore** busca ser una herramienta de referencia para estudiantes de medicina, médicos generales y especialistas, al centralizar cálculos, valores normales y parámetros clave que agilizan la toma de decisiones clínicas.



## 🙌 Contribuciones

Las contribuciones están abiertas y son bienvenidas. Puedes:

* Sugerir mejoras o nuevas funciones
* Reportar errores o problemas
* Enviar *pull requests* con funcionalidades o correcciones



## 📄 Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License versión 3 (GPL v3)**, que permite usar, modificar y redistribuir el software bajo los términos de dicha licencia.

El autor original conserva los derechos de autor y la propiedad intelectual sobre MedCore.

Para más detalles, consulte la licencia completa en [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).

Consulta el archivo `LICENSE` para más detalles.
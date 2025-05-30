![Banner](img/banner.png)

# MedCore

**MedCore** es una aplicación multiplataforma para **móviles, web y escritorio**, desarrollada en Python utilizando el framework [Flet](https://flet.dev). Está diseñada para brindar acceso rápido, organizado y práctico a herramientas esenciales para la práctica clínica y el estudio de las ciencias médicas.

Su propósito es centralizar calculadoras clínicas, valores de referencia paraclínicos y otros recursos útiles en una plataforma intuitiva, modular y eficiente, accesible desde diferentes dispositivos y entornos.

<p align="center">
  <img src="https://img.shields.io/github/license/Julian-Almario/medcore_app" />
  <img src="https://img.shields.io/github/issues/Julian-Almario/medcore_app" />
  <img src="https://img.shields.io/github/stars/Julian-Almario/medcore_app" />
</p>

## 📚 Tabla de contenido

- [Características](#-características)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Estado actual](#-estado-actual)
- [Objetivo](#-objetivo)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

## 🩺 Características

* 🚀 **Uso inmediato sin necesidad de inicio de sesión**: ingresa y accede a las herramientas al instante.
* 🔎 **Búsqueda interactiva** por nombre o etiquetas, rápida y eficiente.
* 🧮 **Calculadoras médicas** de uso frecuente:
    * Índice de masa corporal (IMC)
    * Regla de tres (Directa)
    * Talla medio parental
    * TFG (Schwartz 2009)
    * Criterios SLICC para LES
    * qSOFA y SOFA Score (Sepsis)
    * CKD-EPI 2021
    * Anion Gap y Sodio corregido
    * **Entre otras**
* 🧪 **Valores normales paraclínicos**, organizados por edad y tipo de análisis.
* 📝 **Creador de historias clínicas** con exportación y edición.
* 📦 **Almacenamiento local** de datos, acceso offline completo.
* 💻 **Interfaz moderna, fluida y responsiva**, optimizada para escritorio, web y dispositivos móviles.
* 🌙 **Modo oscuro permanente**, ideal para entornos clínicos y sesiones de estudio prolongadas.
* 🧩 **Diseño modular**, con componentes reutilizables que facilitan su expansión futura.


## 🧰 Tecnologías utilizadas

* **Python 3.10+**
* **[Flet](https://flet.dev/)** – Framework para construir interfaces web y de escritorio con Python.
* **Arquitectura modular** y escalable para fácil mantenimiento y crecimiento del proyecto.



## 🚀 Instalación y ejecución

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/Julian-Almario/medcore_app.git
    cd medcore_app/src
    ```

2. **Instala las dependencias necesarias:**

    ```bash
    pip install flet
    ```

3. **Ejecuta la aplicación:**

    ```bash
    python main.py
    ```

> **Nota:** Se recomienda usar un entorno virtual para evitar conflictos de dependencias.



## 📁 Estructura del proyecto

```
medcore_app/
│
├── main.py                  # Punto de entrada de la aplicación
├── README.md                # Documentación principal
├── LICENSE                  # Licencia del proyecto
│
├── src/
│   ├── modules/             # Módulos y componentes reutilizables (paneles, tarjetas, búsqueda, calculadoras, etc.)
│   └── assets/              # Imágenes e íconos
│
├── storage/
│   └── data/
│       ├── historias_clinicas/   # Guardado de historias clínicas
│       └── pearls/               # Guías clínicas y perlas
│   └── temp/                # Archivos temporales
```



## 🧪 Estado actual

* [x] Acceso offline completo
* Valores de paraclínicos normales
    * [x] Hemograma
    * [ ] LCR
    * [ ] Uroanalisis
* Calculadoras médicas más usadas:
    * [x] Índice de masa corporal (IMC)
    * [x] Regla de tres (Directa)
    * [x] Talla medio parental
    * [x] TFG Ecuación de Schwartz 2009
    * [x] Criterios SLICC para diagnóstico de LES
    * [x] qSOFA (Sepsis)
    * [x] SOFA Score (Sepsis)
    * [x] CKD-EPI 2021
    * [x] Anion Gap
    * [x] Sodio corregido
* [ ] Base de datos medicamentos
* [x] Búsqueda interactiva por nombre o etiqueta
* [ ] Añade las guias que quieras para que todo este en un solo lugar
* [x] Creador de historias clínicas
    * [x] Elegir formatos de historias clinicas
    * [ ] Exportar historias clínicas a PDF/Markdown
    * [x] Autoguardado de historias clinicas
* [ ] Personalización de temas de color



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
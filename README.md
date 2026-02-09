SSG - Static Site GeneratorUn generador de sitios estáticos personalizado, ligero y escrito en Python. Este proyecto convierte una estructura de directorios de archivos Markdown en un sitio web HTML completo, gestionando activos estáticos y permitiendo configuraciones flexibles para despliegue (especialmente compatible con GitHub Pages).🚀 CaracterísticasConversión de Markdown a HTML: Transforma archivos .md en páginas .html limpias utilizando un parser personalizado.Generación Recursiva: Procesa directorios y subdirectorios dentro de la carpeta de contenido, manteniendo la estructura original.Gestión de Activos Estáticos: Copia automáticamente imágenes y hojas de estilo desde el directorio static al directorio de salida.Sistema de Plantillas: Utiliza un archivo template.html base para mantener un diseño consistente en todas las páginas, inyectando dinámicamente el título y el contenido.Soporte para Base Path: Permite configurar una ruta base (ej. /mi-repo/), ideal para desplegar en subdirectorios o GitHub Pages.Cross-Platform: Incluye scripts de construcción (build.sh) que detectan automáticamente el sistema operativo (Windows, Linux, macOS).📋 Requisitos PreviosPython 3.x: El núcleo del generador está escrito en Python.(Opcional) Git Bash o terminal compatible si estás en Windows para ejecutar el script .sh.📂 Estructura del ProyectoEl proyecto sigue una arquitectura clara separando la lógica, el contenido y la salida:.
├── content/          # Archivos Markdown de origen (Tu contenido va aquí)
├── static/           # Archivos estáticos (CSS, Imágenes)
├── src/              # Código fuente en Python
│   ├── main.py       # Punto de entrada principal
│   ├── generate_content.py # Lógica de generación de páginas
│   ├── copy_static.py      # Lógica de copiado de activos
│   └── ...           # Módulos de parsing (block, inline, html_node)
├── docs/             # SALIDA: Sitio web generado (configurado para GitHub Pages)
├── template.html     # Plantilla HTML base
├── build.sh          # Script de automatización de construcción
└── main.sh           # Script de ejecución principal
Nota: El directorio de salida está configurado como docs/ por defecto para facilitar la integración con la opción de publicación desde la carpeta /docs de GitHub Pages.🛠️ Instalación y UsoClonar el repositorio:git clone [https://github.com/tu-usuario/tu-repositorio-ssg.git](https://github.com/tu-usuario/tu-repositorio-ssg.git)
cd tu-repositorio-ssg
Agregar Contenido:Crea o edita archivos .md dentro de la carpeta content/.Asegúrate de que cada archivo Markdown comience con un encabezado H1 (# Título) para que el generador pueda extraer el título de la página correctamente.Generar el Sitio:Puedes utilizar el script de construcción incluido que detecta tu sistema operativo y configura la ruta base por defecto (actualmente configurada como /SSG/):./build.sh
O ejecutarlo manualmente con Python especificando la ruta base (o / para raíz):# Uso: python src/main.py <basepath>
python3 src/main.py "/"
⚙️ Configuración y PersonalizaciónCambiar la Ruta Base (Deploy en GitHub Pages)Si tu sitio no está en el dominio raíz (por ejemplo usuario.github.io/mi-proyecto), necesitas ajustar el argumento basepath.El script build.sh ya está preconfigurado para pasar /SSG/ como argumento. Edita este archivo si el nombre de tu repositorio es diferente:# En build.sh
python3 src/main.py "/nombre-de-tu-repo/"
Esto ajustará automáticamente todos los enlaces href y src en el HTML generado para que apunten correctamente a la subcarpeta.Modificar el DiseñoEdita el archivo template.html. El generador buscará y reemplazará los siguientes marcadores:{{ Title }}: Se reemplaza con el primer H1 encontrado en el Markdown.{{ Content }}: Se reemplaza con el HTML convertido del cuerpo del Markdown.📦 DespliegueEste generador coloca los archivos resultantes en la carpeta docs/.Sube tus cambios a GitHub.Ve a la configuración de tu repositorio (Settings) > Pages.En "Source", selecciona Deploy from a branch.En "Branch", selecciona main (o master) y la carpeta /docs.Guarda los cambios.🤝 ContribuciónLas contribuciones son bienvenidas. Por favor, asegúrate de actualizar las pruebas si modificas la lógica de parsing de Markdown.📄 LicenciaEste proyecto está bajo la Licencia MIT.MIT License

Copyright (c) 2024 Davinson Ortiz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

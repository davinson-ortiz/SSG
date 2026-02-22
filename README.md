# **Generador de Sitios Estáticos (SSG) en Python 🐍**

*Un generador de sitios estáticos personalizado construido desde cero utilizando Python. Este proyecto toma archivos escritos en Markdown, analiza su contenido (bloques y sintaxis en línea), y genera un sitio web HTML completamente funcional y listo para producción.*

## **Comenzando 🚀**

*Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.*

Mira **Despliegue** para conocer como desplegar el proyecto.

### **Pre-requisitos 📋**

*Para ejecutar este proyecto, solo necesitas tener instalado Python en tu sistema, ya que está construido utilizando las librerías estándar.*

* [Python 3.8+](https://www.python.org/downloads/)  
* Bash (para ejecutar los scripts .sh)

### **Instalación 🔧**

*Sigue estos pasos para tener un entorno de desarrollo ejecutándose:*

1. Clona el repositorio en tu máquina local:

git clone \[https://github.com/davinson-ortiz/ssg.git\](https://github.com/davinson-ortiz/ssg.git)  
cd ssg

2. Otorga permisos de ejecución a los scripts de shell (si estás en Linux/macOS):

chmod \+x main.sh build.sh test.sh

3. Ejecuta el script principal para construir el sitio y levantar un servidor local de pruebas:

./main.sh

*Este script típicamente limpiará el directorio de destino (docs/), copiará los archivos estáticos de static/, generará los archivos HTML a partir de content/ y levantará un servidor web en el puerto 8888 para previsualizar el resultado.*

## **Estructura del Proyecto 📁**

* /src: Contiene todo el código fuente en Python (main.py, analizadores de markdown, conversores de nodos, etc.).  
* /content: Archivos .md (Markdown) que conforman el contenido de las páginas y el blog.  
* /static: Archivos estáticos como imágenes (/images) y hojas de estilo (index.css).  
* /docs: Directorio de salida (output) donde se genera el sitio web en HTML.  
* template.html: Plantilla base HTML que envuelve el contenido convertido.

## **Ejecutando las pruebas ⚙️**

*Este proyecto cuenta con una suite completa de pruebas unitarias para garantizar que el parseo de Markdown a HTML funcione correctamente.*

### **Analice las pruebas unitarias 🔩**

*Las pruebas verifican la correcta conversión de nodos de texto, bloques de Markdown y la estructura HTML subyacente.*

Para ejecutar la suite de pruebas completa, simplemente corre el script de pruebas:

./test.sh

*O alternativamente, usando el módulo de pruebas de Python directamente:*

python3 \-m unittest discover \-s src

## **Despliegue 📦**

El directorio de salida está configurado por defecto como docs/. Esto hace que el proyecto esté listo de forma nativa para ser desplegado utilizando **GitHub Pages**.

Solo necesitas ir a los ajustes de tu repositorio en GitHub (Settings \> Pages), seleccionar la rama main y la carpeta /docs como origen (Source). Cada vez que generes tu sitio y hagas push, GitHub servirá tu web automáticamente.

## **Construido con 🛠️**

*Herramientas y tecnologías utilizadas en el desarrollo:*

* [Python](https://www.python.org/) \- El lenguaje principal de programación (Librerías estándar).  
* [Markdown](https://daringfireball.net/projects/markdown/) \- Lenguaje de marcado para la creación de contenido.  
* HTML5 & CSS3 \- Para el renderizado y estilos del sitio web.  
* Shell Script \- Para la automatización de la construcción y pruebas (.sh).

## **Contribuyendo 🖇️**

Por favor, envía un pull request si deseas agregar nuevas funcionalidades, como soporte para nuevas etiquetas Markdown o mejoras en el diseño de la plantilla.

## **Versionado 📌**

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://www.google.com/search?q=https://github.com/davinson-ortiz/ssg/tags).

## **Autores ✒️**

* **Davinson Ortiz** \- *Trabajo Inicial y Desarrollo* \- [davinson-ortiz](https://www.google.com/search?q=https://github.com/davinson-ortiz)

## **Licencia 📄**

Este proyecto está bajo la Licencia MIT \- mira el archivo [LICENSE.md](http://docs.google.com/LICENSE.md) para detalles.

## **Expresiones de Gratitud 🎁**

* Comenta a otros sobre este proyecto 📢  
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo si te ha servido de ayuda.  
* ¡Gracias por revisar este código\! 🤓
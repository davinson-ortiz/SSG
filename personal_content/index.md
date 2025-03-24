# QUE ES UN SSG

Un **SSG (Static Site Generator)** o **Generador de Sitios Estáticos** es una herramienta que convierte archivos de contenido, como Markdown o JSON, en un sitio web completamente estático. En lugar de generar páginas dinámicamente en el servidor cuando un usuario las solicita (como lo haría un CMS tradicional como WordPress), un SSG preprocesa y genera todas las páginas en HTML, CSS y JavaScript antes de ser publicadas en un servidor o CDN.

## 📌 ¿Cómo funciona un SSG?
El proceso de un **Static Site Generator** sigue tres etapas principales:

1. **Entrada**:  
   - Se toma contenido en formatos como **Markdown**, **JSON**, **YAML** o bases de datos ligeras.
   - Se combinan con **plantillas HTML** y estilos CSS para definir la estructura y apariencia del sitio.

2. **Generación**:  
   - El SSG procesa los archivos y **pre-renderiza** el sitio, generando archivos HTML estáticos listos para su distribución.

3. **Salida**:  
   - Se obtiene un conjunto de archivos estáticos (HTML, CSS, JS, imágenes, etc.) que pueden ser desplegados en **servidores estáticos** como GitHub Pages, Netlify, Vercel o incluso en un simple servidor Nginx o Apache.

## 🔥 Beneficios de usar un SSG

✅ **Rendimiento óptimo**  
   - Como el sitio está completamente estático, se sirve mucho más rápido desde una CDN sin necesidad de consultas a bases de datos.

✅ **Seguridad mejorada**  
   - No hay base de datos ni ejecución de código en el servidor, lo que reduce los puntos de ataque.

✅ **Menos costos y mantenimiento**  
   - Puede ser alojado en plataformas gratuitas o de bajo costo, sin necesidad de servidores complejos.

✅ **Escalabilidad**  
   - Funciona bien incluso con alto tráfico porque simplemente se sirven archivos estáticos.

✅ **Mejor SEO**  
   - El contenido es renderizado previamente, lo que facilita su indexación por motores de búsqueda.

## 🚀 Ejemplos de SSG populares

- **Next.js** (puede funcionar como SSG o SSR)
- **Gatsby** (enfocado en React)
- **Hugo** (rápido y basado en Go)
- **Jekyll** (usado en GitHub Pages, basado en Ruby)
- **Eleventy (11ty)** (ligero y flexible en JavaScript)
- **Nuxt.js** (para Vue.js, puede funcionar como SSG)


## 🎯 ¿Cuándo usar un SSG?
- **Blogs y sitios de documentación** (ej. la documentación de React usa Docusaurus).
- **Portafolios personales**.
- **Landing pages y sitios corporativos**.
- **E-commerce pequeños con pocos productos** (ej. Shopify usa SSG en algunas páginas).
- **Sitios donde el contenido no cambia constantemente**.

---

Si buscas una solución rápida, segura y fácil de mantener para tu sitio web, un **SSG** puede ser una gran opción. ¿Quieres ayuda para elegir uno o implementarlo en un proyecto? 🚀
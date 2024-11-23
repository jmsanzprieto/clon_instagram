
# FastAPI Project

Este es un proyecto basado en **FastAPI** que sirve una aplicación web utilizando plantillas HTML. 

## Estructura del proyecto

```
fastapi_project/
│
├── clon_instagram.py      # Archivo principal que arranca la aplicación
├── .env                   # Configuración del entorno
├── requirements.txt       # Dependencias del proyecto
├── templates/             # Carpeta que contiene las plantillas HTML
│   ├── index.html         # Página principal
│   ├── parts/             # Componentes reutilizables (header, footer)
│   │   ├── header.html    # Cabecera del sitio
│   │   └── footer.html    # Pie de página del sitio
│   ├── css/               # Archivos CSS
│   │   └── styles.css     # Estilos personalizados
│   └── js/                # Archivos JavaScript
│       └── app.js         # Scripts personalizados
```

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-proyecto.git
   ```

2. Accede al directorio del proyecto:
   ```bash
   cd fastapi_project
   ```

3. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Crea un archivo `.env` en la raíz del proyecto con la configuración básica:
   ```
   URL_BASE=http://127.0.0.1:8000/
   ```

6. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

7. Abre tu navegador y ve a la URL base:
   ```
   http://127.0.0.1:8000/
   ```

## Funcionalidades actuales

- Servir una página principal desde `index.html`.
- Incluir componentes reutilizables como `header.html` y `footer.html`.
- Servir archivos estáticos (CSS, JS).

## Tareas pendientes

- [ ] Implementar autenticación de usuarios.
- [ ] Crear rutas adicionales (e.g., `/login`, `/upload`).
- [ ] Añadir validaciones y formularios.
- [ ] Configurar una base de datos para almacenar información dinámica.

## Actualizaciones

### [Fecha] - Inicialización del proyecto
- Se creó la estructura básica del proyecto.
- Se configuró la ruta para la página de inicio (`/`).
- Se añadió soporte para archivos estáticos y plantillas parciales (`header.html`, `footer.html`).

### [Fecha] - Mejoras en la plantilla
- Se añadió un formulario para iniciar sesión (popup).
- Se añadió un formulario para cargar imágenes (popup).
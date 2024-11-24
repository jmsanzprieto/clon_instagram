# Proyecto de Gestión de Usuarios y Subida de Imágenes con FastAPI

Este proyecto es una aplicación web desarrollada con **FastAPI** que permite gestionar usuarios y la subida de imágenes. Los usuarios pueden registrarse, iniciar sesión y subir imágenes que se almacenan en el servidor, además de ser procesadas (como redimensionarlas).

## Requisitos

- Python 3.7 o superior
- FastAPI
- Uvicorn (para ejecutar el servidor)
- Pydantic
- Pillow (para el procesamiento de imágenes)
- Passlib (para la encriptación de contraseñas)
- PyJWT (para la generación de tokens JWT)
- Python-dotenv (para cargar variables de entorno desde un archivo `.env`)

## Instalación

1. Clona el repositorio en tu máquina local:

    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2. Crea un entorno virtual:

    ```bash
    python3 -m venv venv
    ```

3. Activa el entorno virtual:

    - En Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    - En Windows:

        ```bash
        venv\Scripts\activate
        ```

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

5. Crea un archivo `.env` con las siguientes variables de entorno:

    ```
    USERS_FILE=usuarios.json
    SECRET_KEY=mi_clave_secreta
    ALGORITHM=HS256
    ```

6. Ejecuta el servidor de desarrollo:

    ```bash
    uvicorn main:app --reload
    ```

    Esto iniciará el servidor en `http://127.0.0.1:8000`.

## Endpoints

### 1. **Registro de Usuario**

**Método:** `POST`  
**Ruta:** `/register`

Permite registrar un nuevo usuario. Los parámetros a enviar son:

- `username` (str): Nombre de usuario
- `password` (str): Contraseña

**Respuesta:**  
- `message`: Mensaje de éxito
- `id`: ID del usuario registrado

### 2. **Login**

**Método:** `POST`  
**Ruta:** `/login`

Permite a un usuario iniciar sesión y obtener un token JWT. Los parámetros a enviar son:

- `username` (str): Nombre de usuario
- `password` (str): Contraseña

**Respuesta:**  
- `access_token`: Token JWT generado
- `token_type`: Tipo de token (siempre "bearer")

### 3. **Subir Imagen**

**Método:** `POST`  
**Ruta:** `/upload-image`

Permite subir una imagen. Los parámetros a enviar son:

- `title` (str): Título de la imagen
- `image` (archivo): Imagen a cargar
- `authorization` (str): Token JWT en el encabezado Authorization

**Respuesta:**  
- `message`: Mensaje de éxito
- `data`: Información de la imagen subida (nombre, ruta y usuario)

### 4. **Ver Imágenes**

**Método:** `GET`  
**Ruta:** `/ver_imagenes`

Permite obtener todas las imágenes subidas por los usuarios.

**Respuesta:**  
- `images`: Lista con la información de todas las imágenes (nombre, ruta y título)

## Estructura de Archivos

- `main.py`: Código principal de la aplicación FastAPI.
- `functions.py`: Funciones auxiliares (encriptación de contraseñas, manejo de usuarios, generación de tokens).
- `templates/`: Directorio con los templates HTML.
- `images/`: Directorio donde se almacenan las imágenes subidas.
- `imagenes.json`: Archivo JSON que almacena la información de las imágenes subidas.
- `usuarios.json`: Archivo JSON que almacena los usuarios registrados.

## Notas

- El sistema de autenticación se basa en **JWT** para la protección de los endpoints.
- Las imágenes subidas se redimensionan a 800x600 píxeles antes de ser almacenadas.
- Las contraseñas se encriptan utilizando **SHA-256** antes de ser almacenadas.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.


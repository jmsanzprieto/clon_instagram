# main.py
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from functions import * # Importamos todas las funciones de functions.py
from io import BytesIO
from PIL import Image
import uuid
import json

app = FastAPI()

# Montar directorio estático
app.mount("/static", StaticFiles(directory="templates"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")


# Configuración de templates
templates = Jinja2Templates(directory="templates")

# Ruta para la carga de imágenes
UPLOAD_DIR = "images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Configuración para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Modelo para los datos del usuario
class User(BaseModel):
    username: str
    password: str

# Modelo de usuario para recibir el login
class UserLogin(BaseModel):
    username: str
    password: str


# Ruta para la página principal (index)
@app.get("/", response_class=HTMLResponse)
async def get_register_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Ruta para registrar un usuario
@app.post("/register")
async def register_user(user: User):
    # Cargar usuarios existentes
    users = load_users()

    # Comprobar si el usuario ya existe
    existing_user = next((existing_user for existing_user in users if existing_user["username"] == hash_username(user.username)), None)

    if existing_user:
        raise HTTPException(status_code=400, detail=f"El usuario con el nombre de usuario '{user.username}' ya existe")

    # Generar un ID único (UUID)
    user_id = str(uuid.uuid4())  # Genera un UUID único como cadena

    # Encriptar la contraseña
    hashed_password = hash_password(user.password)

    # Encriptar el nombre de usuario
    hashed_username = hash_username(user.username)

    # Guardar el nuevo usuario con su ID
    users.append({"id": user_id, "username": hashed_username, "password": hashed_password})
    save_users(users)

    # Retornar mensaje de éxito con formato JSON
    return {"message": "Usuario registrado correctamente", "id": user_id}



# Ruta para el login
@app.post("/login")
async def login(user: UserLogin):
    # Cargar los usuarios existentes
    users = load_users()

    # Hashear el username y password ingresados
    hashed_username = hash_username(user.username)
    hashed_password = hash_password(user.password)

    # Buscar el usuario por el hash del username
    user_data = next((u for u in users if u["username"] == hashed_username), None)

    # Verificar si el usuario existe y si el hash del password coincide
    if user_data is None or user_data["password"] != hashed_password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Crear el token JWT
    access_token = create_access_token(data={"id": user_data["id"]})

    # Retornar el token
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para cargar la imagen
@app.post("/upload-image")
async def upload_image(
    title: str = Form(...),
    image: UploadFile = File(...),
    authorization: str = Depends(get_current_user)  # Ahora se obtiene el token correctamente
):
    # Obtener el id del usuario desde el token (authorization ya es un diccionario con el payload decodificado)
    user_id = authorization['id']

    # Generar un nombre único para la imagen
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Leer la imagen cargada
    image_data = await image.read()

    # Redimensionar la imagen
    with Image.open(BytesIO(image_data)) as img:
        img = img.resize((800, 600))  # Redimensionamos a 800x600 px
        img.save(filepath)

    # Crear el objeto JSON con la información de la imagen
    image_info = {
        "image_path": filepath,
        "image_name": filename,
        "user_id": user_id,
        "title": title  # Incluimos el título en la información de la imagen
    }

    # Guardar el JSON con la información de las imágenes
    images_json_path = 'imagenes.json'
    if os.path.exists(images_json_path):
        with open(images_json_path, 'r') as f:
            images = json.load(f)
    else:
        images = []

    images.append(image_info)

    with open(images_json_path, 'w') as f:
        json.dump(images, f, indent=4)

    return JSONResponse(content={"message": "Imagen subida exitosamente", "data": image_info})

# Ruta para ver las imagenes
@app.get("/ver_imagenes", response_class=JSONResponse)
async def get_images():
    images_json_path = 'imagenes.json'

    # Comprobar si el archivo de imágenes existe
    if os.path.exists(images_json_path):
        with open(images_json_path, 'r') as f:
            images = json.load(f)
    else:
        images = []

    # Retornar las imágenes como respuesta JSON
    return {"images": images}
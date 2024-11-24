from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header
import json
from typing import List
import hashlib
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import JWTError, jwt

# Cargar variables desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
USERS_FILE = os.getenv("USERS_FILE")
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Cargar usuarios desde el archivo JSON
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Guardar usuarios en el archivo JSON
def save_users(users: List[dict]):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)


# Función para guardar usuarios en un archivo JSON
def save_users(users):
    with open("usuarios.json", "w") as f:
        json.dump(users, f, indent=4)  # El parámetro indent=4 asegura la sangría de 4 espacios

# Función para encriptar la contraseña
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Función para encriptar el nombre de usuario
def hash_username(username: str) -> str:
    return hashlib.sha256(username.encode()).hexdigest()

# Función para guardar usuarios en un archivo JSON
def save_users(users):
    with open("usuarios.json", "w") as f:
        json.dump(users, f, indent=4)  # El parámetro indent=4 asegura la sangría de 4 espacios

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # Crear el JWT codificado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para cargar usuarios desde un archivo JSON (con manejo de errores)
def load_users():
    try:
        with open("usuarios.json", "r") as f:
            # Si el archivo está vacío, devolver una lista vacía
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []  # Si el archivo no existe, devolver una lista vacía
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al procesar el archivo de usuarios")


# Función para guardar los usuarios en el archivo JSON
def save_users(users):
    with open("usuarios.json", "w") as f:
        json.dump(users, f, indent=4) 


# Función para obtener el usuario actual desde el token
def get_current_user(authorization: str = Header(...)):
    # Extraer el token del encabezado Authorization
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
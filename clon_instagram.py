from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
BASE_URL = os.getenv("URL_BASE", "/")

# Crear la app
app = FastAPI()

# Montar directorio estático
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Configuración de templates
templates = Jinja2Templates(directory="templates")

# Ruta de índice
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "base_url": BASE_URL})

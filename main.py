import re
from fastapi import FastAPI, Request, Form, Response, status
from pydantic import BaseModel
from terminusdb_client import WOQLClient
from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi.templating import Jinja2Templates
import datetime
import pymongo
from isodate import parse_datetime

app = FastAPI()
config = dotenv_values(".env")
client = MongoClient(config["ATLAS_URI"])
db = client["mongodb"]
collection_coches = db["coches"]
collection_concesionarios = db["concesionarios"]
templates = Jinja2Templates(directory="templates/")


# Class


class Coche(BaseModel):
    marca: str
    coste: float
    fecha_ingreso: datetime.datetime
    vendido: bool
    matricula: str
    precio: float


class Concesionario(BaseModel):
    Direccion: str


# Cuando la base de datos se inicia crear las colecciones
# Insertar varios coches prueba


@app.on_event("startup")
async def startup():
    date = datetime.datetime(2022, 2, 3)
    coche1 = Coche(marca='ford', coste=12000, fecha_ingreso=date, vendido=False, matricula='6895LPS', precio=17000)
    # collection_coches.insert_one(dict(coche1))


# Lista de los coches GENERAL


@app.get('/api/cars')
async def get_cars(request: Request):
    coches = list(collection_coches.find())
    return templates.TemplateResponse('cars.html', context={"request": request, "coches": coches})


# Lista de los coches BUSCAR POR FECHA DE INGRESO


@app.get('/api/cars/{fecha_ingreso}')
async def get_cars_by_fecha_ingreso(request: Request, fecha_ingreso):
    digits = re.findall(r'\d+', str(fecha_ingreso))
    y = int(digits[0])
    m = int(digits[1])
    d = int(digits[2])
    coches_fecha_ingreso = list(collection_coches.find({'fecha_ingreso': datetime.datetime(y, m, d)}))

    return templates.TemplateResponse('cars_date.html', context={"request": request, "coches": coches_fecha_ingreso})


# Ver todos los detalles de im coche incluyendo su concesionario


@app.get('/api/coches_concesionario')
async def get_coches_concesionario(request: Request):
    return {"coches": "concesionario"}


# Actualizar precio de venta final -> Pasa a vendido Coche vendido no puede ser modificado



@app.post('/api/update/{matricula}/{n_precio}')
async def actualizar_precio_de_venta_final(response: Response,
                                           matricula: str,
                                           n_precio: float
                                           ):
    if not comprobar_matricula(matricula) or n_precio > 1:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return response.status_code

    coche = collection_coches.find_one({'matricula': matricula})
    if not coche.get('vendido'):
        filtro = {'matricula': matricula}
        update = {"$set": {"precio": n_precio, "vendido": True}}
        collection_coches.update_one(filtro, update)
        response.status_code = status.HTTP_201_CREATED
        return response.status_code
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code


# Dar de baja a un coche NO vendido


@app.delete('/api/delete/{matricula}')
async def dar_de_baja_a_un_coche(response: Response,
                                 matricula: str
                                 ):
    if not comprobar_matricula(matricula) :
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return response.status_code

    coche = collection_coches.find_one({'matricula': matricula})
    if coche is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response.status_code
    if not coche.get('vendido'):
        filtro = {'matricula': matricula}
        collection_coches.delete_one(filtro)
        response.status_code = status.HTTP_200_OK
        return response.status_code
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return response.status_code


# FUNCIONES
def comprobar_matricula(matricula: str):
    numeros = sum(c.isdigit() for c in matricula)
    letras = sum(c.isalpha() for c in matricula)
    return matricula.__len__() == 7 and numeros == 4 and letras == 3

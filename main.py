from fastapi import FastAPI
from pydantic import BaseModel
from terminusdb_client import WOQLClient
from pymongo import MongoClient
from dotenv import dotenv_values
import datetime
import pymongo
from peewee import *

app = FastAPI()
config = dotenv_values(".env")
client = MongoClient(config["ATLAS_URI"])
db = client["mongodb"]
collection_coches = db["coches"]




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
    date = datetime.datetime(2022,2,3)
    coche1 = Coche(marca='ford', coste=12000, fecha_ingreso=date,vendido=False, matricula='6895LPS', precio=17000)
    collection_coches.insert_one(dict(coche1))


# Lista de los coches GENERAL


@app.get('/api/cars')
async def get_cars():
    return collection_coches.find_one({'marca':"ford"})


# Lista de los coches BUSCAR POR FECHA DE INGRESO


@app.get('/api/cars/{fecha_ingreso}')
async def get_cars_by_fecha_ingreso(fecha_ingreso):
    return {"cars": "Lista de los cochesPOR FECHA DE INGRESO"}


# Actualizar precio de venta final -> Pasa a vendido Coche vendido no puede ser modificado

# para actualizar


@app.put('/api/update')
async def actualizar_precio_de_venta_final():
    return {"precio_de_venta_final": "Actualizacion de precio de venta final"}


# Dar de baja a un coche NO vendido


@app.delete('/api/delete')
async def dar_de_baja_a_un_coche():
    return {"dar_de_baja_a_un_coche": "Dar de baja a un coche"}

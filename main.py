from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()


# Class


class Coche(BaseModel):
    marca: str
    coste: float
    fecha_ingreso: datetime
    vendido: bool
    matricula: str
    precio: float


class Concesionario(BaseModel):
    Direccion: str


# Lista de los coches GENERAL


@app.get('/api/cars')
async def get_cars():
    return {"cars": "Lista de los coches GENERAL "}


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

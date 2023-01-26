from bson import ObjectId
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi import Response, status, HTTPException
from isodate import parse_datetime
from datetime import datetime
from pydantic import BaseModel
import datetime

app = FastAPI()
config = dotenv_values(".env")
client = MongoClient(config["ATLAS_URI"])
db = client["mongodb"]
collection_coches = db["coches"]
collection_concesionarios = db["concesionarios"]


class Coche(BaseModel):
    marca: str
    coste: float
    fecha_ingreso: datetime.datetime
    vendido: bool
    matricula: str
    precio: float
    concesionario_id: str


class Concesionario(BaseModel):
    nombre: str
    direccion: str


@app.on_event("startup")
async def startup():
    date = datetime.datetime(2022, 2, 3)
    concesionario = Concesionario(nombre='Concesionario Teslas', direccion='calle falsa teslas')
    concesionario_id = collection_concesionarios.insert_one(dict(concesionario)).inserted_id
    coche1 = Coche(marca='Tesla', coste=22000, fecha_ingreso=datetime.datetime.now(), vendido=False,
                   matricula='1234BCD',
                   precio=37000, concesionario_id=str(concesionario_id))
    # collection_concesionarios.insert_one(dict(concesionario))
    # collection_coches.insert_one(dict(coche1))


@app.get('/api/cars')
async def get_cars():
    coches = list(collection_coches.find())
    return [crear_coche(c) for c in coches]


@app.get('/api/cars/{fecha_ingreso}')
async def get_cars_by_fecha_ingreso(fecha_ingreso):
    fecha = parse_datetime(fecha_ingreso)
    coches_fecha_ingreso = list(collection_coches.find({'fecha_ingreso': fecha}))

    return [crear_coche(c) for c in coches_fecha_ingreso]


@app.get('/api/coches_concesionario/{matricula}')
async def get_coches_concesionario_enpoint(matricula: str):
    return await get_coches_concesionario(matricula)


@app.post('/api/update/{matricula}/{n_precio}')
async def actualizar_precio_de_venta_final_endpoint(matricula: str, n_precio: float):
    return await actualizar_precio_venta_final(matricula, n_precio)


@app.delete('/api/delete/{matricula}')
async def dar_de_baja_a_un_coche_endpoint(matricula: str):
    return await dar_de_baja_a_un_coche(matricula)


async def dar_de_baja_a_un_coche(matricula: str):
    if not comprobar_matricula(matricula):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Matricula incorrecta")

    coche = collection_coches.find_one({'matricula': matricula})

    if coche is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Coche no encontrado")

    if not coche.get('vendido'):
        filtro = {'matricula': matricula}
        collection_coches.delete_one(filtro)
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Coche dado de baja correctamente")
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Coche vendido, no se puede dar de baja")


async def get_coches_concesionario(matricula: str):
    if not comprobar_matricula(matricula):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Matricula incorrecta")

    filtro_coche = {'matricula': matricula}
    coche = collection_coches.find_one(filtro_coche)
    filtro_concesionario = {'_id': ObjectId(coche['concesionario_id'])}
    concesionario = collection_concesionarios.find_one(filtro_concesionario)

    return crear_concesionario(concesionario), crear_coche(coche)


async def actualizar_precio_venta_final(matricula: str, n_precio: int):
    if not comprobar_matricula(matricula) or n_precio < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Precio o matricula incorrectas")

    coche = collection_coches.find_one({'matricula': matricula})

    if not coche.get('vendido'):
        filtro = {'matricula': matricula}
        update = {"$set": {"precio": n_precio, "vendido": True}}
        collection_coches.update_one(filtro, update)
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="Precio de venta final actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Coche vendido, no se puede actualizar el precio")


def crear_coche(coche):
    nuevo_coche = {
        "marca": coche["marca"],
        "coste": coche["coste"],
        "fecha_ingreso": coche["fecha_ingreso"],
        "vendido": coche["vendido"],
        "matricula": coche["matricula"],
        "precio": coche["precio"]
    }
    return nuevo_coche


def crear_concesionario(concesionario):
    nuevo_concesionario = {
        "nombre": concesionario["nombre"],
        "direccion": concesionario["direccion"]
    }
    return nuevo_concesionario


def comprobar_matricula(matricula: str):
    numeros = sum(c.isdigit() for c in matricula)
    letras = sum(c.isalpha() for c in matricula)
    return len(matricula) == 7 and numeros == 4 and letras == 3

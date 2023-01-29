# PruebaTecnicaBackend
Iniciar -> uvicorn main:app --reload

Lunes 23 
- Empezar el proyecto, lectura y primeros pasos
- Creacion de clases 
- Creacion de mapeo solo por encima sin la logica

Martes 24
- Libreria de base de datos usada MongDB (NoSQL)
- Configuración atlas
- Configuracion del fichero .env 
- Obtener lista de coches
- Obtener lista de cohes por fechas 
- Empezando actualizar un coche
- Empezar a eliminar un coche

Miércoles 25 
- Dar de baja un coche (Borrar) -> curl -X DELETE "http://localhost:8000/api/delete/{matriucla}"
- Añadido codigo de estado para borrar coches 
- Actualizar el precio de los coches -> curl -X PUT "http://localhost:8000/api/update/{matricula}/{precio}"
- Códigos de estado para atualizar el precio del coche 
- Comprobar matriculas y precios 
- Comprobar listar coches -> curl  "http://localhost:8000/api/cars"
- Refactorizar el código y hacerlo más legible 

Jueves 26 
- Relación One to Many concesionario 
- Revisar enunciado 

Domingo 29 
- Base de datos conectar a docker POR HACER
- Refactorizar último código (startup e insertar datos) 
Para conectar el docker docker run -d -p 27017:27017 --name mongodb mongo
## Incio del docker 
Para iniciar iniciamos el docker(docker pull mongo:latest para descargar 
la imagen de mongoDB) Para ejecutar el contenedor docker(docker run -d -p 27017:27017 
--name mongodb mongo)

## Inicio de la app 
Una vez iniciado el contenedor usamos el comando uvicorn main:app en la terminal
(añadir el flag --reload por si se quiere recargar el poryecto con alguna modificación)

## Comprobar cosas del proyecto 
- Listar todos los coches -> curl "http://localhost:8000/api/cars"
- Listar los coches por fecha de ingreso -> curl "http://localhost:8000/api/cars/{fecha_de_ingreso}"
Formato correcto para la fecha 2023-01-29T22:59:05.708000
- Ver los detalles completo de un coche concreto, incluyendo el concesionario -> 
  curl  "http://localhost:8000/api/coche_concesionario/{matricula}"
- Actualizar precio de venta final -> curl -X PUT "http://localhost:8000/api/update/{matricula}/{precio}"
- Dar de baja a un coche sin vender -> curl -X DELETE "http://localhost:8000/api/delete/{matriucla}"
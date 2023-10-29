# clasePersonaBakcend
Este repositorio es un complemento para el bootcamp dado en la escuela rio software con el fin de complementar lo dictado en la clase 

# Preparar entorno python
1. Crear el entorno virtual con el comando:
```CMD
    pip -m venv ./venv
```

2. Activar el entorno virtual con el comando:
```CMD
./venv/Scripts/Activate.ps1
```
3. Crear el archivo llamado requirements.txt
 (saltarse el paso si existe el archivo)
4. Ejecutar el siguiente comando para instalar las dependencias:
```CMD
pip install -r requirements.txt
```


# Crear migración de alembic (se debe preparar el entorno virtual con los pasos anteriores)
1. para inicializar el framework de alembic se ejecuta el comando
```CMD
alembic init alembic
```
cuando se crea la carpeta alembic encontraremos varios archivos
  - >  una carpeta llamada versions donde se alojará nuestras versiones
 - >  un archivo de configuración llamado alembic.ini el cual tendrá
las configuraciones de la herramienta

2. Para crear una nueva migración se ejecuta el comando
```PYTHON
alembic revision -m "nombre de la revision"
```
Donde editaremos el upgrade y el downgrade(opcional) para la creación
de las tablas y columnas de la base de datos

3. Ejecutar la migración en la base de datos
    - > se debe apuntar a la base de datos (ya sea local o remoto),
    si es local se puede levantar con docker (revisar apartado docker)
    - > editar la ruta de conexión sqlalchemy.url en el archivo alembic.ini
    en la linea 63 con nuestra ruta de conexión
    Ruta de sqlalchemy.url de ejemplo:
    ```
    postgresql+psycopg2://test:docker@localhost:5432/postgres
    ```
    ```
    <tipo de bd>+driver://<user>:<password>@<servidor>:<puerto>/<base de datos>
    ```
     - >ejecutar el comando
    ```CMD

    alembic upgrade head

    ```
    para ejecutar hasta la ultima migración
    (opcional)
    Para devolverse al estado anterior de la base de datos se ejecuta el comando
    ```CMD

    alembic downgrade -1

    ```
    pero debe estar previamente configurado en el archivo de migración


# Levantar servidor docker
1. Si no se tiene instalado docker se debe instalar docker desktop
2. Abrir docker desktop para inicializar docker
3. Revisar en el apartado contenedores docker existe el contenedor con el nombre de la imagen postgres
    - > si existe se ejecuta el comando:
    ```CMD
        docker start <nombre_del_contendor>
    ```
    - > Si no existe se ejecuta el comando:
    ```CMD
        docker run --name postgres-db -e POSTGRES_PASSWORD=docker -e POSTGRES_DB=postgres -e POSTGRES_USER=test -p 5432:5432 postgres
    ```
    El cual requerirá internet para descargar la imagen

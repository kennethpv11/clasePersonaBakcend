from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator


postgres_url = "postgresql+psycopg2://test:docker@localhost:5432/postgres" #ruta de conexión
engine = create_engine(postgres_url, echo=True)#creación de la conexión a la base de datos
Session = sessionmaker(bind=engine) #creación del generador de la sesión a la base de datos
Base = declarative_base() #base que se utilizará en los modelos sqlalchemy para que
#la clase pueda ser utilizada por el framework

def get_db() -> Generator:#metodo que nos entrega una session
    try:
        db= Session() #instanciación de una sessión de la base de datos (creación de la sessión)
        yield db #entrega de una sessión
    finally:
        db.close() #instrucción que cierra la sessión al final de la ejecución de todas las tareas
        #de la sessión, es importante no dejar la sessión abierta por temas de seguridad
from db import Base
from sqlalchemy import Column,String,Integer
from pydantic import BaseModel
class Persona(Base): #modelo de persona que representa la tabla en la base de datos
    #es necesaria para que la herramienta sqlalchemy pueda conocer las tablas
    __tablename__='persona'
    nombre = Column(String,nullable=False)
    id = Column(Integer,primary_key=True)
    usuario = Column(String,nullable=False)
    password = Column(String,nullable=False)

class Persona_py(BaseModel):
    #modelo de pydantic que sirve para recibir los datos de entrada de la api
    #en este caso lo utilizaremos para crear una persona
    nombre:str
    id:int
    usuario:str
    password:str

class Persona_request(BaseModel):
    #modelo de pydantic que sirve para recibir los datos de entrada de la api
    #en este caso la utilizaremos para buscar una persona por usuario y contraseña
    usuario:str
    password:str
    
#es indispensable tener en cuenta que los modelos de pydantic no son los mismos de sqlalchemy
#y que pueden variar con base a la necesidad a utilizar en todo el proyecto
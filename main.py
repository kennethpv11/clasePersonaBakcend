from db import get_db
from model import Persona,Persona_py,Persona_request
from sqlalchemy.orm import Session
from typing import Union
from fastapi import FastAPI,Response,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#Lista de origenes permitidos
#CORS (intercambio de recursos entre orígenes)
#CORS o "intercambio de recursos entre orígenes"
# se refiere a las situaciones en las que una interfaz 
# que se ejecuta en un navegador tiene código JavaScript que se comunica con un backend,
#  y el backend tiene un "origen" diferente al de la interfaz.
#ORIGEN:
#Un origen es la combinación de:
# - protocolo ( http, https)
# - dominio ( myapp.com, localhost, localhost.tiangolo.com) 
# - puerto ( 80, 443, 8080).
origins = [ #Lista de origenes permitidos
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://127.0.0.1:5500",
    ]
#Los middleware son pasos intermediarios entre el cliente y el servidor
#en este caso el navegador hace un paso intermediario llamado una petición options
#la cual le da permiso y las credenciales para poder usar los metodos
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,#lista de origenes permitidos
        allow_credentials=True,#permisos que concede
        allow_methods=["*"],#Methodos a los cuales tiene acceso
        allow_headers=["*"],#Headers permitidos
)

@app.post("/")
def create_persona(persona:Persona_py):
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        session = get_db()
        db:Session
        for db in session:
            persona = Persona(**persona.model_dump())
            #añade el recurso persona para subirse a la base de datos
            db.add(persona)
            #se sube a la base de datos
            db.commit()
            #se refresca la información en la variable persona para poderla devolver
            #en el servicio
            db.refresh(persona)
            return persona
    #¡fin try!
    except Exception as e: #instrucción que nos ayuda a atrapar la excepción que ocurre cuando alguna instrucción dentro de try falla
        #se debe controlar siempre que nos conectamos a una base de datos con un try - except
        #debido a que no podemos controlar la respuesta del servicio externo (en este caso la base de datos)
        #y es muy posible que la conexión falle por lo cual debemos responder que paso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        #la instrucción raise es similar a la instrucción return, pero en vez de retornar cualquier elemento, retornamos especificamente
        #un error, en este caso el error esta contenido en HTTPException
    

@app.get("/{item_id}",response_model=Persona_py)
def read_persona(item_id: int):
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        session = get_db()
        db:Session
        for db in session:
            #se usa la instrucción where para buscar por el id y se ejecuta el first para
            #encontrar la primera coincidencia, esto es posible porque el id es un 
            #identificador unico
            r=db.query(Persona).where(Persona.id == item_id).first()
            return r
    #¡fin try!
    except Exception as e:#instrucción que nos ayuda a atrapar la excepción que ocurre cuando alguna instrucción dentro de try falla
        #se debe controlar siempre que nos conectamos a una base de datos con un try - except
        #debido a que no podemos controlar la respuesta del servicio externo (en este caso la base de datos)
        #y es muy posible que la conexión falle por lo cual debemos responder que paso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        #la instrucción raise es similar a la instrucción return, pero en vez de retornar cualquier elemento, retornamos especificamente
        #un error, en este caso el error esta contenido en HTTPException
    
@app.post("/validate-credentials/")#la ruta de tipo post se utiliza ya que debemos recibir un usuario y contraseña y esta información es sencible,
#por lo cual se utiliza el cuerpo body para recibir la información y que no sea expuesta (es decir se hace por seguridad de la información)
def read_usuario_password(item: Persona_request):
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        #si falla, se detendrá el flujo común y se ejecutará las instrucciones del except
        session = get_db()
        db:Session
        for db in session:
            #se usa la palabra filter para filtrar por varios valores al mismo tiempo donde filtramos la primera vez
            #por usuario y la segunda vez por contraseña, posteriormente utilizamos el metodo all debido a que no podemos
            #garantizar que solo exista una persona
            r=db.query(Persona).filter(Persona.usuario == item.usuario).filter(Persona.password == item.password).all()

            if len(r) ==0:#se debe validar si es cero la cantidad de personas que nos responde para retornar un error ya que no encontro la persona esperada
                return Response(status_code=status.HTTP_404_NOT_FOUND)
            elif len(r) > 1:#se debe validar que es mayor a uno porque si varias personas tienen el mismo usuario y contraseña
                #logicamente puede generar conflictos al crear una session
                return Response(status_code=status.HTTP_409_CONFLICT)
            else:
                return r
    #¡fin try!
    except Exception as e: #instrucción que nos ayuda a atrapar la excepción que ocurre cuando alguna instrucción dentro de try falla
        #se debe controlar siempre que nos conectamos a una base de datos con un try - except
        #debido a que no podemos controlar la respuesta del servicio externo (en este caso la base de datos)
        #y es muy posible que la conexión falle por lo cual debemos responder que paso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        #la instrucción raise es similar a la instrucción return, pero en vez de retornar cualquier elemento, retornamos especificamente
        #un error, en este caso el error esta contenido en HTTPException


@app.delete("/{item_id}")
def delete_persona(item_id: int):
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        #si falla, se detendrá el flujo común y se ejecutará las instrucciones del except
        session = get_db()
        db:Session
        for db in session:
            #one or none es una instrucción que nos permite encontrar uno o ningún recurso
            #en caso que sea un recurso lo añadiremos al delete ya que es el que vamos a borrar
            #en caso que sea None se lanza un error, ya que no tenemos un dato con el id a borrar
            #si intentamos borrar algo que no existe (en el caso que sea None) nos lanzará una 
            #excepción y será atrapada en el except
            r=db.query(Persona).where(Persona.id == item_id).one_or_none()
            if r is not None:
                db.delete(r)#instruccion para borrar un recurso
                db.commit()
                return Response(status_code=status.HTTP_200_OK)
            else:
                return Response(status_code=status.HTTP_404_NOT_FOUND)
    #¡fin try!
    except Exception as e: #instrucción que nos ayuda a atrapar la excepción que ocurre cuando alguna instrucción dentro de try falla
        #se debe controlar siempre que nos conectamos a una base de datos con un try - except
        #debido a que no podemos controlar la respuesta del servicio externo (en este caso la base de datos)
        #y es muy posible que la conexión falle por lo cual debemos responder que paso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        #la instrucción raise es similar a la instrucción return, pero en vez de retornar cualquier elemento, retornamos especificamente
        #un error, en este caso el error esta contenido en HTTPException            }

            
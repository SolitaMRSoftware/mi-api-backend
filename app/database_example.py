from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://tu_username:tu_password@host/database_name'
#tu_usuario, tu_contraseña, localhost y nombre_base deben ser reemplazados con los reales

#creo el motor q hace que sql alchemy se conecte con la BD postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#necesito de una sesion para hablar con la BD
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

#aca pego la dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
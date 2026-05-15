from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Clase para manejar la conexión a la base de datos
class Database:
    def __init__(self, database_url):
        #print (database_url)
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self):
        return self.SessionLocal()

# Aquí definimos cómo conectarnos a nuestra base de datos MySQL. 
DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost:3307/EcDeposito"

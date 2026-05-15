from app.worker.consumer import start
from app.core.database import engine, Base

# Code First también aquí
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    start()
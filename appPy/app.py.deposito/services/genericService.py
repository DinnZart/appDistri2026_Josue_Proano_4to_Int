from typing import Generic, TypeVar
from dataAccess.conexion import Database

T = TypeVar('T')

class GenericService(Generic[T]):
    
    def __init__(self, model: T,  database: Database):
        self.model = model
        self.db = database

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        session = self.db.get_session()
        session.add(instance)
        session.commit()
        session.refresh(instance)
        session.close()
        return instance
    

    def getAll(self):
        session = self.db.get_session()
        instance = session.query(self.model).all();
        session.close()
        return instance
    

    def get(self, id):
        session = self.db.get_session()
        instance = session.query(self.model).get(id)
        session.close()
        return instance


    def update(self, id, obj_data) -> T:
        session = self.db.get_session()
        obj = session.query(self.model).get(id)
        for var, value in vars(obj_data).items():
            setattr(obj, var, value)
        print('obj listo para update')
        print(vars(obj))
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def delete(self, id):
        instance = self.get(id)
        session = self.db.get_session()
        session.delete(instance)
        session.commit()
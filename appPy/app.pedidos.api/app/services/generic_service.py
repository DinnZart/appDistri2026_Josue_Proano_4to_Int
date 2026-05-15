from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")


class GenericService(Generic[T]):

    def __init__(self, model: Type[T], database):
        self.model = model
        self.db = database

    def create(self, data: dict) -> T:
        session: Session = self.db.get_session()
        try:
            instance = self.model(**data)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get_all(self) -> List[T]:
        session: Session = self.db.get_session()
        try:
            return session.query(self.model).all()
        finally:
            session.close()

    def get_by_id(self, id: int) -> Optional[T]:
        session: Session = self.db.get_session()
        try:
            return session.get(self.model, id)
        finally:
            session.close()

    def update(self, id: int, data: dict) -> Optional[T]:
        session: Session = self.db.get_session()
        try:
            instance = session.get(self.model, id)

            if not instance:
                return None

            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, id: int) -> bool:
        session: Session = self.db.get_session()
        try:
            instance = session.get(self.model, id)
            if not instance:
                return False

            session.delete(instance)
            session.commit()
            return True
        finally:
            session.close()
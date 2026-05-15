
from dataAccess.conexion import DATABASE_URL, Database
from dataAccess.entities.depositos import Base, Deposito
from models.depositoDto import DepositoDto
from services.genericService import GenericService
from datetime import datetime

class DepositoService:

    def __init__(self):
        self.db = Database(DATABASE_URL)
        self.engine =  self.db.engine
        # Crea todas las tablas definidas en el modelo
        #db.Base.metadata.create_all(bind=engine)
        Base.metadata.create_all(bind= self.engine)
        self.depService = GenericService[Deposito](Deposito,  self.db)


    def Depositar(self, depDto: DepositoDto):
        # Obtener la fecha actual
        fecha_actual = datetime.now()
        # Formatear la fecha en formato dd/mm/YYYY
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
        return self.depService.create(nombre=depDto.nombre, cuenta=depDto.cuenta, tipo=depDto.tipo, cantidad=depDto.valor, fecha=fecha_formateada)


    def Consultar(self):
        listaDeposito = self.depService.getAll()
        return listaDeposito
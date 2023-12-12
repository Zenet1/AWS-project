from utils.db import ConexionDB

class Profesor(ConexionDB.Model):

    IDProfesor = ConexionDB.Column(ConexionDB.Integer, primary_key = True)
    nombres = ConexionDB.Column(ConexionDB.String(50))
    apellidos = ConexionDB.Column(ConexionDB.String(50)) 
    numeroEmpleado = ConexionDB.Column(ConexionDB.Integer())
    horasClase = ConexionDB.Column(ConexionDB.Integer())

    def __init__(self, nombres, apellidos, numeroEmpleado, horasClase):
        self.nombres = nombres
        self.apellidos = apellidos
        self.numeroEmpleado = numeroEmpleado
        self.horasClase = horasClase
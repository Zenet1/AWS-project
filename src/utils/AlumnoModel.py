from utils.db import ConexionDB

class Alumno(ConexionDB.Model):

    IDAlumno = ConexionDB.Column(ConexionDB.Integer, primary_key = True)
    nombre_alumno = ConexionDB.Column(ConexionDB.String(50))
    apellidos_alumno = ConexionDB.Column(ConexionDB.String(50)) 
    matricula = ConexionDB.Column(ConexionDB.String(10))
    promedio = ConexionDB.Column(ConexionDB.Float(10))

    def __init__(self, nombre_alumno, apellidos_alumno, matricula, promedio):
        self.nombre_alumno = nombre_alumno
        self.apellidos_alumno = apellidos_alumno
        self.matricula = matricula
        self.promedio = promedio
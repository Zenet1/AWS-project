from utils.db import ConexionDB

class Alumno(ConexionDB.Model):

    IDAlumno = ConexionDB.Column(ConexionDB.Integer, primary_key = True)
    nombres = ConexionDB.Column(ConexionDB.String(50))
    apellidos = ConexionDB.Column(ConexionDB.String(50)) 
    matricula = ConexionDB.Column(ConexionDB.String(50))
    promedio = ConexionDB.Column(ConexionDB.Float())
    password = ConexionDB.Column(ConexionDB.String(50))
    fotoPerfilUrl = ConexionDB.Column(ConexionDB.String(100))

    def __init__(self, nombres, apellidos, matricula, promedio, password, fotoPerfilUrl = None):
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
        self.password = password
        self.fotoPerfilUrl = fotoPerfilUrl
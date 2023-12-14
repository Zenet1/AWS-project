from app import MarshmallowHandler

class AlumnoSchema(MarshmallowHandler.Schema):
    class Meta:
        fields = ('IDAlumno', 'nombres', 'apellidos', 'matricula', 'promedio', 'password', 'fotoPerfilUrl')
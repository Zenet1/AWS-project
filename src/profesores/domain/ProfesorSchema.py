from app import MarshmallowHandler

class ProfesorSchema(MarshmallowHandler.Schema):
    class Meta:
        fields = ('IDProfesor', 'numeroEmpleado', 'nombres', 'apellidos', 'horasClase')

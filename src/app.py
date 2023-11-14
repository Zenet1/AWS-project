from flask import Flask
from alumnos.AlumnoRoute import alumnos
from profesores.ProfesorRoute import profesores

app = Flask(__name__)

app.register_blueprint(alumnos)
app.register_blueprint(profesores)
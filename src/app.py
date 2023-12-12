from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.config import database_connection_uri
from utils.db import ConexionDB
from alumnos.infraestructure.AlumnoRoute import alumnos
from profesores.infraestructure.ProfesorRoute import profesores

app = Flask(__name__)

app.register_blueprint(alumnos)
app.register_blueprint(profesores)

#Conexión MySQL por SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = database_connection_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ConexionDB.init_app(app)

#SQLAlchemy(app)
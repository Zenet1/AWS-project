from alumnos.domain.AlumnoService import getAllAlumnos, getAlumnoByID, insertAlumno, updateAlumno, deleteAlumno
from flask import Blueprint, jsonify, render_template, request, redirect, url_for

alumnos = Blueprint('alumnos', __name__)

# Ruta 'GET /alumnos': Recupera todos los registros de los alumnos

@alumnos.route('/alumnos', methods = ['GET'])
def obtener_alumnos():
    response = getAllAlumnos()
    
    return jsonify(response.get("alumnos")), response.get("statusCode")


# Ruta 'GET /alumnos/<id>': Recupera el registro del alumno con el ID correspondiente

@alumnos.route('/alumnos/<id>', methods = ['GET'])
def obtener_alumno_individual(id):
    
    response = getAlumnoByID(id)
    
    if response.get('founded') == 0:
        responseBody = 'Not founded'
    else:
        responseBody = response.get('alumno')
        
    return jsonify(responseBody), response.get("statusCode")

# Ruta 'POST /alumnos/<id>': Ingresa un nuevo registro 'Alumno'

@alumnos.route('/alumnos', methods = ['POST'])
def registrar_alumno():
    response = insertAlumno(request.json)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'PUT /alumnos/<id>': Actualiza el registro del alumno con el ID correspondiente

@alumnos.route('/alumnos/<id>', methods = ['PUT'])
def actualizar_alumno(id):
    response = updateAlumno(id, request.json)

    return jsonify(response.get('responseBody')), response.get('statusCode')
    
# Ruta 'DELETE /alumnos/<id>': Elimina el registro del alumno con el ID correspondiente

@alumnos.route('/alumnos/<id>', methods = ['DELETE'])
def eliminar_alumno(id):
    response = deleteAlumno(id)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')
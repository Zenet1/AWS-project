from alumnos.domain.AlumnoService import getAllAlumnos, getAlumnoByID, insertAlumno, updateAlumno, deleteAlumno, uploadAlumnoPhoto, sendAlert, loginAlumno, verifySessionAlumno, logoutAlumno
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
import json

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

# Ruta 'POST /alumnos/<id>/fotoPerfil': Acepta una imagen para su inclusión en un bucket público en Amazon S3, actualiza el registro para contener la url
# Aceptar 'multipart/form-data'

@alumnos.route('/alumnos/<id>/fotoPerfil', methods = ['POST'])
def subir_foto(id):
    response = uploadAlumnoPhoto(id, request)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'POST /alumnos/<id>/email': Envía una alerta de SNS a un correo 'suscriptor'

@alumnos.route('/alumnos/<id>/email', methods = ['POST'])
def enviar_alerta(id):
    response = sendAlert(id)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'POST /alumnos/<id>/session/login': Registra una entrada en una tabla en DynamoDB con la información de la sesión del alumno

@alumnos.route('/alumnos/<id>/session/login', methods = ['POST'])
def iniciar_sesion(id):
    response = loginAlumno(id, request.json)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'POST /alumnos/<id>/session/verify': Valida si la sesión es válida y si está activa

@alumnos.route('/alumnos/<id>/session/verify', methods = ['POST'])
def validar_sesion(id):
    response = verifySessionAlumno(id, request.json)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'POST /alumnos/<id>/session/logout': Desactiva la sesión
@alumnos.route('/alumnos/<id>/session/logout', methods = ['POST'])
def cerrar_sesion(id):
    response = logoutAlumno(id, request.json)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')
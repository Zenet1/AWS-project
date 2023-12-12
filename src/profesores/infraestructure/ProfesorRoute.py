from profesores.domain.ProfesorService import getAllProfesores, getProfesorByID, insertProfesor, updateProfesor, deleteProfesor
from flask import Blueprint, jsonify, render_template, request, redirect, url_for

profesores = Blueprint('profesores', __name__)

# Ruta 'GET /profesores': Recupera todos los registros de los profesores

@profesores.route('/profesores', methods = ['GET'])
def obtener_profesores():
    response = getAllProfesores()
    
    return jsonify(response.get("profesores")), response.get("statusCode")


# Ruta 'GET /profesores/<id>': Recupera el registro del profesor con el ID correspondiente

@profesores.route('/profesores/<id>', methods = ['GET'])
def obtener_profesor_individual(id):
    
    response = getProfesorByID(id)
    
    if response.get('founded') == 0:
        responseBody = 'Not founded'
    else:
        responseBody = response.get('profesor')
        
    return jsonify(responseBody), response.get("statusCode")

# Ruta 'POST /profesores/<id>': Ingresa un nuevo registro 'Profesor'

@profesores.route('/profesores', methods = ['POST'])
def registrar_profesor():
    response = insertProfesor(request.json)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')

# Ruta 'PUT /profesores/<id>': Actualiza el registro del profesor con el ID correspondiente

@profesores.route('/profesores/<id>', methods = ['PUT'])
def actualizar_profesor(id):
    response = updateProfesor(id, request.json)

    return jsonify(response.get('responseBody')), response.get('statusCode')
    
# Ruta 'DELETE /profesores/<id>': Elimina el registro del alumno con el ID correspondiente

@profesores.route('/profesores/<id>', methods = ['DELETE'])
def eliminar_alumno(id):
    response = deleteProfesor(id)
    
    return jsonify(response.get('responseBody')), response.get('statusCode')
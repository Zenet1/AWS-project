from app import app
from ProfesorService import getAllProfesores, getProfesorByID, insertProfesor, updateProfesor, deleteProfesor
from flask import Blueprint, render_template, request, redirect, url_for
import ProfesorDTO

'''
Ruta 'GET /profesores': Recupera todos los registros de los profesores
'''
@app.route('/profesores', methods = ['GET'])
def obtener_profesores():
    response = getAllProfesores()
    '''
    agencias = Agencia.query.all()
    data = {
        'agencias' : agencias,
        'numero_agencias' : len(agencias)
    }
    return data
    '''
    return response, 200

'''
Ruta 'GET /profesores/<id>': Recupera el registro del profesor con el ID correspondiente
'''
@app.route('/profesores/<id>', methods = ['GET'])
def obtener_profesor_individual(id):
    response = getProfesorByID(id)
    '''
    data = recuperar_agencias()
    return render_template('agencia/agencias.html', data = data)
    '''
    return response, 200

'''
Ruta 'POST /profesores/<id>': Ingresa un nuevo registro 'Profesor'
'''
@app.route('/profesores', methods = ['POST'])
def registrar_profesor(profesorData):
    insertProfesor(profesorData)
    '''
    return render_template("agencia/crear-agencia.html")
    '''
    return "Ok", 200

'''
Ruta 'PUT /profesores/<id>': Actualiza el registro del profesor con el ID correspondiente
'''
@app.route('/profesores/<id>', methods = ['PUT'])
def actualizar_profesor(id, profesorDataActualizada):
    updateProfesor(id, profesorDataActualizada)
    '''
    nombre_agencia = request.form['nombre_agencia']
    direccion_linea1 = request.form['direccion_linea1']
    direccion_linea2 = request.form['direccion_linea2']
    ciudad = request.form['ciudad']
    estado = request.form['estado']
    
    nueva_agencia = Agencia(nombre_agencia, direccion_linea1, direccion_linea2, ciudad, estado)

    ConexionDB.session.add(nueva_agencia)
    ConexionDB.session.commit()

    return redirect(url_for('agencias.listar_agencias'))
    '''
    return "Ok", 200
    
'''
Ruta 'DELETE /profesores/<id>': Elimina el registro del profesor con el ID correspondiente
'''
@app.route('/profesores/<id>', methods = ['DELETE'])
def eliminar_profesor(id):
    deleteProfesor(id)
    '''
    agencia = Agencia.query.get(id)
    ConexionDB.session.delete(agencia)
    ConexionDB.session.commit()
    return redirect(url_for('agencias.listar_agencias'))
    '''
    return "Ok", 200
from app import app
from AlumnoService import getAllAlumnos, getAlumnoByID, insertAlumno, updateAlumno, deleteAlumno
from flask import Blueprint, render_template, request, redirect, url_for

'''
Ruta 'GET /alumnos': Recupera todos los registros de los alumnos
'''
@app.route('/alumnos', methods = ['GET'])
def obtener_alumnos():
    response = getAllAlumnos()
    
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
Ruta 'GET /alumnos/<id>': Recupera el registro del alumno con el ID correspondiente
'''
@app.route('/alumnos/<id>', methods = ['GET'])
def obtener_alumno_individual(id):
    response = getAlumnoByID(id)
    '''
    data = recuperar_agencias()
    return render_template('agencia/agencias.html', data = data)
    '''
    return response, 200

'''
Ruta 'POST /alumnos/<id>': Ingresa un nuevo registro 'Alumno'
'''
@app.route('/alumnos', methods = ['POST'])
def registrar_alumno(alumnoData):
    insertAlumno(alumnoData)
    '''
    return render_template("agencia/crear-agencia.html")
    '''
    return "Ok", 200

'''
Ruta 'PUT /alumnos/<id>': Actualiza el registro del alumno con el ID correspondiente
'''
@app.route('/alumnos/<id>', methods = ['PUT'])
def actualizar_alumno(id, alumnoDataActualizada):
    updateAlumno(id, alumnoDataActualizada)
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
Ruta 'DELETE /alumnos/<id>': Elimina el registro del alumno con el ID correspondiente
'''
@app.route('/alumnos/<id>', methods = ['DELETE'])
def eliminar_alumno(id):
    deleteAlumno(id)
    '''
    agencia = Agencia.query.get(id)
    ConexionDB.session.delete(agencia)
    ConexionDB.session.commit()
    return redirect(url_for('agencias.listar_agencias'))
    '''
    return "Ok", 200
from utils.validator import verifyData
from utils.db import ConexionDB
from alumnos.domain.AlumnoModel import Alumno
from sqlalchemy.exc import SQLAlchemyError

def getAllAlumnos():
    alumnos = Alumno.query.all()
    alumnos_list = [{'IDAlumno': alumno.IDAlumno,
                     'nombres': alumno.nombres,
                     'apellidos': alumno.apellidos,
                     'matricula': alumno.matricula,
                     'promedio': alumno.promedio,
                     'password': alumno.password} for alumno in alumnos
                    ]

    return {'alumnos': alumnos_list, 'statusCode': 200}

def getAlumnoByID(id):
    foundedStatus = 0
    statusCode = 404
    dataFounded = {
        'error': 'Cannot retrieve'
    }
    
    try:
        alumno_founded = Alumno.query.get(id)
        
        if alumno_founded is not None:
            foundedStatus = 1
            statusCode = 200
            
            dataFounded = {
            'nombres': alumno_founded.nombres,
            'apellidos': alumno_founded.apellidos,
            'matricula': alumno_founded.matricula,
            'promedio': alumno_founded.promedio,
            'password': alumno_founded.password
            }
            
    except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'founded': foundedStatus, 'alumno': dataFounded, 'statusCode': statusCode}

def insertAlumno(alumnoData):
    responseBody = 'Error in the insertion: Invalid input data'
    statusCode = 400
    
    if verifyData(alumnoData, 'alumno'):
        
        try:
            nuevo_alumno = Alumno(alumnoData.get('nombres'), alumnoData.get('apellidos'), alumnoData.get('matricula'), alumnoData.get('promedio'), alumnoData.get('password'))
            ConexionDB.session.add(nuevo_alumno)
            ConexionDB.session.commit()
            
            statusCode = 201
            responseBody = {
            'id': nuevo_alumno.IDAlumno,
            'nombres': nuevo_alumno.nombres,
            'apellidos': nuevo_alumno.apellidos,
            'matricula': nuevo_alumno.matricula,
            'promedio': nuevo_alumno.promedio,
            'password': nuevo_alumno.password
            }
            
        except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
        
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateAlumno(id, alumnoData):
    responseBody = 'Error in the update: Invalid input data'
    statusCode = 400
    
    if verifyData(alumnoData, 'alumno'):
        
        try:
            alumno_toUpdate = Alumno.query.get(id)
            
            if alumno_toUpdate is None:
                responseBody = "ID not found"
                
            else:
                statusCode = 200
                responseBody = "Succesfully updated"
                
                alumno_toUpdate.nombres = alumnoData.get('nombres')
                alumno_toUpdate.apellidos = alumnoData.get('apellidos')
                alumno_toUpdate.matricula = alumnoData.get('matricula')
                alumno_toUpdate.promedio = alumnoData.get('promedio')
                alumno_toUpdate.password = alumnoData.get('password')
                ConexionDB.session.commit()
                
        except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'responseBody': responseBody, 'statusCode': statusCode}

def deleteAlumno(id):
    responseBody = 'ID not found'
    statusCode = 404
    try:
        alumno_toDelete = Alumno.query.get(id)
        
        if alumno_toDelete is not None:
            ConexionDB.session.delete(alumno_toDelete)
            ConexionDB.session.commit()
            responseBody = 'Succesfully deleted'
            statusCode = 200
            
    except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'responseBody': responseBody, 'statusCode': statusCode}
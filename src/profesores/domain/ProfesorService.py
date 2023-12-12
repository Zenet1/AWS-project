from utils.validator import verifyData
from utils.db import ConexionDB
from profesores.domain.ProfesorModel import Profesor
from sqlalchemy.exc import SQLAlchemyError

def getAllProfesores():
    profesores = Profesor.query.all()
    profesores_list = [{'IDProfesor': profesor.IDProfesor,
                     'nombres': profesor.nombres,
                     'apellidos': profesor.apellidos,
                     'numeroEmpleado': profesor.numeroEmpleado,
                     'horasClase': profesor.horasClase} for profesor in profesores
                    ]

    return {'profesores': profesores_list, 'statusCode': 200}

def getProfesorByID(id):
    foundedStatus = 0
    statusCode = 404
    dataFounded = {
        'error': 'Cannot retrieve'
    }
    
    try:
        profesor_founded = Profesor.query.get(id)
        
        if profesor_founded is not None:
            foundedStatus = 1
            statusCode = 200
            
            dataFounded = {
            'nombres': profesor_founded.nombres,
            'apellidos': profesor_founded.apellidos,
            'numeroEmpleado': profesor_founded.numeroEmpleado,
            'horasClase': profesor_founded.horasClase
            }
            
    except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'founded': foundedStatus, 'profesor': dataFounded, 'statusCode': statusCode}

def insertProfesor(profesorData):
    responseBody = 'Error in the insertion: Invalid input data'
    statusCode = 400
    
    if verifyData(profesorData, 'profesor'):
        
        try:
            nuevo_profesor = Profesor(profesorData.get('nombres'), profesorData.get('apellidos'), profesorData.get('numeroEmpleado'), profesorData.get('horasClase'))
            ConexionDB.session.add(nuevo_profesor)
            ConexionDB.session.commit()
            
            statusCode = 201
            responseBody = 'Insertion completed'
            
        except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
        
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateProfesor(id, profesorData):
    responseBody = 'Error in the update: Invalid input data'
    statusCode = 400
    
    if verifyData(profesorData, 'profesor'):
        
        try:
            profesor_toUpdate = Profesor.query.get(id)
            
            if profesor_toUpdate is None:
                responseBody = "ID not found"
                
            else:
                statusCode = 200
                responseBody = "Succesfully updated"
                
                profesor_toUpdate.nombres = profesorData.get('nombre_pronombresfesor')
                profesor_toUpdate.apellidos = profesorData.get('apellidos')
                profesor_toUpdate.numeroEmpleado = profesorData.get('numeroEmpleado')
                profesor_toUpdate.horasClase = profesorData.get('horasClase')
                ConexionDB.session.commit()
                
        except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'responseBody': responseBody, 'statusCode': statusCode}

def deleteProfesor(id):
    responseBody = 'ID not found'
    statusCode = 404
    try:
        profesor_toDelete = Profesor.query.get(id)
        
        if profesor_toDelete is not None:
            ConexionDB.session.delete(profesor_toDelete)
            ConexionDB.session.commit()
            responseBody = 'Succesfully deleted'
            statusCode = 200
            
    except SQLAlchemyError as e:
            statusCode = 500
            responseBody = f'Error during database transaction: {str(e)}'
            ConexionDB.session.rollback()
            
    return {'responseBody': responseBody, 'statusCode': statusCode}

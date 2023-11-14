from utils.db import profesorDB
from utils.validator import verifyData

def getAllProfesores():
    return {'profesores': profesorDB, 'statusCode': 200}
    

def getProfesorByID(id):
    foundedStatus = 0
    statusCode = 404
    profesor_founded = {
    'id': 0,
    'nombres': '',
    'apellidos': '',
    'matricula': '',
    'promedio': 0.1
    }
    
    for profesor in profesorDB:
        if profesor.get('id') == int(id):
            profesor_founded = profesor
            foundedStatus = 1
            statusCode = 200
            
    return {'founded': foundedStatus, 'profesor': profesor_founded, 'statusCode': statusCode}

def insertProfesor(profesorData):
    responseBody = 'Error in the insertion: Invalid input data'
    statusCode = 400
    if verifyData(profesorData, 'profesor'): 
        profesorDB.append(profesorData)
        statusCode = 201
        responseBody = 'Insertion completed'
    
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateProfesor(id, profesorData):
    responseBody = 'Error in the update: Invalid input data'
    statusCode = 400
    
    if verifyData(profesorData, 'profesor'):
        updaterResponse = updateFinder(id, profesorData)
        responseBody = updaterResponse.get('responseBody')
        statusCode = updaterResponse.get('statusCode')
        
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateFinder(id, profesorData):
    responseBody = 'ID not found'
    statusCode = 404
    for profesor in profesorDB:
        if profesor.get('id') == int(id):
            profesor.update({'numeroEmpleado': profesorData.get('numeroEmpleado')})
            profesor.update({'nombres': profesorData.get('nombres')})
            profesor.update({'apellidos': profesorData.get('apellidos')})
            profesor.update({'horasClase': profesorData.get('horasClase')})
            responseBody = 'Updated'
            statusCode = 200
    return {'responseBody': responseBody, 'statusCode': statusCode}

def deleteProfesor(id):
    responseBody = 'ID not found'
    statusCode = 404
    for profesor in profesorDB:
        if profesor.get('id') == int(id):
            profesorDB.remove(profesor)
            responseBody = 'Deleted'
            statusCode = 200
            
    return {'responseBody': responseBody, 'statusCode': statusCode}

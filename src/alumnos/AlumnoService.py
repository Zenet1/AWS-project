from utils.db import alumnoDB
from utils.validator import verifyData

def getAllAlumnos():
    return {'alumnos': alumnoDB, 'statusCode': 200}
    

def getAlumnoByID(id):
    foundedStatus = 0
    statusCode = 404
    alumno_founded = {
    'id': 0,
    'nombres': '',
    'apellidos': '',
    'matricula': '',
    'promedio': 0.1
    }
    
    for alumno in alumnoDB:
        if alumno.get('id') == int(id):
            alumno_founded = alumno
            foundedStatus = 1
            statusCode = 200
            
    return {'founded': foundedStatus, 'alumno': alumno_founded, 'statusCode': statusCode}

def insertAlumno(alumnoData):
    responseBody = 'Error in the insertion: Invalid input data'
    statusCode = 400
    if verifyData(alumnoData, 'alumno'): 
        alumnoDB.append(alumnoData)
        statusCode = 201
        responseBody = 'Insertion completed'
    
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateAlumno(id, alumnoData):
    responseBody = 'Error in the update: Invalid input data'
    statusCode = 400
    
    if verifyData(alumnoData, 'alumno'):
        updaterResponse = updateFinder(id, alumnoData)
        responseBody = updaterResponse.get('responseBody')
        statusCode = updaterResponse.get('statusCode')
        
    return {'responseBody': responseBody, 'statusCode': statusCode}

def updateFinder(id, alumnoData):
    responseBody = 'ID not found'
    statusCode = 404
    for alumno in alumnoDB:
        if alumno.get('id') == int(id):
            alumno.update({'nombres': alumnoData.get('nombres')})
            alumno.update({'apellidos': alumnoData.get('apellidos')})
            alumno.update({'matricula': alumnoData.get('matricula')})
            alumno.update({'promedio': alumnoData.get('promedio')})
            responseBody = 'Updated'
            statusCode = 200
    return {'responseBody': responseBody, 'statusCode': statusCode}

def deleteAlumno(id):
    responseBody = 'ID not found'
    statusCode = 404
    for alumno in alumnoDB:
        if alumno.get('id') == int(id):
            alumnoDB.remove(alumno)
            responseBody = 'Deleted'
            statusCode = 200
            
    return {'responseBody': responseBody, 'statusCode': statusCode}

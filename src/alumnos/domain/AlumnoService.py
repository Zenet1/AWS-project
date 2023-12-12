from flask import jsonify
from utils.validator import verifyData
from utils.db import ConexionDB
from alumnos.domain.AlumnoModel import Alumno
from sqlalchemy.exc import SQLAlchemyError
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename
from utils.awsConfig import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, SESSION_TOKEN
import boto3

def getAllAlumnos():
    alumnos = Alumno.query.all()
    alumnos_list = [{'IDAlumno': alumno.IDAlumno,
                     'nombres': alumno.nombres,
                     'apellidos': alumno.apellidos,
                     'matricula': alumno.matricula,
                     'promedio': alumno.promedio,
                     'password': alumno.password,
                     'fotoPerfilUrl': alumno.fotoPerfilUrl} for alumno in alumnos
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
            'password': alumno_founded.password,
            'fotoPerfilUrl': alumno_founded.fotoPerfilUrl
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
                statusCode = 404
                
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

def uploadAlumnoPhoto(id, alumnoData):
    responseBody = 'Invalid input data'
    statusCode = 400
    
    try:
        alumno_toUpdate = Alumno.query.get(id)
        
        if alumno_toUpdate is None:
            return {'responseBody': 'Error: Alumno no encontrado', 'statusCode': 404}
        
        s3 = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY, aws_session_token = SESSION_TOKEN)
        
        if 'foto' not in alumnoData.files:
            responseBody = 'Error: No file part'
            statusCode = 400
        
        foto = alumnoData.files['foto']
        
        s3_filename = f'alumnos/{id}_fotoPerfil.jpg'
        s3.upload_fileobj(foto, 'eduardozenetawsproject', s3_filename)
        fotoUrl = f'https://eduardozenetawsproject.s3.amazonaws.com/alumnos/{id}_fotoPerfil.jpg'

        responseBody = fotoUrl
        
        alumno_toUpdate.fotoPerfilUrl = fotoUrl
        ConexionDB.session.commit()
        statusCode = 201
        responseBody = "Succesfully uploaded"
        
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = f'Error during database transaction: {str(e)}'
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
    
    return {'responseBody': responseBody, 'statusCode': statusCode}
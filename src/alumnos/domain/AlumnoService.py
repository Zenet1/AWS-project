import json
from flask import jsonify
from utils.validator import verifyData
from utils.db import ConexionDB
from alumnos.domain.AlumnoModel import Alumno
from sqlalchemy.exc import SQLAlchemyError
from botocore.exceptions import NoCredentialsError, ClientError
from utils.awsConfig import BUCKET_NAME, DYNAMODB_NAME, ARN_TOPIC
from datetime import datetime
import time
from utils.randomGenerator import get_random_string
from utils.awsServicesHandler import s3_handler, dynamodb_handler, sns_handler

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
            return {'responseBody': {'response': 'Error: Alumno no encontrado'}, 'statusCode': 404}
        
        if 'foto' not in alumnoData.files:
            responseBody = {'response': 'Error: No file parte'}
            statusCode = 400
        
        foto = alumnoData.files['foto']
        
        s3_filename = f'alumnos/{id}_fotoPerfil.jpg'
        s3_handler.upload_fileobj(foto, BUCKET_NAME, s3_filename)
        fotoUrl = f'https://{BUCKET_NAME}.s3.amazonaws.com/alumnos/{id}_fotoPerfil.jpg'

        responseBody = fotoUrl
        
        alumno_toUpdate.fotoPerfilUrl = fotoUrl
        ConexionDB.session.commit()
        statusCode = 201
        statusCode = 200
        responseBody = {'response': 'Succesfully uploaded', 'fotoPerfilUrl': fotoUrl}
        
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = {'response': f'Error during database transaction: {str(e)}'}
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        statusCode = 500
        responseBody = f"Error en DynamoDB: {error_code} - {error_message}"

    except Exception as e:
        statusCode = 500
        responseBody = f"Error durante la ejecución: {e}"
    
    return {'responseBody': responseBody, 'statusCode': statusCode}
    
def sendAlert(id):
    
    try:
        alumno_ToInspect = Alumno.query.get(id)
        
        if alumno_ToInspect is not None:
            studentData = {
                'id': alumno_ToInspect.IDAlumno,
                'nombre': alumno_ToInspect.nombres,
                'apellido': alumno_ToInspect.apellidos,
                'promedio': alumno_ToInspect.promedio
            }
            
            response = sns_handler.publish(
                TopicArn = ARN_TOPIC,
                Message = json.dumps(studentData),
                Subject = f'Calificaciones del alumno {alumno_ToInspect.nombres}'
            )
            
            responseStatusCode = response['ResponseMetadata']['HTTPStatusCode']
            if responseStatusCode == 200:
                statusCode = 200
                responseBody = {'response': 'Notificación enviada correctamente'}
                
            else:
                statusCode = responseStatusCode
                responseBody = {'response': 'Error: Hubo un problema al enviar la notificación'}
                
        else:
            statusCode = 404
            responseBody = f"No student with ID {id} founded"
            
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = f'Error during database transaction: {str(e)}'
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        statusCode = 500
        responseBody = f"Error en DynamoDB: {error_code} - {error_message}"

    except Exception as e:
        statusCode = 500
        responseBody = f"Error durante la ejecución: {e}"
    
    return {'responseBody': responseBody, 'statusCode': statusCode}


def loginAlumno(id, alumnoData):
    responseBody = 'Invalid input data'
    statusCode = 400
    
    try:
        if 'password' not in alumnoData:
            return {'responseBody': 'Error: No password in request', 'statusCode': 404}
        
        alumno_toLogin = Alumno.query.get(id)
        
        if alumno_toLogin is None:
            return {'responseBody': 'Error: Alumno no encontrado', 'statusCode': 404}
        
        if alumnoData.get('password') == alumno_toLogin.password:
            
            
            tableDynamo = dynamodb_handler.Table(DYNAMODB_NAME)
            
            current_datetime = datetime.utcnow()
            unix_timestamp = int(time.mktime(current_datetime.timetuple()))
            
            newSession = {
                'id': str(alumno_toLogin.IDAlumno),
                'fecha': unix_timestamp,
                'alumnoId': alumno_toLogin.IDAlumno,
                'active': True,
                'sessionString': get_random_string(128)
            }
            
            tableDynamo.put_item(Item = newSession)
            
            statusCode = 200
            responseBody = newSession
            
        else:
            statusCode = 400
            responseBody = "Incorrect Password"
        
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = f'Error during database transaction: {str(e)}'
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        statusCode = 500
        responseBody = f"Error en DynamoDB: {error_code} - {error_message}"

    except Exception as e:
        statusCode = 500
        responseBody = f"Error durante la ejecución: {e}"
    
    return {'responseBody': responseBody, 'statusCode': statusCode}

def verifySessionAlumno(id, alumnoData):
    
    try:
        tableDynamo = dynamodb_handler.Table(DYNAMODB_NAME)
        
        sessionToVerify = tableDynamo.get_item(Key = {'id': id})
        
        if 'Item' in sessionToVerify:
            if alumnoData.get('sessionString') == sessionToVerify['Item'].get('sessionString') and sessionToVerify['Item'].get('active'):
                statusCode = 200
                responseBody = "Valid session"
                
            else:
                statusCode = 400
                responseBody = "Invalid session"
        else:
            statusCode = 400
            responseBody = f"No session with ID {id} founded"
            
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = f'Error during database transaction: {str(e)}'
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        statusCode = 500
        responseBody = f"Error en DynamoDB: {error_code} - {error_message}"

    except Exception as e:
        statusCode = 500
        responseBody = f"Error durante la ejecución: {e}"
    
    return {'responseBody': responseBody, 'statusCode': statusCode}

def logoutAlumno(id, alumnoData):
    
    try:
        tableDynamo = dynamodb_handler.Table(DYNAMODB_NAME)
        
        sessionToLogout = tableDynamo.get_item(Key = {'id': id})
        
        if 'Item' in sessionToLogout:
            if alumnoData.get('sessionString') == sessionToLogout['Item'].get('sessionString'): 

                tableDynamo.update_item(
                    Key = {'id': id},
                    UpdateExpression = 'SET active = :newState',
                    ExpressionAttributeValues = {':newState': False},
                    ReturnValues = 'ALL_NEW'
                )
                
                statusCode = 200
                responseBody = "Session succesfully updated to expired"
                
            else:
                statusCode = 400
                responseBody = "Session not matched"
        else:
            statusCode = 400
            responseBody = f"No session with ID {id} founded"
            
    except SQLAlchemyError as e:
        statusCode = 500
        responseBody = f'Error during database transaction: {str(e)}'
        ConexionDB.session.rollback()
            
    except NoCredentialsError:
        statusCode = 500
        responseBody('Error: AWS credentials not available')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        statusCode = 500
        responseBody = f"Error en DynamoDB: {error_code} - {error_message}"

    except Exception as e:
        statusCode = 500
        responseBody = f"Error durante la ejecución: {e}"
    
    return {'responseBody': responseBody, 'statusCode': statusCode}
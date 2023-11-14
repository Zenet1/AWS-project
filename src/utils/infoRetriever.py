from utils.specifiedTypes import alumno_keys, alumno_types, profesor_keys, profesor_types

def infoRetriever(entityType):
    info_dict = {
        'alumno': {'keys': alumno_keys, 'types': alumno_types},
        'profesor': {'keys': profesor_keys, 'types': profesor_types}
    }
    return info_dict.get(entityType)
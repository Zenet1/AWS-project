from utils.infoRetriever import infoRetriever

def verifyData(data, entityType):
    entityInfo = infoRetriever(entityType)
    
    if verifyKeys(data, entityInfo.get('keys')) and verifyValues(data, entityInfo.get('types')):
        return 1
    else:
        return 0

def verifyKeys(data, correctKeys):
    
    if isinstance(data, dict):
        dataKeys = set(data.keys())
        if dataKeys == correctKeys:
            status = 1
        else:
            status = 0
    else:
        status = 0

    return status
    
def verifyValues(data, correctTypes):
    
    for key, specType in correctTypes.items():
        value = data.get(key)
        if not value or value is None or not isinstance(value, specType):
            return 0
    return 1
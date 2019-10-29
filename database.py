import pymongo, config

connectionUrl = "mongodb+srv://Dom:password1234@cluster0-tgp6l.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

client = pymongo.MongoClient(connectionUrl)

db = client.get_database("Property_Management")

def getAllTenants():
    tenantCollection = db['Tenant']
    return list(tenantCollection.find())

def getAllLandlords():
    landlordCollection = db['LandLord']
    return list(landlordCollection.find())

def getTenant(tenantUsername):
    tenantCollection = db['Tenant']
    tenant = tenantCollection.find_one({'Username': tenantUsername})
    profileImage = fileHandler.getImagePathOrDefault(config.avatarsFolder, tenantUsername)
    tenant['profileImage'] = profileImage
    return tenant

def getLandLord(landLordUsername):
    landLordCollection = db['LandLord']
    landLord = landLordCollection.find_one({'Username': landLordUsername})
    profileImage = fileHandler.getImagePathOrDefault(config.avatarsFolder, landLordUsername)
    landLord['profileImage'] = profileImage
    return landLord
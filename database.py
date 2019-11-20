import pymongo, re
from bson import ObjectId
from . import config
from . helpers.fileHandler import FileHandler
from . models.propertyIssue import PropertyIssue

connectionUrl = "mongodb+srv://Dom:password1234@cluster0-tgp6l.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

client = pymongo.MongoClient(connectionUrl)

db = client.get_database("Property_Management")

fileHandler = FileHandler()


# returns the information of the tenant who has the given username
def getTenant(tenantUsername):
    tenantCollection = db['Tenant']
    tenant = tenantCollection.find_one({"Username": re.compile(tenantUsername, re.IGNORECASE)})
    profileImageName = ""
    if ('Profile Image' in tenant): profileImageName = tenant['Profile Image']
    else: profileImageName = "default.png"
    profileImageAbsolutePath = fileHandler.getImage(config.avatarsFolder, profileImageName)
    tenant['profileImage'] = profileImageAbsolutePath
    return tenant

# returns the information of the landlord who has the given username
def getLandLord(landLordUsername):
    landLordCollection = db['LandLord']
    landLord = landLordCollection.find_one({"Username": re.compile(landLordUsername, re.IGNORECASE)})
    profileImageName = ""
    if ('Profile Image' in landLord): profileImageName = landLord['Profile Image']
    else: profileImageName = "default.jpg"
    profileImageAbsolutePath = fileHandler.getImage(config.avatarsFolder, profileImageName)
    landLord['profileImage'] = profileImageAbsolutePath
    return landLord

def updateLandlordProfilePicture(landLordUsername, profileImageName):
    landLordCollection = db['LandLord']
    landLordCollection.update({"Username": re.compile(landLordUsername, re.IGNORECASE)}, 
                     {'$set' : {'Profile Image' : profileImageName }})


def updateTenantProfilePicture(tenantUsername, profileImageName):
    tenantCollection = db['Tenant']
    tenantCollection.update({"Username": re.compile(tenantUsername, re.IGNORECASE)}, 
                     {'$set' : {'Profile Image' : profileImageName }})
    
# returns all the properties a landlord owns
def getLandLordProperties(landLordUsername) -> list:
    propertiesCollection = db['Property']
    landLordProperties = propertiesCollection.find({'Linked Landlord': re.compile(landLordUsername, re.IGNORECASE)})
    return convertCursorToList(landLordProperties)


# returns the all unresolved issues that a property has.
def getPropertyIssues(propertyId: str, resolved: bool) -> list:
    propertyIssuesCollection = db['Property Issues']
    propertyIssues = propertyIssuesCollection.find({'Linked Property Id': propertyId, 'Resolved': resolved})
    propertyIssues = convertCursorToList(propertyIssues)
    for propertyIssue in propertyIssues:
        propertyId = propertyIssue["Linked Property Id"]
        imageFolderPath = f"{config.propertyIssuesImageFolder}{propertyId}"
        imageAbsolutePath = fileHandler.getImage(imageFolderPath, propertyIssue['Image Name'])
        propertyIssue['Image Absolute Path'] = imageAbsolutePath
    return propertyIssues
    
# converts the given cursor object to a list
def convertCursorToList(cursorObject):
    list = []
    for row in cursorObject:
        list.append(row)
    return list


def addPropertyIssue(propertyIssue: PropertyIssue):
    propertyIssueCollection = db['Property Issues']
    propertyIssueCollection.insert_one(propertyIssue.toDictionary())

def resolvePropertyIssue(propertyIssueId: str):
    propertyIssueId = ObjectId(propertyIssueId)
    propertyIssueCollection = db['Property Issues']
    propertyIssueCollection.update({"_id": propertyIssueId}, 
                     {'$set' : {'Resolved' : True }})
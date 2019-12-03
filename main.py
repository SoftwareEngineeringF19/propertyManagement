from flask import Flask, render_template, request, redirect, url_for, session 
from pathlib import Path
from . import database as db, config
from . helpers.fileHandler import FileHandler
from . helpers.propertyIssueSubmitter import PropertyIssueSubmitter
from . models.propertyIssue import PropertyIssue
from . helpers.userVerifier import UserVerifier

app = Flask(__name__)
app.secret_key = config.secretKey

fileHandler = FileHandler()
userVerifier = UserVerifier()

activeUserKey = "activeUser"

@app.route('/', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'): return render_template('login.html')
    # else it must be a post request...

    username = request.form['username']
    password = request.form['password']

    print(username, password)
    
    if(request.form['loginSubmit'] == 'Login As Landlord'):
        if (userVerifier.landLordExists(username, password)):
            print("valid landlord")
            session[activeUserKey] = username
            return redirect(url_for('showLandLordProfile'))
    else: 
        if (userVerifier.tenantExists(username, password)):
            print("valid tenant")
            session[activeUserKey] = username
            return redirect(url_for('showTenantProfile'))

    return render_template('login.html') # Rerender the login page if the user was not found

@app.route("/tenant/" , methods=['GET', 'POST'])
def showTenantProfile():
    selectedTenantUsername = session[activeUserKey]
    if (not selectedTenantUsername): return render_template('login.html')
    tenant = db.getTenant(selectedTenantUsername)
    return render_template('tenant.html', tenant = tenant)

@app.route("/tenant/WorkSubmission/" , methods=['GET', 'POST'])
def workOrderSubmission():
    if request.method == 'GET':
        return render_template('tenantWorkSubmission.html')
    else:
        propertyIssueSubmitter = PropertyIssueSubmitter()
        userName = session[activeUserKey]
        if (not userName): userName = "bob" # default user name for now
        tenant = db.getTenant(userName)
        issueDescription = request.form.get('issueDescription')
        priority = request.form.get('priority')
        issueImage = request.files['issueImage'] 
        propertyIssue = PropertyIssue(tenant['Linked Property Id'], issueDescription, priority,issueImage, tenant['Username'])
        propertyIssueSubmitter.handlePropertySubmission(propertyIssue)
        return redirect(url_for('showTenantProfile'))
    


@app.route("/landlord/" , methods=['GET', 'POST'])
def showLandLordProfile():
    selectedLandLordUsername = session[activeUserKey]
    print(selectedLandLordUsername)
    if (not selectedLandLordUsername): return render_template('login.html')
    landLord = db.getLandLord(selectedLandLordUsername)
    return render_template('landLord.html', landLord = landLord)

@app.route("/landlord/properties")
def showLandLordProperties():
    landLordProperties = db.getLandLordProperties(session[activeUserKey])
    return render_template('landLordProperties.html', landLordProperties = landLordProperties)

@app.route("/landlord/unresolved-property-issues")
def showUnresolvedPropertyIssues():
    propertyIssues = getPropertyIssues(False)
    return render_template('landLordUnresolvedPropertyIssues.html', propertyIssues = propertyIssues)


@app.route("/landlord/resolved-property-issues") 
def showResolvedPropertyIssues():
    propertyIssues = getPropertyIssues(True)
    return render_template('landLordResolvedPropertyIssues.html', propertyIssues = propertyIssues)


def getPropertyIssues(resolvedStatus: bool):
    landLordProperties = db.getLandLordProperties(session[activeUserKey])
    propertyIssues = {}
    for property in landLordProperties:
        propertyId = str(property['_id'])
        propertyIssues[propertyId] = [property]
        propertyIssues[propertyId].append(db.getPropertyIssues(propertyId, resolvedStatus))
    return propertyIssues

@app.route("/landlordResolvePropertyIssue", methods = ['POST'])
def handlePropertyIssueResolving():
    propertyIssueId = request.form['propertyIssueId']
    db.resolvePropertyIssue(propertyIssueId)
    return redirect(url_for('showUnresolvedPropertyIssues'))    

@app.route("/changeAvatar/", methods = ['POST'])
def changeAvatar():
    userName = session[activeUserKey]
    image = request.files['image'] 
    fileExtension = Path(image.filename).suffix
    image.filename = f"{userName}{fileExtension}"
    return_url = request.referrer
    fileHandler.saveImage(config.avatarsFolder, image)

    if ('tenant' in return_url): 
        db.updateTenantProfilePicture(userName, image.filename)
        return redirect(url_for('showTenantProfile'))
    else: 
        db.updateLandlordProfilePicture(userName, image.filename)
        return redirect(url_for('showLandLordProfile'))

db.getLandLordProperties('greastern')

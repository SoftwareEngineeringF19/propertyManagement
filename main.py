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

@app.route("/landlord/propertyIssues")
def showPropertyIssues():
    landLordProperties = db.getLandLordProperties(session[activeUserKey])
    propertyIssues = {}
    for property in landLordProperties:
        propertyId = str(property['_id'])
        propertyIssues[propertyId] = [property]
        propertyIssues[propertyId].append(db.getPropertyIssues(propertyId))
    
    print(propertyIssues['5db852321c9d4400004c7d3a'][1])
    return render_template('landLordPropertyIssues.html', propertyIssues = propertyIssues)
       

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


# from flask import Flask, redirect, url_for, session, request
# from flask_oauth import OAuth


# SECRET_KEY = 'development key'
# DEBUG = True
# FACEBOOK_APP_ID = '188477911223606'
# FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'


# app = Flask(__name__)
# app.debug = DEBUG
# app.secret_key = SECRET_KEY
# oauth = OAuth()

# facebook = oauth.remote_app('facebook',
#     base_url='https://graph.facebook.com/',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key=FACEBOOK_APP_ID,
#     consumer_secret=FACEBOOK_APP_SECRET,
#     request_token_params={'scope': 'email'}
# )


# @app.route('/')
# def index():
#     return redirect(url_for('login'))


# @app.route('/login')
# def login():
#     return facebook.authorize(callback=url_for('facebook_authorized',
#         next=request.args.get('next') or request.referrer or None,
#         _external=True))


# @app.route('/login/authorized')
# @facebook.authorized_handler
# def facebook_authorized(resp):
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['oauth_token'] = (resp['access_token'], '')
#     me = facebook.get('/me')
#     return 'Logged in as id=%s name=%s redirect=%s' % \
#         (me.data['id'], me.data['name'], request.args.get('next'))


# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('oauth_token')


# if __name__ == '__main__':
#     app.run()

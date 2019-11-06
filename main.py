from flask import Flask, render_template, request, redirect, url_for, session 
from . import database as db, config
from . helpers.fileHandler import FileHandler
from . helpers.propertyIssueSubmitter import PropertyIssueSubmitter
from . models.propertyIssue import PropertyIssue
from . helpers.userVerifier import UserVerifier

d = UserVerifier()

app = Flask(__name__)
app.secret_key = config.secretKey

fileHandler = FileHandler()

activeUserKey = "activeUser"

@app.route('/', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'): return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    
    if(request.form['loginSubmit'] == 'Login As Landlord'): print("hi")
        
    else: print("hi")


@app.route("/tenant/" , methods=['GET', 'POST'])
def showTenantProfile():
    selectedTenantUsername = request.form.get('tenant-select')
    session[activeUserKey] = selectedTenantUsername 
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
        return login()
    


@app.route("/landlord/" , methods=['GET', 'POST'])
def showLandLordProfile():
    selectedLandLordUsername = request.form.get('landlord-select')
    session[activeUserKey] = selectedLandLordUsername
    landLord = db.getLandLord(selectedLandLordUsername)
    return render_template('landLord.html', landLord = landLord)

@app.route("/changeAvatar/", methods = ['POST'])
def changeAvatar():
    userName = session[activeUserKey]
    image = request.files['image'] 
    image.filename = f"{userName}.png"
    print(userName)
    return_url = request.referrer
    fileHandler.saveImage(config.avatarsFolder, image)

    if ('tenant' in return_url):
        tenant = db.getTenant(userName)
        return render_template('tenant.html', tenant = tenant)
    else:
        landLord = db.getLandLord(userName)
        return render_template('landlord.html', landLord = landLord)


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

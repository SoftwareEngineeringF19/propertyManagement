import database as db
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://<gaius>:<password123>@cluster0-tgp6l.gcp.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)

client = pymongo.MongoClient("mongodb+srv://<gaius>:<password123>@cluster0-tgp6l.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

@app.route('/')
def index():
    landlords = db.getAllLandlords()
    tenants = db.getAllTenants()
    data = {
        "landlords" : landlords,
        "tenants" : tenants
    }
    return render_template('index.html', data=data)

@app.route("/tenant/" , methods=['GET', 'POST'])
def showTenantProfile():
    selectedTenantUsername = request.form.get('tenant-select')
    tenant = db.getTenant(selectedTenantUsername)
    return render_template('tenant.html', tenant = tenant)


@app.route("/landlord/" , methods=['GET', 'POST'])
def showLandlordProfile():
    selectedLandLordUsername = request.form.get('landlord-select')
    landLord = db.getLandLord(selectedLandLordUsername)
    return render_template('landLord.html', landLord = landLord)


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

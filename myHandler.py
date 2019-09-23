import database as db
from flask import Flask, render_template, request
app = Flask(__name__)

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




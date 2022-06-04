from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3307/doctors'
# Add Secret Key
app.config['SECRET_KEY'] = 'super secret sweet key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#db.create_all()
#db.session.commit()

# Create Contracts Model (Table)
class Contracts(db.Model):
    contract_number = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    date = db.Column(db.String(12), nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, contract_number, date, sum):
        self.contract_number = contract_number
        self.date = date
        self.sum = sum


class ContractForm(FlaskForm):
    contract_number = StringField("Contract Number", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    sum =  StringField("Sum Of contract", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/contract/add', methods=['GET', 'POST'])
def add_contract():
    contract_number = None
    form = ContractForm()
    if form.validate_on_submit():
        contract_number = Contracts.query.filter_by(contract_number=form.contract_number.data).first()
        if contract_number is None:
            contract_number = Contracts(contract_number=form.contract_number.data, date=form.date.data, sum=form.sum.data)
            db.session.add(contract_number)
            db.session.commit()
        contract_number = form.contract_number.data
        form.contract_number.data = ''
        form.date.data = ''
        form.sum.data = ''
        flash("Contract Added Successfully!")
    our_contracts = Contracts.query.order_by(Contracts.date_added)
    return render_template('add_contract.html', form=form, contract_number=contract_number, our_contracts=our_contracts)


@app.route('/update_contract/<int:contract_number>', methods=['GET', 'POST'])
def update_contract(contract_number):
    form = ContractForm()
    contract_to_update = Contracts.query.get_or_404(contract_number)
    if request.method == "POST":
        contract_to_update.contract_number = request.form['contract_number']
        contract_to_update.date = request.form['date']
        contract_to_update.sum = request.form.get('sum')
        try:
            db.session.commit()
            flash('Contract Updated Successfully!')
            return render_template('update_contract.html', form=form, contract_to_update=contract_to_update)
        except:
            flash('Error... Try again!')
            return render_template('update_contract.html', form=form, contract_to_update=contract_to_update)
    else:
        return render_template("update_contract.html", form=form, contract_to_update=contract_to_update, contract_number=contract_number)


@app.route('/delete/contract/<int:contract_number>')
def delete_contract(contract_number):
    contract_to_delete = Contracts.query.get_or_404(contract_number)
    contract_number = None
    form = ContractForm()
    try:
        db.session.delete(contract_to_delete)
        db.session.commit()
        flash('Contract Deleted Successfully!')

        our_contracts = Contracts.query.order_by(Contracts.date_added)
        return render_template('add_contract.html', form=form, contract_number=contract_number, our_contracts=our_contracts)
    except:
        flash('Error Deleting Contract')
        return render_template('add_contract.html', form=form, contract_number=contract_number, our_contracts=our_contracts)


# Create Patients Model (Table)
class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    insurance_number = db.Column(db.String(6), nullable=False)
    phone_number =db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(10))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, address, insurance_number, phone_number, sex):
        self.name = name
        self.address = address
        self.insurance_number = insurance_number    
        self.phone_number = phone_number
        self.sex = sex

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create A Form Class For Patient
class PatientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    insurance_number =  StringField("Insurance Number", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    sex = StringField("Sex", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/patient/add', methods=['GET', 'POST'])
def add_patient():
    name = None
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patients.query.filter_by(name=form.name.data).first()
        if patient is None:
            patient = Patients(name=form.name.data, address=form.address.data, 
                insurance_number=form.insurance_number.data,
                phone_number=form.phone_number.data, sex=form.sex.data)
            db.session.add(patient)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.address.data = ''
        form.insurance_number.data = ''
        form.phone_number.data = ''
        form.sex.data = ''
        flash("Patient Added Successfully!")
    our_patients = Patients.query.order_by(Patients.date_added)
    return render_template('add_patient.html', form=form, name=name, our_patients=our_patients)


@app.route('/update_patient/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    form = PatientForm()
    name_to_update = Patients.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.address = request.form['address']
        name_to_update.insurance_number = request.form.get('insurance_number')
        name_to_update.phone_number = request.form.get('phone_number')
        name_to_update.sex = request.form.get('sex')
        try:
            db.session.commit()
            flash('Patient Updated Successfully!')
            return render_template('update_patient.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error... Try again!')
            return render_template('update_patient.html', form=form, name_to_update=name_to_update)
    else:
        return render_template("update_patient.html", form=form, name_to_update=name_to_update, id=id)


@app.route('/delete/patient/<int:id>')
def delete_patient(id):
    patient_to_delete = Patients.query.get_or_404(id)
    name = None
    form = PatientForm()
    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash('Patient Deleted Successfully!')

        our_patients = Patients.query.order_by(Patients.date_added)
        return render_template('add_patient.html', form=form, name=name, our_patients=our_patients)
    except:
        flash('Error Deleting Patient')
        return render_template('add_patient.html', form=form, name=name, our_patients=our_patients)



# Create Doctors Model (Table)
class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(120), nullable=False, unique=True)
    room = db.Column(db.Integer, nullable=False)
    time =db.Column(db.String(12), nullable=False)
    service = db.Column(db.String(200))
    contract_number = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, position, room, time, service, contract_number):
        self.name = name
        self.position = position
        self.room = room    
        self.time = time
        self.service = service
        self.contract_number = contract_number

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name
    

@app.route('/create/<tablename>')
def create_table(tablename):
    try:
        if tablename == 'Doctors':
            Doctors.__table__.create(db.engine)
        if tablename == 'Patients':
            Patients.__table__.create(db.engine)
        if tablename == 'Contracts':
            Contracts.__table__.create(db.engine)
        flash_message = tablename + ' Table Created Successfully!'
        flash(flash_message)
        return render_template('index.html')
    except:
        flash_message = 'Problem Creating' + tablename + 'Table...'
        flash(flash_message)
        return render_template('index.html')


@app.route('/drop/<tablename>')
def delete_table(tablename):
    try:
        if tablename == 'Doctors':
            Doctors.__table__.drop(db.engine)
        if tablename == 'Patients':
            Patients.__table__.drop(db.engine)
        if tablename == 'Contracts':
            Contracts.__table__.drop(db.engine)
        flash_message = tablename + ' Table Was Dropped!'
        flash(flash_message)
        return render_template('index.html')
    except:
        flash_message = 'Problem Dropping ' + tablename + ' Table...'
        flash(flash_message)
        return render_template('index.html')


# Create a Form Class
class DoctorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    room =  StringField("Room", validators=[DataRequired()])
    time = StringField("Working Hours", validators=[DataRequired()])
    service = StringField("Servises", validators=[DataRequired()])
    contract_number = StringField("Contract Number", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/delete/<int:id>')
def delete(id):
    doctor_to_delete = Doctors.query.get_or_404(id)
    name = None
    form = DoctorForm()
    try:
        db.session.delete(doctor_to_delete)
        db.session.commit()
        flash('Doctor Deleted Successfully!')

        our_doctors = Doctors.query.order_by(Doctors.date_added)
        return render_template('add_doctor.html', form=form, name=name, our_doctors=our_doctors)
    except:
        flash('Error deleting doctor')
        return render_template('add_doctor.html', form=form, name=name, our_doctors=our_doctors)


# Update Doctror Record
@app.route('/update_doctor/<int:id>', methods=['GET', 'POST'])
def update_doctor(id):
    form = DoctorForm()
    name_to_update = Doctors.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.position = request.form['position']
        name_to_update.room = request.form.get('room')
        name_to_update.time = request.form.get('time')
        name_to_update.service = request.form.get('service')
        name_to_update.contract_number = request.form.get('contract_number')
        try:
            db.session.commit()
            flash('Doctor Updated Successfully!')
            return render_template('update_doctor.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error... Try again!')
            return render_template('update_doctor.html', form=form, name_to_update=name_to_update)
    else:
        return render_template("update_doctor.html", form=form, name_to_update=name_to_update, id=id)

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Add Doctor
@app.route('/doctor/add', methods=['GET', 'POST'])
def add_doctor():
    name = None
    form = DoctorForm()

    if form.validate_on_submit():
        doctor = Doctors.query.filter_by(name=form.name.data).first()
        if doctor is None:
            doctor = Doctors(name=form.name.data, position=form.position.data, room=form.room.data,
                time=form.time.data, service=form.service.data, contract_number=form.contract_number.data)
            db.session.add(doctor)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.position.data = ''
        form.room.data = ''
        form.time.data = ''
        form.service.data = ''
        form.contract_number.data = ''
        flash("Doctor Added Successfully!")
    our_doctors = Doctors.query.order_by(Doctors.date_added)
    return render_template('add_doctor.html', form=form, name=name, our_doctors=our_doctors)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error 
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template('name.html', name = name, form = form)


app.run(host='localhost', port=5000, debug=True)






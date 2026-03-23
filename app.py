from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key_123'

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'clinic.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(50), nullable=False)
    pet_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # In production use hashed passwords!

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.json
        new_appointment = Appointment(
            pet_type=data.get('pet_type'),
            pet_name=data.get('pet_name'),
            owner_name=data.get('owner_name'),
            phone=data.get('phone'),
            email=data.get('email'),
            city=data.get('city'),
            date=data.get('date'),
            branch=data.get('branch'),
            message=data.get('message', '')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"success": True, "message": "Your Appointment has been successfully booked. We sent a mail to your registered mobile number."})
    except Exception as e:
        print(f"Error booking appointment: {e}")
        return jsonify({"success": False, "message": "Failed to book appointment."}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple hardcoded check or DB check
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect(url_for('appointments'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/appointments')
def appointments():
    # In a real app, you would check if user is logged in here using sessions
    all_appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template('appointments.html', appointments=all_appointments)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables and a default admin user if it doesn't exist
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='password') # Simple default credentials
            db.session.add(admin_user)
            db.session.commit()
            
    app.run(debug=True)

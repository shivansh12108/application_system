from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from functools import wraps
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'xyzsdfg'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'application_form_db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mysql = MySQL(app)

# ---------------- Helper: Require Admin Login ---------------- #
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_loggedin' not in session:
            flash("Please login as admin to access this page.", "warning")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- User Routes ---------------- #
@app.route('/', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        age = request.form['age']
        email = request.form['email']
        position = request.form['position']
        languages = ', '.join(request.form.getlist('languages'))
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        mobile = request.form['mobile']
        github = request.form['github']
        linkedin = request.form['linkedin']
        resume_file = request.files.get('resume')
        resume_filename = None
        if resume_file and allowed_file(resume_file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            resume_filename = secure_filename(email + '_' + resume_file.filename)
            resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
        else:
            mesage = 'Please upload a valid PDF resume.'
            return render_template('form.html', mesage=mesage)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM applicants WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account with this email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address!'
        elif password != confirm_password:
            mesage = 'Passwords do not match!'
        elif not all([first_name, last_name, dob, gender, age, email, position, languages, password, mobile, github, linkedin, resume_filename]):
            mesage = 'Please fill out the complete form!'
        else:
            cursor.execute('''
                INSERT INTO applicants 
                (first_name, last_name, dob, gender, age, email, position, languages, password, mobile, github, linkedin, resume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (first_name, last_name, dob, gender, age, email, position, languages, password, mobile, github, linkedin, resume_filename))
            mysql.connection.commit()
            mesage = 'Application submitted successfully!'
            return render_template('success.html', mesage=mesage)
    return render_template('form.html', mesage=mesage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM applicants WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['first_name']
            session['email'] = user['email']
            mesage = 'Logged in successfully!'
            return render_template('user.html', mesage=mesage, user=user)
        else:
            mesage = 'Incorrect email or password!'

    return render_template('login.html', mesage=mesage)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- Admin Routes ---------------- #
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    mesage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE email = %s AND password = %s', (email, password))
        admin = cursor.fetchone()

        if admin:
            session['admin_loggedin'] = True
            session['admin_id'] = admin['id']
            session['admin_email'] = admin['email']
            return redirect(url_for('admin_dashboard'))
        else:
            mesage = 'Invalid admin credentials!'

    return render_template('admin_login.html', mesage=mesage)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_login_required
def admin_dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applicants')
    applicants = cursor.fetchall()
    return render_template('admin_dashboard.html', applicants=applicants)

@app.route('/admin/create', methods=['GET', 'POST'])
@admin_login_required
def admin_create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        age = request.form['age']
        email = request.form['email']
        position = request.form['position']
        languages = ', '.join(request.form.getlist('languages'))
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO applicants 
            (first_name, last_name, dob, gender, age, email, position, languages, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, dob, gender, age, email, position, languages, password))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_form.html', form_type='create')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applicants WHERE id = %s', (id,))
    applicant = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        age = request.form['age']
        email = request.form['email']
        position = request.form['position']
        languages = ', '.join(request.form.getlist('languages'))
        password = request.form['password'] if request.form['password'] else applicant['password']

        cursor.execute('''
            UPDATE applicants SET 
            first_name=%s, last_name=%s, dob=%s, gender=%s, age=%s, email=%s, position=%s, languages=%s, password=%s
            WHERE id=%s
        ''', (first_name, last_name, dob, gender, age, email, position, languages, password, id))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_form.html', applicant=applicant, form_type='edit')

@app.route('/admin/delete/<int:id>', methods=['POST'])
@admin_login_required
def admin_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM applicants WHERE id = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------------- Run App ---------------- #
if __name__ == '__main__':
    app.run(debug=True)

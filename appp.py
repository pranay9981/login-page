from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key in production

# User authentication manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user data (replace with DB in production)
users = {'admin': {'password': 'password123'}}  # Example user credentials

# User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Login form class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Registration form class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# User loader
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Upload folder configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route to render the frontend
@app.route('/')
@login_required
def index():
    videos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', videos=videos)

# Route for video upload
@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('Video uploaded successfully', 'success')  # Feedback on successful upload
    return redirect(url_for('index'))

# Route for streaming videos
@app.route('/stream/<filename>')
@login_required
def stream_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout', methods=['GET'])  # Only GET method allowed
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')  # Feedback on logout
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Here you should add logic to save the new user
        # For simplicity, we will just add to the dummy user data
        if username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = {'password': password}  # Store the new user
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Run the application
if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)

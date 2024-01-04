from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import check_password_hash
from src.views.forms.registration_form import RegistrationForm
from src.views.forms.login_form import LoginForm
from src.views.forms.scheduler_form import SchedulerForm  # Fix import error
 # Fix import error
from src.models.user import User
from src.controllers import user_controller, scheduler_controller, attendance_controller, \
    alert_controller, document_controller, chatbot_controller, report_controller

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)

# Register blueprints
from src.views import user_bp
app.register_blueprint(user_bp)
app.register_blueprint(scheduler_controller.scheduler_bp)
app.register_blueprint(attendance_controller.attendance_bp)
app.register_blueprint(alert_controller.alert_bp)
app.register_blueprint(document_controller.document_bp)
app.register_blueprint(chatbot_controller.chatbot_bp)
app.register_blueprint(report_controller.report_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/upload_schedule', methods=['GET', 'POST'])
def upload_schedule():
    form = SchedulerForm()
    # Add logic to handle schedule form submission
    return render_template('upload_schedule.html', title='Upload Schedule', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)

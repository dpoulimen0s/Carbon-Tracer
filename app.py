# Author: Dimitrios Poulimenos

# Imports
import socket
import logging
from flask_login import current_user, LoginManager
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Author: Dimitrios Poulimenos
# Config
app = Flask(__name__)

app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfFdRMcAAAAAEeOwLocqoG8LhRNZhE0TYF8MdMG"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfFdRMcAAAAAILSgmbrJcTLnkDV5fG-xwPzyoR4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# Author: Dimitrios Poulimenos
# Functions
def requires_roles(*roles):
    '''Takes role and Send unauthorised access attempt notification to security log file '''

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Send unauthorised access attempt notification to security log file.
                logging.warning('SECURITY - Unauthorised access attempt [%s, %s, %s, %s]',
                                current_user.id,
                                current_user.email,
                                current_user.role,
                                request.remote_addr)
                # redirect the user to an unauthorised notice!
                return render_template('errors/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


# Author: Dimitrios Poulimenos
# Home Page View
@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'admin':
        return render_template('users/profile.html')
    else:
        return render_template('index.html')


# Author: Dimitrios Poulimenos
# Error Page Views
@app.errorhandler(400)
def internal_error(error):
    return render_template('errors/400.html'), 400


# Author: Dimitrios Poulimenos
@app.errorhandler(403)
def page_forbidden(error):
    return render_template('errors/403.html'), 403


# Author: Dimitrios Poulimenos
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


# Author: Dimitrios Poulimenos
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


# Author: Dimitrios Poulimenos
@app.errorhandler(503)
def internal_error(error):
    return render_template('errors/503.html'), 503


# Author: Dimitrios Poulimenos
if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    # free_port = free_socket.getsockname()[1]
    free_port = 5000
    free_socket.close()

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # BLUEPRINTS
    # import blueprints
    from users.views import users_blueprint
    from calculator.views import calculator_blueprint
    from admin.views import admin_blueprint
    from quiz.views import quiz_blueprint

    # register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(calculator_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(quiz_blueprint)
    app.run(host=my_host, port=free_port, debug=True)

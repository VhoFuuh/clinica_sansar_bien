import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_limiter.util import get_remote_address

# Importar extensiones desde un archivo separado
from app.extensions import db, login_manager, bcrypt, limiter, mail

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuraciones generales
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de correo
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    bcrypt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # Importar modelos para que SQLAlchemy los registre
    from app.models import user, paciente, turno, examen  # ✅ correcto


    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))

    # Registrar blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.paciente import paciente_bp, formatear_rut
    app.register_blueprint(paciente_bp)
    app.jinja_env.filters['formatear_rut'] = formatear_rut

    from app.routes.turno import turno_bp
    app.register_blueprint(turno_bp)

    from app.routes.user import user_bp
    app.register_blueprint(user_bp)

    from app.routes.examen import examen_bp
    app.register_blueprint(examen_bp)

    return app

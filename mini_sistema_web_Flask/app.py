# ============================================================
# app.py - Punto de entrada del mini-sistema web con Flask
# Proyecto: U1 - A5 Desarrollo de Bases de Datos para Web
# ============================================================

from flask import Flask, render_template
from config import Config
from models import db
from models.user import User
from routes.user_routes import user_bp
from flask_wtf import CSRFProtect


def create_app():
    """Factory pattern: crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensiones
    db.init_app(app)
    CSRFProtect(app)

    # Blueprint de usuarios
    app.register_blueprint(user_bp)

    # Ruta raíz: lista de usuarios registrados
    @app.route('/')
    def index():
        users = User.query.order_by(User.id).all()
        return render_template('user_list.html', users=users)

    # Error 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template('base.html', error="Página no encontrada"), 404

    # Crear tablas al iniciar
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
from flask import Flask
from config import Config
from models import db
from models.user import User
from routes.user_routes import user_bp
from flask_wtf.csrf import CSRFProtect, generate_csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar protección CSRF
    CSRFProtect(app)
    
    db.init_app(app)

    # Pasar csrf_token a todas las plantillas (esto soluciona el error)
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)

    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
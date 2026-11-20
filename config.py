import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-super-secreta-cambiar")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
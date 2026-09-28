# ============================================================
# config.py - Configuración de la aplicación
# ============================================================

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-u1-a5-2026'

    # Conexión a MySQL con PyMySQL
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:22MORANbay@localhost:3306/mini_sistema_usuarios'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
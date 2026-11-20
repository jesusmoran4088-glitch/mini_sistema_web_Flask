import os
import sys

# Esto asegura que Python encuentre tu app.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

import pytest
import app as app_module

@pytest.fixture
def client():
    # Buscamos la variable de Flask (por si se llama app, application, etc.)
    flask_app = getattr(app_module, 'app', getattr(app_module, 'application', None))
    
    if not flask_app:
        pytest.fail("No se encontró la variable app o application en app.py")
        
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False # Por si usas formularios
    
    with flask_app.test_client() as client:
        yield client

def test_index(client):
    """Prueba que la página principal cargue."""
    response = client.get('/')
    # Aceptamos 200 (OK) o 302 (Redirección si pide login)
    assert response.status_code in [200, 302]
import pytest
import app

def test_index(client):
    """Prueba que la página principal responda."""
    response = client.get('/')
    assert response.status_code in [200, 302]

@pytest.fixture
def client():
    # Busca CUALQUIER cosa que sea una app de Flask en tu archivo
    flask_app = None
    for name in dir(app):
        obj = getattr(app, name)
        if obj.__class__.__name__ == 'Flask':
            flask_app = obj
            break
            
    # Si usa el patrón create_app()
    if not flask_app and hasattr(app, 'create_app'):
        flask_app = app.create_app()
        
    if not flask_app:
        pytest.fail("No se encontró ninguna app de Flask en el archivo app.py")
        
    flask_app.config['TESTING'] = True
    return flask_app.test_client()
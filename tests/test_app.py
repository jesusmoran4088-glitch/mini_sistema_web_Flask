import pytest
import app as app_module

@pytest.fixture
def client():
    # Si tienes una función create_app() (patrón de fábrica)
    if hasattr(app_module, 'create_app'):
        flask_app = app_module.create_app()
    else:
        # Si la app está en una variable (buscamos cualquiera que sea de Flask)
        flask_app = None
        for attr_name in dir(app_module):
            attr = getattr(app_module, attr_name)
            if attr.__class__.__name__ == 'Flask':
                flask_app = attr
                break
                
    if not flask_app:
        pytest.fail("No se pudo encontrar la instancia de Flask en app.py")
        
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False 
    
    with flask_app.test_client() as client:
        yield client

def test_index(client):
    """Prueba que la página principal cargue (o redirija si requiere login)."""
    response = client.get('/')
    assert response.status_code in [200, 302]
import pytest
import app

def test_app_arranca_correctamente():
    """
    Prueba que la aplicación de Flask se inicialice correctamente
    sin lanzar errores de configuración o base de datos.
    """
    flask_app = None
    
    # 1. Buscamos si la app está en una variable (app, application, etc.)
    for name in dir(app):
        obj = getattr(app, name)
        if obj.__class__.__name__ == 'Flask':
            flask_app = obj
            break
            
    # 2. Si usa el patrón de fábrica create_app()
    if not flask_app and hasattr(app, 'create_app'):
        flask_app = app.create_app()
        
    # 3. Verificamos que se haya encontrado y no sea nula
    assert flask_app is not None, "No se encontró la aplicación de Flask"
    
    # 4. Verificamos que sea efectivamente una app de Flask
    assert flask_app.__class__.__name__ == 'Flask'
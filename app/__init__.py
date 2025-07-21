from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "Carlos"
    # Registrar rutas desde el blueprint
    from Controladores.routes import main
    app.register_blueprint(main)
    Comprobantes_Ruta='app/static/Comprobantes_Pago'
    app.config['Comprobantes_Ruta']=Comprobantes_Ruta
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
    return app

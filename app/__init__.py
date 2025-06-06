from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.parts import parts_bp
from .extensions import ma, limiter
from .extensions import ma, limiter, cache
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'                                                               #URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'                                                        #Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app.name': "Mechanic Shop API"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #INITIALIZE EXTENSIONS
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)    
    
    
    #REGISTER BLUEPRINTS
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)     
    
    return app
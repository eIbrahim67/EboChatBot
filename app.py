from flask import Flask
from flask_talisman import Talisman
from config import AppConfig
from logging_config import setup_logging
from presentation.api_routes import api_blueprint
from presentation.error_handlers import register_error_handlers

config = AppConfig()

def create_app():
    app = Flask(__name__)
    Talisman(app)  # Enforces HTTPS and adds security headers
    app.register_blueprint(api_blueprint, url_prefix='/')
    register_error_handlers(app)
    return app


if __name__ == '__main__':
    setup_logging()
    app = create_app()
    app.run(debug=(config.ENVIRONMENT == "development"), host='0.0.0.0', port=5000)
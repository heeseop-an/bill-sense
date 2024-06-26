from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    from app.routes.invoice_routes import invoice_bp
    app.register_blueprint(invoice_bp, url_prefix='/api')

    return app
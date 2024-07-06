from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    from app.routes.invoice_routes import invoice_bp

    app.register_blueprint(invoice_bp, url_prefix="/api")

    return app

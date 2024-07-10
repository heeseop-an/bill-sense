from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    # create uploads directory if it doesn't exist
    uploads_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "uploads"
    )
    os.makedirs(uploads_dir, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = uploads_dir
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    from app.routes.invoice_routes import invoice_bp

    app.register_blueprint(invoice_bp, url_prefix="/api")

    return app

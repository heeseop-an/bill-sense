from flask import Blueprint, send_file, request, current_app
from typing import Set, Tuple
from app.gemini import analyze_invoice
import pandas as pd
import os

invoice_bp = Blueprint("invoice", __name__)

ALLOWED_EXTENSIONS: Set[str] = {"png", "jpg", "jpeg", "pdf", "zip"}


def is_allowed_file(filename: str) -> bool:

    if "." not in filename:
        return False

    filename_parts: list[str] = filename.rsplit(".", 1)
    file_extension: str = filename_parts[1].lower()

    return file_extension in ALLOWED_EXTENSIONS


@invoice_bp.route("/invoice", methods=["POST"])
def upload_file() -> Tuple[str, int]:

    file = request.files["file"]

    if file and is_allowed_file(file.filename):

        filename = file.filename
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        results = analyze_invoice(filepath)

        df = pd.DataFrame(results)

        csv_filename = f"{file.filename.rsplit(".", 1)[0]}_extracted.csv"
        csv_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], csv_filename)

        df.to_csv(csv_filepath, index=False)

        return send_file(csv_filepath, as_attachment=True)



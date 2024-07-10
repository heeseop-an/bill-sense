from flask import Blueprint, send_file, request, current_app, jsonify
import pandas as pd
import os
import logging

invoice_bp = Blueprint("invoice", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def is_allowed_file(filename):
    if "." not in filename:
        return False

    filename_parts = filename.rsplit(".", 1)
    file_extension = filename_parts[1].lower()

    return file_extension in ALLOWED_EXTENSIONS


@invoice_bp.route("/invoice", methods=["POST"])
def upload_file():
    logging.info("Log in upload_file: Received request to /api/invoice")
    logging.info(
        f"Log in upload_file: UPLOAD_FOLDER: {current_app.config['UPLOAD_FOLDER']}"
    )

    if "file" not in request.files:
        logging.error("Error in upload_file: No file part in the request")
        return jsonify({"Error in upload_file": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        logging.error("Error in upload_file: No file selected")
        return jsonify({"Error in upload_file": "No file selected"}), 400

    if file and is_allowed_file(file.filename):
        try:
            filename = file.filename
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            logging.info(f"Log in upload_file: Attempting to save file to: {filepath}")
            file.save(filepath)
            logging.info(f"Log in upload_file: File saved successfully to {filepath}")

            logging.info("Log in upload_file: Analyzing invoice...")
            from app.gemini import analyze_invoice

            results = analyze_invoice(filepath)
            logging.info(f"Log in upload_file: Invoice analysis results: {results}")

            if isinstance(results, list) and results and "error" in results[0]:
                return jsonify(results[0]), 500

            df = pd.DataFrame(results)

            csv_filename = f"{filename.rsplit('.', 1)[0]}_extracted.csv"
            csv_filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], csv_filename
            )
            logging.info(f"Log in upload_file: Saving CSV to: {csv_filepath}")

            df.to_csv(csv_filepath, index=False)
            logging.info(
                f"Log in upload_file: CSV file created successfully at {csv_filepath}"
            )

            return send_file(csv_filepath, as_attachment=True)
        except Exception as e:
            logging.error(
                f"Error in upload_file: Error processing file: {str(e)}", exc_info=True
            )
            return jsonify({"Error in upload_file": str(e)}), 500
    else:
        logging.error(f"Error in upload_file: File type not allowed: {file.filename}")
        return jsonify({"Error in upload_file": "File type not allowed"}), 400

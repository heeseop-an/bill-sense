import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import json
import logging
import re

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def analyze_invoice(file_path):
    model = genai.GenerativeModel("gemini-pro-vision")
    if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(file_path)
        return process_image(model, image)
    else:
        logging.error("Error in analyze_invoice: Unsupported file format")
        return None


def process_image(model, image):
    prompt = """
    Analyze this invoice image and extract the following information:
    - Item names
    - Item numbers (if available)
    - Quantities
    - Unit prices
    - Total price for each item

    Format the output as a JSON object with a list of items, where each item is a dictionary.
    """

    try:
        response = model.generate_content([prompt, image])
        logging.info(f"Log in process_image: Raw API response: {response.text}")

        # remove markdown code block if present
        json_string = re.sub(r"```json\n|\n```", "", response.text).strip()

        try:
            parsed_data = json.loads(json_string)
            return parsed_data.get("items", [])
        except json.JSONDecodeError as json_error:
            logging.error(
                f"Error in process_image: Failed to parse API response as JSON. Error: {str(json_error)}"
            )
            return [
                {
                    "Error in process_image": "Failed to parse API response",
                    "raw_response": response.text,
                }
            ]

    except Exception as e:
        logging.error(f"Error in process_image: {str(e)}", exc_info=True)
        return None

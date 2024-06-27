import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def analyze_invoice(image_path):
    model = genai.GenerativeModel('gemini-pro-vision')

    image = Image.open(image_path)

    prompt = """
    Analyze this invoice image and extract the following information:
    - Item names
    - Item numbers (if available)
    - Quantities
    - Unit prices
    - Total price for each item

    Format the output as a JSON object.
    """

    response = model.generate_content([prompt, image])
    return response.text

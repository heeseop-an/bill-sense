# sample_invoice.png source: https://invoicehome.com/

import sys
import os
import json

from app.utils.gemini import analyze_invoice

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    if len(sys.argv) < 2:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_invoice_path = os.path.join(script_dir, '..', 'test_data', 'sample_invoice.png')
        if not os.path.exists(sample_invoice_path):
            print(f"Sample invoice not found at {sample_invoice_path}")
            print("Usage: python -m tests.test_invoice [path_to_invoice_image]")
            sys.exit(1)
        image_path = sample_invoice_path
    else:
        image_path = sys.argv[1]

    try:
        result = analyze_invoice(image_path)

        try:
            parsed_result = json.loads(result)
            print(json.dumps(parsed_result, indent=2))
        except json.JSONDecodeError:
            print(result)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

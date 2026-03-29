import requests
import os
from image_processor import process_image

RAW_FOLDER = "data/images_raw"
os.makedirs(RAW_FOLDER, exist_ok=True)

def download_image(url, product_name, index):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save all images directly in RAW_FOLDER
            filename = f"{product_name}_{index}.jpg"
            path = os.path.join(RAW_FOLDER, filename)

            with open(path, "wb") as f:
                f.write(response.content)

            # Process image after download
            processed_path = process_image(path)

            return path, processed_path

    except Exception as e:
        print("Download failed:", e)

    return None, None
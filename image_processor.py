import cv2
import numpy as np
import os

RAW_FOLDER = "data/images_raw"
OUTPUT_FOLDER = "data/images_process"
LOGO_PATH = "assets/aiko_logo.png"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load logo with transparency
logo = cv2.imread(LOGO_PATH, cv2.IMREAD_UNCHANGED)

logo_width = 120
logo_height = 40
logo = cv2.resize(logo, (logo_width, logo_height))

logo_rgb = logo[:, :, :3]
alpha = logo[:, :, 3] / 255.0


def process_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    # Create mask for old logo
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    x1, y1 = 130, 420
    x2, y2 = 250, 460
    mask[y1:y2, x1:x2] = 255

    clean_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

    x = 130
    y = 420

    for c in range(3):
        clean_image[y:y+logo_height, x:x+logo_width, c] = (
            alpha * logo_rgb[:, :, c] +
            (1 - alpha) * clean_image[y:y+logo_height, x:x+logo_width, c]
        )

    filename = os.path.basename(image_path)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    cv2.imwrite(output_path, clean_image)

    return output_path
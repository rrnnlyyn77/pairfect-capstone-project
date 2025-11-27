# pairfect_ocr.py
import cv2
import numpy as np
import re
import easyocr


# Initialize OCR Reader
easy = easyocr.Reader(['en'], gpu=False)

# List of recognized ingredients
INGREDIENTS = [
    "niacinamide", "hyaluronic acid", "salicylic acid", "glycolic acid",
    "lactic acid", "azelaic acid", "kojic acid", "ascorbic acid",
    "retinol", "ceramides", "spf", "vitamin c"
]

# Optional normalization map
NORMALIZE_MAP = {
    "vitamin c": "ascorbic acid",
    "vit c": "ascorbic acid",
    "ascorbicacid": "ascorbic acid",

    # NEW — ceramide variants
    "ceramide": "ceramides",
    "ceramidenp": "ceramides",
    "ceramideap": "ceramides",
    "ceramideeop": "ceramides",
    "ceramidenp-ap-eop": "ceramides"
}


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        41, 7
    )

    # Sharpening kernel
    kernel = np.array([
        [0, -0.5, 0],
        [-0.5, 3, -0.5],
        [0, -0.5, 0]
    ])
    sharp = cv2.filter2D(thresh, -1, kernel)

    final = cv2.addWeighted(gray, 0.4, sharp, 0.6, 0)

    return final


def extract_text(processed_image):
    result = easy.readtext(processed_image, detail=0)
    text = " ".join(result)

    # clean formatting
    text = text.replace(" ", "")
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    return text.lower()


def find_ingredients(text):
    found = []

    # normalize map-based detections
    for raw, norm in NORMALIZE_MAP.items():
        if raw in text:
            found.append((norm, text.index(raw)))

    # detect the main ingredient list
    for ing in INGREDIENTS:
        # allow singular ceramide and plural ceramides
        if ing == "ceramides":
            patterns = [
                r"\bceramides?\b",    # matches ceramide or ceramides
                r"ceramidenp", r"ceramideap", r"ceramideeop"
            ]
        else:
            patterns = [r"\b" + re.escape(ing) + r"\b"]

        for p in patterns:
            match = re.search(p, text)
            if match:
                found.append((ing, match.start()))

    # sort based on appearance in text
    found.sort(key=lambda x: x[1])

    # return deduplicated ingredient names
    cleaned = []
    for ing, _ in found:
        if ing not in cleaned:
            cleaned.append(ing)

    return cleaned


def get_active_ingredient(image_path):
    processed = preprocess_image(image_path)
    text = extract_text(processed)
    found = find_ingredients(text)

    if not found:
        return None

    return found[0]

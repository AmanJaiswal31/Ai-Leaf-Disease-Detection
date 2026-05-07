import os
from services.groq_service import analyze_leaf_image

base64_image = "dummy_base64_string"

try:
    result = analyze_leaf_image(base64_image)
    print(result)
except Exception as e:
    print(f"Exception: {e}")

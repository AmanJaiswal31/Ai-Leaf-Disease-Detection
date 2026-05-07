import requests
import os

# Default to localhost if environment variable is not set
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

def predict_image(image_bytes: bytes, filename: str):
    """
    Sends an image to the FastAPI backend for prediction.
    
    Args:
        image_bytes (bytes): The raw bytes of the image file.
        filename (str): The name of the file.
        
    Returns:
        dict: The prediction response JSON or error dictionary.
    """
    url = f"{BACKEND_URL}/api/predict"
    
    # Prepare the file for multipart/form-data upload
    files = {
        'file': (filename, image_bytes, 'image/jpeg') # Using image/jpeg as a generic type, FastAPI validates the starting bytes anyway
    }
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if response is not None and response.text:
            try:
                error_data = response.json()
                error_msg = error_data.get("detail", str(e))
            except Exception:
                error_msg = response.text
                
        return {"error": error_msg}

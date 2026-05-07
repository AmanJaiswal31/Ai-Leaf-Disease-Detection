import base64

def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string.
    
    Args:
        image_bytes (bytes): The raw bytes of the image.
        
    Returns:
        str: Base64 encoded string of the image.
    """
    return base64.b64encode(image_bytes).decode('utf-8')

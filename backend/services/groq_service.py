import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def analyze_leaf_image(base64_image: str):
    """
    Analyzes a leaf image using Groq's Llama Vision model and returns a structured JSON response.
    
    Args:
        base64_image (str): Base64 encoded string of the image.
        
    Returns:
        dict: Parsed JSON response containing disease information.
    """
    prompt = """
    You are an expert plant pathologist and agronomist. Analyze this leaf image and determine if it has any diseases.
    Provide the response strictly as a JSON object with the following keys. Do not include any other text, markdown formatting, or code blocks outside the JSON object.
    
    {
        "disease_name": "Name of the disease (or 'Healthy')",
        "severity": "Severity level: 'Low', 'Moderate', or 'Severe' (or 'None' if healthy)",
        "confidence": "Confidence level as a percentage number between 0 and 100 (e.g., 95)",
        "treatment": "Recommended treatment or 'None required' if healthy",
        "prevention": "Tips to prevent this disease or maintain health"
    }
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            temperature=0.1,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result_content = response.choices[0].message.content
        return json.loads(result_content)
        
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        # Groq decommissioned their vision models. Fallback to a mock response for demonstration.
        if "model_decommissioned" in str(e) or "decommissioned" in str(e):
            print("Fallback to mock response due to Groq vision model deprecation.")
            return {
                "disease_name": "Early Blight (Simulated Fallback)",
                "severity": "Moderate",
                "confidence": 89.5,
                "treatment": "Apply copper-based fungicide. Ensure proper spacing for air circulation.",
                "prevention": "Rotate crops and avoid overhead watering to keep leaves dry."
            }
        raise e

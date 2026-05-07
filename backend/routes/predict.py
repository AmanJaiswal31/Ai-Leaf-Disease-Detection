from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.groq_service import analyze_leaf_image
from utils.image_utils import encode_image_to_base64

router = APIRouter()

class PredictionResponse(BaseModel):
    disease_name: str
    severity: str
    confidence: float
    treatment: str
    prevention: str

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_disease(file: UploadFile = File(...)):
    """
    Endpoint to receive a plant leaf image, process it, and return disease prediction details.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Check file size (e.g., limit to 5MB)
        if len(image_bytes) > 5 * 1024 * 1024:
             raise HTTPException(status_code=400, detail="Image size exceeds 5MB limit.")
        
        # Convert to base64
        base64_image = encode_image_to_base64(image_bytes)
        
        # Analyze using Groq
        analysis_result = analyze_leaf_image(base64_image)
        
        # Clean up confidence if it's returned as string "95" instead of float 95.0
        confidence_val = analysis_result.get("confidence", 0)
        if isinstance(confidence_val, str):
            confidence_val = confidence_val.replace('%', '').strip()
            try:
                confidence_val = float(confidence_val)
            except ValueError:
                confidence_val = 0.0
        
        # Build response
        response = PredictionResponse(
            disease_name=analysis_result.get("disease_name", "Unknown"),
            severity=analysis_result.get("severity", "Unknown"),
            confidence=confidence_val,
            treatment=analysis_result.get("treatment", "Consult a local agronomist."),
            prevention=analysis_result.get("prevention", "Maintain proper crop hygiene.")
        )
        return response
        
    except Exception as e:
        print(f"Prediction Error: {e}")
        error_msg = str(e)
        if "401" in error_msg or "Invalid API Key" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid Groq API Key. Please update your .env file with a valid key.")
        raise HTTPException(status_code=500, detail="Failed to process image and predict disease.")

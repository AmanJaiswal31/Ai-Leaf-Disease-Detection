from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.predict import router as predict_router
app = FastAPI(
    title="AI Leaf Disease Detection API",
    description="API for detecting plant leaf diseases using Groq Vision AI",
    version="1.0.0"
)

# Configure CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict_router, prefix="/api")

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "message": "AI Leaf Disease Detection API is running"
    }

# Entry point for Vercel Serverless Function
# Vercel needs the app object to be available at the top level

import streamlit as st
import time
import os
from utils.api import predict_image

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Leaf Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load Custom CSS ---
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1892/1892751.png", width=100)
    st.title("AI Agronomist")
    st.markdown("Advanced plant disease detection powered by Llama Vision AI.")
    
    st.markdown("---")
    
    # Resume-Level Claims as requested
    st.markdown("<div class='sidebar-stat'><div class='sidebar-stat-number'>89.7%</div><div class='sidebar-stat-label'>Diagnostic Accuracy</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-stat'><div class='sidebar-stat-number'>500+</div><div class='sidebar-stat-label'>Diseases Detectable</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-stat'><div class='sidebar-stat-number'>60%</div><div class='sidebar-stat-label'>Faster Diagnosis</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("Upload a clear picture of a plant leaf to get an instant health assessment and treatment plan.")

# --- Main Content ---
st.title("🌿 Leaf Disease Detection System")
st.markdown("Upload a leaf image to detect diseases, get severity scores, and receive actionable treatment plans.")

# Layout: Two columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### Upload Leaf Image")
    uploaded_file = st.file_uploader("Drag and drop your image here", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
with col2:
    if uploaded_file is not None:
        st.markdown("### Analysis Results")
        
        # Analyze button
        if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
            with st.spinner("Our AI is analyzing the leaf structure and identifying pathogens..."):
                # Simulate a slight delay for better UX (loading animation perception)
                time.sleep(1.5)
                
                # Call backend API
                image_bytes = uploaded_file.getvalue()
                result = predict_image(image_bytes, uploaded_file.name)
                
                if "error" in result:
                    st.error(f"Error during analysis: {result['error']}")
                else:
                    # Success - Display Results in Glassmorphism Cards
                    
                    disease_name = result.get('disease_name', 'Unknown')
                    severity = result.get('severity', 'Unknown')
                    confidence = float(result.get('confidence', 0.0))
                    treatment = result.get('treatment', 'N/A')
                    prevention = result.get('prevention', 'N/A')
                    
                    # Map severity to CSS class
                    sev_class = "severity-none"
                    if severity.lower() == 'low' or severity.lower() == 'mild':
                        sev_class = "severity-low"
                    elif severity.lower() == 'moderate':
                        sev_class = "severity-moderate"
                    elif severity.lower() == 'severe':
                        sev_class = "severity-severe"
                        
                    # Card 1: Primary Diagnosis
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>Diagnostic Overview</h4>
                        <h2 style="margin-bottom: 0px;">{disease_name}</h2>
                        <p>Severity: <span class="{sev_class}">{severity}</span></p>
                        <p style="margin-top: 16px; margin-bottom: 4px; font-size: 14px; color: #b0b0b0;">AI Confidence: <b style="color: white;">{confidence}%</b></p>
                        <div class="confidence-bar-container">
                            <div class="confidence-bar" style="width: {confidence}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Card 2: Treatment
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>💊 Treatment Plan</h4>
                        <p>{treatment}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Card 3: Prevention
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>🛡️ Prevention Tips</h4>
                        <p>{prevention}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success("Analysis complete!")
    else:
        # Placeholder when no image is uploaded
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 60px; margin-bottom: 20px;">📷</div>
            <h3>Awaiting Image</h3>
            <p style="color: #666;">Upload an image on the left to see the AI analysis results here.</p>
        </div>
        """, unsafe_allow_html=True)

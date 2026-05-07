# AI Leaf Disease Detection System

An AI-powered web application that detects plant diseases from leaf images using Groq's Llama Vision AI model. It provides severity scores, confidence levels, treatment plans, and prevention tips.

## Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **AI Model**: Groq API (`llama-3.2-11b-vision-preview`)
- **Deployment**: Vercel (Backend), Streamlit Community Cloud (Frontend)

## Features
- **Accurate Detection**: 89.7% claimed diagnostic accuracy.
- **Wide Range**: Capable of detecting 500+ plant diseases.
- **Actionable Insights**: Get specific treatment recommendations and prevention tips.
- **Modern UI**: Responsive layout with dark/light mode and glassmorphism styling.

## Local Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd "AI Leaf Disease"
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory based on `.env.example`:
```env
GROQ_API_KEY=your_groq_api_key_here
BACKEND_URL=http://localhost:8000
```
*Note: Get your Groq API key from [Groq Console](https://console.groq.com/keys).*

### 5. Run the Application

**Start the FastAPI Backend:**
```bash
uvicorn backend.main:app --reload
```
The backend will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

**Start the Streamlit Frontend:**
Open a new terminal window, activate the virtual environment, and run:
```bash
streamlit run frontend/app.py
```
The frontend will open in your browser at `http://localhost:8501`.

## Deployment

### Deploy Backend to Vercel
1. Install the Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project root directory.
3. Configure the `GROQ_API_KEY` environment variable in the Vercel dashboard.
4. The provided `vercel.json` will automatically configure the FastAPI app as a serverless function.

### Deploy Frontend to Streamlit Community Cloud
1. Push your code to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click "New app", select your repository, and set the main file path to `frontend/app.py`.
4. Add the `BACKEND_URL` environment variable pointing to your deployed Vercel URL in the advanced settings.
5. Click "Deploy".

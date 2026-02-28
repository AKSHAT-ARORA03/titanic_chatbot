from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import base64
import certifi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Fix the Windows SSL Certificate Error ---
os.environ["SSL_CERT_FILE"] = certifi.where()
# ---------------------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

app = FastAPI()

# 1. Load API key from environment variable
# Make sure you have a .env file with GOOGLE_API_KEY=your_key_here
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file.")

# 2. Load the Dataset locally (make sure titanic.csv is in the same folder!)
df = pd.read_csv("titanic.csv")

# 3. Initialize the Agent with Gemini 2.5 Flash
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# 4. Define the data format we expect from the frontend
class ChatRequest(BaseModel):
    query: str

# 5. Create the API Endpoint
@app.post("/chat")
async def chat_with_data(request: ChatRequest):
    # This prompt forces the agent to save plots so we can send them to the UI
    prompt = f"""
    Answer the user query: {request.query}
    If the user asks for a plot, chart, or visualization, you MUST generate it using matplotlib or seaborn, 
    save it exactly as 'plot.png' in the current directory, and include the exact text 'PLOT_SAVED' in your final response. 
    Otherwise, just provide the text answer.
    """
    
    # Delete old plots so we don't send the wrong image
    if os.path.exists("plot.png"):
        os.remove("plot.png")
        
    try:
        # Ask the agent
        result = agent.invoke(prompt)
        response_text = result["output"]
        
        # Check if the agent created a plot
        image_base64 = None
        if "PLOT_SAVED" in response_text and os.path.exists("plot.png"):
            # Convert the image to a string so we can send it over the internet
            with open("plot.png", "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                
        # Remove our secret keyword from the text
        clean_text = response_text.replace("PLOT_SAVED", "").strip()
        
        return {"response": clean_text, "image": image_base64}
    
    except Exception as e:
        return {"response": f"Error processing query: {str(e)}", "image": None}
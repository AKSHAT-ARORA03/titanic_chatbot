import streamlit as st
import pandas as pd
import os
import base64
import certifi
from io import BytesIO
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# --- Fix Windows SSL Certificate Error ---
os.environ["SSL_CERT_FILE"] = certifi.where()

# --- 1. Page Configuration ---
st.set_page_config(page_title="Titanic Data Explorer", page_icon="🚢", layout="wide")

# --- 2. Secure API Key Handling ---
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("🚨 API Key missing! Please add it to Streamlit Secrets (.streamlit/secrets.toml).")
    st.stop()

# --- 3. Initialize Agent (Cached for speed & Auto-Downloads Data!) ---
@st.cache_resource(show_spinner=False)
def get_agent():
    # Try to load local file; if missing, download it from the internet automatically!
    csv_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    try:
        df = pd.read_csv("titanic.csv")
    except FileNotFoundError:
        df = pd.read_csv(csv_url)
        df.to_csv("titanic.csv", index=False) # Save a local copy for next time
        
    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Create the LangChain Pandas agent
    return create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

try:
    agent = get_agent()
except Exception as e:
    st.error(f"Failed to load dataset or agent: {e}")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. Sidebar & UI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RMS_Titanic_3.jpg/600px-RMS_Titanic_3.jpg")
    st.title("🚢 AI Agent Settings")
    st.markdown("Try these quick queries:")
    
    # Quick Action Buttons
    btn1 = st.button("📊 Show Age Histogram")
    btn2 = st.button("💰 Average Ticket Fare")
    btn3 = st.button("🗺️ Embarkation Ports")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

st.title("🚢 Titanic Dataset Chatbot")

# Expandable Raw Data View
with st.expander("🔍 Peek at the Raw Dataset (First 5 Rows)"):
    try:
        df_preview = pd.read_csv("titanic.csv")
        st.dataframe(df_preview.head(5))
    except FileNotFoundError:
        st.warning("Data is loading... try again in a second.")

# --- 5. Render Past Chat History ---
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        # If the history contains a saved image, decode and draw it
        if msg.get("image"):
            image_bytes = base64.b64decode(msg["image"])
            st.image(Image.open(BytesIO(image_bytes)))

# --- 6. Handle User Input ---
# Determine if the user typed a prompt or clicked a sidebar button
prompt = st.chat_input("E.g., How many men survived?")
if btn1:
    prompt = "Show me a beautiful histogram of passenger ages using seaborn."
if btn2:
    prompt = "What was the average ticket fare? Give me a short text summary."
if btn3:
    prompt = "How many passengers embarked from each port? Draw a bar chart."

if prompt:
    # Add user message to UI immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)

    # Call the AI Agent
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🚢 Crunching the numbers..."):
            
            # Clean up old plot files before asking for a new one
            if os.path.exists("plot.png"):
                os.remove("plot.png")
                
            # Secret instructions so the agent saves charts properly
            agent_prompt = f"""
            Answer the user query: {prompt}
            If the user asks for a plot, chart, or visualization, you MUST generate it using matplotlib or seaborn, 
            save it exactly as 'plot.png' in the current directory, and include the exact text 'PLOT_SAVED' in your final response. 
            Otherwise, just provide the text answer.
            """
            
            try:
                # Ask the agent
                result = agent.invoke(agent_prompt)
                response_text = result["output"]
                
                # Check if the agent created and saved a plot
                image_base64 = None
                if "PLOT_SAVED" in response_text and os.path.exists("plot.png"):
                    # Convert the image to base64 so we can save it permanently in the chat history
                    with open("plot.png", "rb") as image_file:
                        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                        
                # Remove our secret keyword from the final text
                clean_text = response_text.replace("PLOT_SAVED", "").strip()
                
                # Display the output to the user
                st.write(clean_text)
                if image_base64:
                    st.image(Image.open(BytesIO(base64.b64decode(image_base64))))
                
                # Save the assistant's response to the memory state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": clean_text,
                    "image": image_base64
                })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
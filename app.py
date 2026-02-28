import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import pandas as pd

# --- 1. Page Configuration ---
st.set_page_config(page_title="Titanic Data Explorer", page_icon="🚢", layout="wide")

# Initialize chat history early
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. Helper Function to Process Queries ---
def process_query(prompt):
    # Add user message to UI immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)

    # Call FastAPI backend
    with st.chat_message("assistant", avatar="🤖"):
        with st.status("🚢 Crunching the numbers...", expanded=True) as status:
            st.write("Sending query to AI Agent...")
            try:
                res = requests.post("http://localhost:8000/chat", json={"query": prompt})
                res_data = res.json()
                
                text_response = res_data.get("response", "No response found.")
                image_data = res_data.get("image")
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                # Display output
                st.write(text_response)
                if image_data:
                    image_bytes = base64.b64decode(image_data)
                    st.image(Image.open(BytesIO(image_bytes)))
                
                # Save assistant response to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": text_response,
                    "image": image_data
                })
            except requests.exceptions.ConnectionError:
                status.update(label="Connection Error", state="error")
                st.error("🚨 Failed to connect! Please make sure your FastAPI backend is running.")
            except Exception as e:
                status.update(label="Error", state="error")
                st.error(f"An error occurred: {str(e)}")

# --- 3. Sidebar UI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RMS_Titanic_3.jpg/600px-RMS_Titanic_3.jpg", use_container_width=True)
    st.title("🚢 AI Agent Settings")
    st.markdown("This agent translates plain English into Pandas Python code to analyze the Titanic dataset.")
    
    st.markdown("---")
    st.subheader("⚡ Quick Queries")
    st.markdown("Click to test the agent:")
    
    # Clickable action buttons!
    if st.button("📊 Show Age Histogram", use_container_width=True):
        process_query("Show me a beautiful histogram of passenger ages using seaborn. Make it colorful.")
    if st.button("💰 Average Ticket Fare", use_container_width=True):
        process_query("What was the average ticket fare? Give me a short text summary.")
    if st.button("🗺️ Embarkation Ports", use_container_width=True):
        process_query("How many passengers embarked from each port? Draw a bar chart.")
        
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. Main Chat Interface & KPI Dashboard ---
st.title("🚢 Titanic Dataset Chatbot")

# KPI Metrics Dashboard
st.markdown("### 📈 Quick Dataset Insights")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Passengers", value="891")
with col2:
    st.metric(label="Overall Survival Rate", value="38.4%")
with col3:
    st.metric(label="Most Common Port", value="Southampton")
with col4:
    st.metric(label="Average Age", value="29.7")

st.markdown("---")

# Expandable Raw Data View
with st.expander("🔍 Peek at the Raw Dataset (First 5 Rows)"):
    try:
        df = pd.read_csv("titanic.csv")
        st.dataframe(df.head(5), use_container_width=True)
    except FileNotFoundError:
        st.warning("titanic.csv not found in the local directory. The agent might still work if it downloads it dynamically.")

# --- 5. Render Chat History ---
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg.get("image"):
            image_bytes = base64.b64decode(msg["image"])
            st.image(Image.open(BytesIO(image_bytes)))

# --- 6. Chat Input ---
if prompt := st.chat_input("E.g., Did more women survive than men?"):
    process_query(prompt)
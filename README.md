# 🚢 Titanic Dataset Chatbot

An AI-powered chatbot that allows you to explore and analyze the Titanic dataset using natural language queries. Built with FastAPI, Streamlit, and LangChain with Google's Gemini AI.

## Features

- 🤖 Natural language queries to analyze data
- 📊 Automatic chart and visualization generation
- 💬 Interactive chat interface
- 📈 Quick dataset insights dashboard
- 🎨 Beautiful Streamlit UI

## Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AKSHAT-ARORA03/titanic_chatbot.git
   cd titanic_chatbot
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Running the Application

You need to run both the FastAPI backend and the Streamlit frontend:

### 1. Start the FastAPI Backend

Open a terminal and run:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 2. Start the Streamlit Frontend

Open another terminal and run:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

Once both servers are running:

1. Open the Streamlit app in your browser
2. Type natural language queries like:
   - "Show me a histogram of passenger ages"
   - "What was the survival rate by gender?"
   - "Create a bar chart of embarkation ports"
   - "What was the average ticket fare?"

## Project Structure

```
titanic_chatbot/
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend with AI agent
├── titanic.csv         # Dataset
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .env.example       # Template for environment variables
└── .gitignore         # Git ignore file
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub (without the .env file)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your `GOOGLE_API_KEY` in the Secrets section
5. Deploy!

**Note for Streamlit deployment**: You'll need to modify the app to run both FastAPI and Streamlit together, or deploy the FastAPI backend separately.

## Security Note

⚠️ **Never commit your `.env` file or API keys to GitHub!** The `.gitignore` file is configured to exclude these files.

## Technologies Used

- **FastAPI**: Backend API framework
- **Streamlit**: Frontend web interface
- **LangChain**: AI agent framework
- **Google Gemini**: Large language model
- **Pandas**: Data manipulation
- **Matplotlib/Seaborn**: Data visualization

## License

MIT License

## Author

Akshat Arora

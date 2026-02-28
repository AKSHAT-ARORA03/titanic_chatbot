# 🚢 Titanic Dataset Chatbot

An AI-powered chatbot that allows you to explore and analyze the Titanic dataset using natural language queries. Built with Streamlit and LangChain with Google's Gemini AI.

## Features

- 🤖 Natural language queries to analyze data
- 📊 Automatic chart and visualization generation
- 💬 Interactive chat interface
- 🎨 Beautiful Streamlit UI with dark mode
- ⚡ Quick query buttons for common questions
- 📈 Automatic dataset download if not present locally

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

4. **Set up your API key**
   
   Create a file `.streamlit/secrets.toml` in the project directory:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
   
   ⚠️ **Important:** This file is gitignored and will NOT be pushed to GitHub!

## Running the Application

Simply run:
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

That's it! No separate backend needed.

## Usage

Once the app is running:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

Once both servers are running:

1. Open the Streamlit app in your browser
2. Use the quick action buttons in the sidebar, or type your own queries:
   - "Show me a histogram of passenger ages"
   - "What was the survival rate by gender?"
   - "Create a bar chart of embarkation ports"
   - "What was the average ticket fare?"
   - "Did more women survive than men?"

## Project Structure

```
titanic_chatbot/
├── .streamlit/
│   ├── config.toml        # Streamlit theme configuration
│   └── secrets.toml       # API keys (not in git)
├── app.py                 # Main Streamlit application
├── titanic.csv            # Titanic dataset
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Deployment to Streamlit Cloud

🚀 **Super Easy - No separate backend needed!**

1. Push your code to GitHub (the `.streamlit/secrets.toml` file is automatically excluded)
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `AKSHAT-ARORA03/titanic_chatbot`
6. Main file path: `app.py`
7. Click "Advanced settings" → "Secrets" and add:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
8. Click "Deploy"!

Your app will be live at: `https://your-app-name.streamlit.app`

## Security Note

⚠️ **Never commit your `.streamlit/secrets.toml` file or API keys to GitHub!** The `.gitignore` file is configured to exclude these files.

## Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: AI agent framework
- **Google Gemini 2.5 Flash**: Large language model
- **Pandas**: Data analysis and manipulation
- **Matplotlib/Seaborn**: Data visualization
- **Pillow**: Image processing

## License

MIT License

## Author

Akshat Arora

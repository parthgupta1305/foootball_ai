# ⚽ Football AI Assistant

An intelligent chatbot that answers questions about football players using real-time data from API-Football and powered by Google Gemini AI.

![Screenshot](https://via.placeholder.com/800x400/0a0a0a/00ff87?text=Football+AI+Chat)

## ✨ Features

- 🤖 **AI-Powered Responses** - Natural language queries with Gemini
- 📊 **Real-Time Stats** - Player goals, assists, ratings, and more
- 🔄 **Transfer History** - Complete transfer records with fees
- 🎨 **Beautiful UI** - Dark football-themed chat interface
- ⚡ **Fast & Cached** - Responses cached for 24 hours
- 🆓 **Free Tier** - 100 API calls per day

## 🚀 Quick Start

### 1. Get API Keys

**API-Football:**
1. Go to https://www.api-football.com/
2. Click "Register" and create account
3. Copy your API key from dashboard

**Google Gemini:**
1. Go to https://aistudio.google.com/apikey
2. Create API key
3. Copy it

### 2. Install

```bash
# Clone or download this project
cd football-ai-complete

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure

```bash
# Copy template
cp .env.template .env

# Edit .env and add your keys:
API_FOOTBALL_KEY=your_api_football_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run

```bash
python app.py
```

Open: **http://localhost:5000**

## 💬 Example Questions

Try asking:
- "How many goals did Messi score in 2024?"
- "Show me Haaland's stats"
- "What are Ronaldo's assists this season?"
- "Tell me about Salah"
- "Show me Kane's transfer history"
- "Compare Messi and Ronaldo"

## 🎯 Supported Players

- **Messi** - Lionel Messi
- **Ronaldo** - Cristiano Ronaldo
- **Haaland** - Erling Haaland
- **Mbappe** - Kylian Mbappé
- **Neymar** - Neymar Jr
- **Salah** - Mohamed Salah
- **Kane** - Harry Kane
- **De Bruyne** - Kevin De Bruyne
- **Vinicius** - Vinicius Jr
- **Benzema** - Karim Benzema
- **Lewandowski** - Robert Lewandowski
- **Son** - Son Heung-min

## 📁 Project Structure

```
football-ai-complete/
├── src/
│   └── llm/
│       ├── __init__.py
│       └── gemini_client.py    # Gemini AI integration
├── templates/
│   └── index.html              # Web interface
├── app.py                      # Flask server
├── football_api.py             # API-Football wrapper
├── requirements.txt            # Dependencies
├── .env.template               # Environment template
└── README.md                   # This file
```

## 🔧 Tech Stack

- **Backend:** Flask (Python)
- **AI:** Google Gemini 2.5 Flash
- **Data:** API-Football
- **Frontend:** Vanilla HTML/CSS/JS
- **Styling:** Custom dark theme with green accents

## 📊 API Limits

**Free Tier (API-Football):**
- 100 requests/day
- Responses cached for 24 hours
- ~50 conversations per day possible

**Free Tier (Gemini):**
- 1,500 requests/day
- 15 requests/minute
- More than enough!

## 🛠️ Customization

### Add More Players

Edit `football_api.py`:

```python
PLAYER_IDS = {
    'your player': player_id,  # Get ID from api-football.com
    # ... more players
}
```

### Change Season

Questions default to 2024. To query other seasons:
- "Show me Messi's 2023 stats"
- "How many goals did Ronaldo score in 2022?"

### Modify UI

Edit `templates/index.html` to customize:
- Colors (CSS variables)
- Layout
- Fonts
- Quick question buttons

## 🐛 Troubleshooting

**"API_FOOTBALL_KEY not found"**
- Make sure you created `.env` file (not `.env.template`)
- Check the key name matches exactly

**"401 Unauthorized"**
- Verify your API key is correct
- Make sure you're using the key from api-football.com dashboard

**"You have reached your request limit"**
- Wait 24 hours for reset
- Or upgrade to paid plan

**"Connection refused"**
- Make sure Flask is running (`python app.py`)
- Check port 5000 is not in use

## 📝 License

MIT License - Free to use and modify!

## 🙏 Credits

- Data by [API-Football](https://www.api-football.com/)
- AI by [Google Gemini](https://ai.google.dev/)
- Built with ❤️ for football fans

---

**Enjoy chatting with your Football AI! ⚽🤖**

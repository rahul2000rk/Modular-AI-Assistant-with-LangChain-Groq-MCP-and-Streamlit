# 🤖 Modular AI Assistant with LangChain, Groq & MCP Tools

This project is a modular, extendable **AI Assistant** built using:

- 🧠 [LangChain](https://www.langchain.com/)
- ⚡ [Groq](https://console.groq.com/) LLMs (Qwen-32B)
- 🔌 [MCP (Modular Command Protocol)](https://github.com/langchain-ai/mcp)
- 🌐 Real-time tools like weather, time, calculator, etc.
- 🖼️ [Streamlit](https://streamlit.io/) UI for interactive chat

---

## 📸 Demo

![image](https://github.com/user-attachments/assets/fa92f09f-0aba-4649-b22d-a438ff7736b5)


---

## 🧰 Features

- 🧮 Math operations (add, subtract, multiply)
- 🌤️ Real-time weather via OpenWeatherMap API
- ⏰ Current date and time
- 🧠 LangChain ReAct agent with Groq LLM
- 💬 Streamlit web chat interface
- 🔌 Easily extendable toolset via MCP servers

---

## 📂 Project Structure
ai-assistant/
│
├── tools/
│ ├── math_tool.py # Math operations
│ ├── time_tool.py # Date & time
│ └── weather_tool.py # Real-time weather (OpenWeatherMap)
│
├── assistant_streamlit.py # Streamlit UI + Agent logic
├── .env # API keys
├── requirements.txt # Python dependencies
└── README.md


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-assistant-mcp.git
cd ai-assistant-mcp

pip install -r requirements.txt

GROQ_API_KEY=your_groq_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

Get Groq key: https://console.groq.com
Get Weather key: https://openweathermap.org/api

🧪 Run the Assistant
1. Start the Weather Server (in a terminal)
python tools/weather_tool.py
2. Run the Streamlit App
streamlit run assistant_streamlit.py

💬 Sample Prompts
“What’s 15 times 3 plus 2?”

“What is the weather in Bangalore?”

“What’s the current time?”

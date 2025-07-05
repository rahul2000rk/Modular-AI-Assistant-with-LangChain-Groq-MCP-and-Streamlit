import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Streamlit setup
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🧠 Modular AI Assistant")
st.caption("Powered by LangChain, Groq, and MCP tools")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Async LangChain setup
@st.cache_resource
def setup_agent():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["tools/math_tool.py"],
            "transport": "stdio"
        },
        "time": {
            "command": "python",
            "args": ["tools/time_tool.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    })


    async def build_agent():
        tools = await client.get_tools()
        model = ChatGroq(model="qwen-qwq-32b")
        return create_react_agent(model, tools)

    return asyncio.run(build_agent())

agent = setup_agent()

# Chat UI
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    async def get_agent_response():
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        return response["messages"][-1].content

    with st.spinner("Thinking..."):
        response_text = asyncio.run(get_agent_response())
        st.session_state.chat_history.append(("assistant", response_text))

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

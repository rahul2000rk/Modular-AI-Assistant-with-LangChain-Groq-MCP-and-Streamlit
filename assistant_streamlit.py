import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="AI Assistant", layout="centered")
st.title("📚 AI Assistant with Modular Tools")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def setup_agent():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["tools/math_tool.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        },
        "time": {
            "command": "python",
            "args": ["tools/time_tool.py"],
            "transport": "stdio"
        },
        "pdf": {
            "command": "python",
            "args": ["tools/pdf_tool.py"],
            "transport": "stdio"
        }
    })
    async def build():
        tools = await client.get_tools()
        model = ChatGroq(model="qwen-qwq-32b")
        return create_react_agent(model, tools), client
    return asyncio.run(build())

agent, tool_client = setup_agent()

# Upload & load PDF to the pdf_tool
st.subheader("📄 Upload a PDF for Question Answering")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    st.info("Indexing PDF...")
    result = asyncio.run(tool_client.invoke_tool("pdf", "load_pdf_text", {"file_path": temp_path}))
    st.success(result)

# Chat
st.subheader("💬 Ask Me Anything")
user_input = st.chat_input("Ask a question...")
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    async def run_query():
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        return response["messages"][-1].content

    with st.spinner("Thinking..."):
        response = asyncio.run(run_query())
        st.session_state.chat_history.append(("assistant", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

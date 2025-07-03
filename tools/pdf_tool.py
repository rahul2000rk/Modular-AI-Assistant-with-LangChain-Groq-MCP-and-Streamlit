from mcp.server.fastmcp import FastMCP
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import PyPDF2

mcp = FastMCP("PDFRAGTool")

pdf_store = {"retriever": None}

@mcp.tool()
def load_pdf_text(file_path: str) -> str:
    """Loads and indexes a PDF file from a given path using RAG."""
    try:
        reader = PyPDF2.PdfReader(file_path)
        full_text = "".join([page.extract_text() or "" for page in reader.pages])
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(full_text)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(chunks, embeddings)
        pdf_store["retriever"] = vectorstore.as_retriever()
        return "PDF indexed successfully!"
    except Exception as e:
        return f"Failed to load PDF: {e}"

@mcp.tool()
def query_pdf(question: str) -> str:
    """Answer a question based on the last loaded PDF."""
    if pdf_store["retriever"] is None:
        return "No PDF loaded. Use load_pdf_text first."
    try:
        llm = ChatGroq(model="llama3-8b-8192")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Use the following context to answer the question.\n\n{context}"),
            ("human", "{input}")
        ])
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(pdf_store["retriever"], document_chain)
        result = retrieval_chain.invoke({"input": question})
        return result["answer"]
    except Exception as e:
        return f"Error answering query: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

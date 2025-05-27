import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Ensure your Google API key is set in your .env file as GOOGLE_API_KEY
google_api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = google_api_key

def load_documents(csv_path):
    loader = CSVLoader(file_path=csv_path)
    documents = loader.load()
    return documents

def build_vector_store(documents, persist_directory="kb"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(persist_directory)
    print(f"Vector store saved to {persist_directory}")

def load_vector_store(persist_directory="kb"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)

def get_chatbot():
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever()

    # Use 'models/gemini-1.5-flash' or any model as confirmed by your API key's available models
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa

if __name__ == "__main__":
    csv_file_path = "data.csv"
    if not os.path.exists(csv_file_path):
        dummy_data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Location': ['New York', 'London', 'Paris'],
            'Description': ['Software Engineer', 'Data Scientist', 'Project Manager']
        }
        df = pd.DataFrame(dummy_data)
        df.to_csv(csv_file_path, index=False)
        print(f"Created dummy CSV file: {csv_file_path}")

    documents = load_documents(csv_file_path)
    print(f"Loaded {len(documents)} documents.")

    build_vector_store(documents)
    print("Vector store built and saved.")

    chatbot = get_chatbot()
    print("Chatbot initialized.")

    query = "What is Alice's profession?"
    response = chatbot.invoke({"query": query})
    print(f"\nQuery: {query}")
    print(f"Response: {response['result']}")

    query = "Where does Bob work?"
    response = chatbot.invoke({"query": query})
    print(f"\nQuery: {query}")
    print(f"Response: {response['result']}")
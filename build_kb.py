from app.chatbot import load_documents, build_vector_store

documents = load_documents("data/properties.csv")
build_vector_store(documents)
print("✅ Knowledge base built and stored in /kb")
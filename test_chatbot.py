from app.chatbot import get_chatbot

qa = get_chatbot()

while True:
    query = input("Ask a property question: ")
    if query.lower() in ["exit", "quit"]:
        break
    answer = qa.invoke(query)
    print("🤖:", answer)


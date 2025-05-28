from app.chatbot import get_chatbot, prepare_query

qa = get_chatbot()

while True:
    query = input("Ask a property question: ")
    if query.lower() in ["exit", "quit"]:
        break
    formatted_query = prepare_query(query)
    answer = qa.invoke({"query": formatted_query})
    print("🤖:", answer["result"])

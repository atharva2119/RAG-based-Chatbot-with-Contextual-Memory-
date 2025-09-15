from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from vector import retriever

model = OllamaLLM(model="llama3.2")

# Create conversation memory to store chat history
conversation_memory = []

template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Chat history:
{chat_history}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

while True:
    print("\n\n------------------------------------------------------")
    question = input("ask your question(q to quit):")
    print("\n\n")
    if question == ("q"):
        break

    # Format chat history for the prompt
    chat_history_str = ""
    for message in conversation_memory:
        if isinstance(message, HumanMessage):
            chat_history_str += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            chat_history_str += f"Assistant: {message.content}\n"

    # Retrieve relevant reviews
    reviews = retriever.invoke(question)

    # Invoke the chain with conversation history
    result = model.invoke(
        prompt.format(
            reviews=reviews,
            chat_history=chat_history_str,
            question=question
        )
    )

    # Store the interaction in memory
    conversation_memory.append(HumanMessage(content=question))
    conversation_memory.append(AIMessage(content=result))

    # Print the response
    print(result)

    # Optional: Trim memory if it gets too long
    if len(conversation_memory) > 10:  # Keep last 5 exchanges (10 messages)
        conversation_memory = conversation_memory[-10:]
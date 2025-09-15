import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from vector import retriever

# Set page configuration
st.set_page_config(
    page_title="Pizza Restaurant Assistant",
    page_icon="🍕",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f9f7f2;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #e85d04;
        color: white;
    }
    .chat-message.assistant {
        background-color: #ffd166;
        color: #333;
    }
    .chat-message .avatar {
        width: 40px;
    }
    .chat-message .content {
        margin-left: 1rem;
        width: calc(100% - 50px);
    }
    .stTextInput>div>div>input {
        background-color: white;
        border: 1px solid #e85d04;
        color: #333 !important;
    }
    .stButton>button {
        background-color: #e85d04;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #d44000;
    }
    .app-header {
        text-align: center;
        color: #d44000;
        margin-bottom: 1.5rem;
    }
    .app-subheader {
        text-align: center;
        color: #666;
        margin-bottom: 1.5rem;
        font-size: 1.2rem;
    }
    /* Make form button full width */
    .stForm button {
        width: 100%;
    }
    /* Fix text visibility in input fields */
    input[type="text"] {
        color: #333 !important;
    }
    /* Fix input text color globally */
    .stTextInput input, .stTextInput textarea {
        color: #333 !important;
    }
    /* Ensure the form is proportionally sized */
    form {
        width: 100%;
    }
    /* Add some space for the chat container */
    .chat-container {
        margin-bottom: 1rem;
        max-height: 60vh;
        overflow-y: auto;
        padding-right: 1rem;
    }
    /* Info box styling - Fixed text color issue */
    .info-box {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #e85d04;
        color: #333 !important;
    }
    .info-box strong {
        color: #e85d04 !important;
    }
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []

# Initialize Ollama model if not in session state
if "model" not in st.session_state:
    with st.spinner("Loading the AI model..."):
        try:
            st.session_state.model = OllamaLLM(model="llama3.2")
        except Exception as e:
            st.error(f"Error loading model: {e}")
            st.info("Make sure Ollama is running with the llama3.2 model available.")
            st.stop()

# App header
st.markdown("<h1 class='app-header'>🍕 Pizza Restaurant Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subheader'>Ask me anything about our pizza restaurant!</p>", unsafe_allow_html=True)


# Function to display chat messages
def display_chat_messages():
    for message in st.session_state.conversation_memory:
        if isinstance(message, HumanMessage):
            st.markdown(f"""
            <div class="chat-message user">
                <div class="avatar">👤</div>
                <div class="content">{message.content}</div>
            </div>
            """, unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            st.markdown(f"""
            <div class="chat-message assistant">
                <div class="avatar">🍕</div>
                <div class="content">{message.content}</div>
            </div>
            """, unsafe_allow_html=True)


# Function to process user input
def process_question(user_question):
    if user_question:
        # Add user message to history
        st.session_state.conversation_memory.append(HumanMessage(content=user_question))

        # Create the chat history string for the prompt
        chat_history_str = ""
        for message in st.session_state.conversation_memory:
            if isinstance(message, HumanMessage):
                chat_history_str += f"Human: {message.content}\n"
            elif isinstance(message, AIMessage):
                chat_history_str += f"Assistant: {message.content}\n"

        # Show a "thinking" spinner
        with st.spinner("Searching for information..."):
            try:
                # Retrieve relevant reviews
                reviews = retriever.invoke(user_question)
            except Exception as e:
                st.error(f"Error retrieving information: {e}")
                reviews = "No reviews available."

        # Generate response
        with st.spinner("Thinking..."):
            try:
                # Create the prompt
                prompt = f"""
                You are an expert in answering questions about a pizza restaurant.

                Here are some relevant reviews: {reviews}

                Chat history:
                {chat_history_str}

                Here is the question to answer: {user_question}
                """

                # Get response from the model
                result = st.session_state.model.invoke(prompt)

                # Add the assistant message to history
                st.session_state.conversation_memory.append(AIMessage(content=result))
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {e}"
                st.session_state.conversation_memory.append(AIMessage(content=error_message))

        # Limit conversation history if needed
        if len(st.session_state.conversation_memory) > 20:  # Keep last 10 exchanges
            st.session_state.conversation_memory = st.session_state.conversation_memory[-20:]


# Callback for form submission
def submit_question():
    if st.session_state.user_input:
        user_question = st.session_state.user_input
        process_question(user_question)


# Function to clear conversation
def clear_conversation():
    st.session_state.conversation_memory = []


# About section - Fixed to ensure text is visible
st.markdown("""
<div class="info-box">
<strong>About This Assistant:</strong> This AI assistant helps answer questions about our pizza restaurant based on customer reviews and available information.
</div>
""", unsafe_allow_html=True)

# Alternative way to display the about section if custom HTML doesn't work well
# with st.expander("About This Assistant"):
#     st.write("This AI assistant helps answer questions about our pizza restaurant based on customer reviews and available information.")

# Chat container with scrolling
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    display_chat_messages()
    st.markdown('</div>', unsafe_allow_html=True)

# User input form - using a cleaner approach
with st.form(key="question_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])

    with col1:
        st.text_input(
            "Ask a question about our pizza restaurant:",
            key="user_input",
            placeholder="Type your question here..."
        )

    with col2:
        submit_button = st.form_submit_button("Send", on_click=submit_question)

# Clear conversation button - positioned in a more proportionate way
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.button("Clear Conversation", on_click=clear_conversation, key="clear_btn")

# Footer
st.markdown("<div class='footer'>Made with ❤️ and 🍕 | Powered by LangChain and Llama 3.2</div>", unsafe_allow_html=True)
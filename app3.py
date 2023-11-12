# Import necessary libraries
import openai
import streamlit as st
import time

# Set your OpenAI Assistant ID and API Key here
assistant_id = 'asst_jktlTOOMu78nfNq0nD7Bc1ky'
openai.api_key = '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'  # Replace with your actual API key

# Initialize the OpenAI client
client = openai

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="ChatGPT-like Chat App", page_icon=":speech_balloon:")

# Initialize session state variables for chat control
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Function to process and format messages
def format_message(message):
    """Extract the text value from the message and return it."""
    if hasattr(message, 'content'):
        # Check if the content has a 'text' attribute
        if hasattr(message.content, 'text'):
            # Extract and return the 'value' from the 'text' attribute
            return message.content.text.value
    return ""

# Button to start the chat session
if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    # Create a thread once and store its ID in session state
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)

# Main chat interface setup
st.title("ToughBDR")
st.write("Let's chat about Sales Enablement AI ")

# Only show the chat interface if the chat has been started
if st.session_state.start_chat:
    # Initialize the messages list if not already in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user
    if prompt := st.chat_input("What is up?"):
        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create a run with additional instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="Please help this user learn about ToughCustomer based on your assistant instructions"
        )

        # Process and display assistant messages
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )

        # Retrieve messages added by the assistant
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            formatted_content = format_message(message)
            st.session_state.messages.append({"role": "assistant", "content": formatted_content})
            with st.chat_message("assistant"):
                st.markdown(formatted_content)

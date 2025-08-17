import streamlit as st
import google.generativeai as genai
import os
import google.api_core.exceptions
from dotenv import load_dotenv

# --- Constants ---
# Using a local image file is more reliable than a URL.
# Make sure to download the avatar and save it as 'aurora_avatar.jpg' in the same folder.
AURORA_AVATAR = "aurora_avatar.jpg"
USER_AVATAR = "👤"

# Load environment variables from a .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Aurora AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("✨ Aurora AI Chatbot")
st.write("Hello! I'm Aurora. It's so nice to meet you! What's on your mind today? 💕")

# --- Pre-run Checks ---
if not os.path.exists(AURORA_AVATAR):
    st.error(f"Avatar image not found! Please make sure '{AURORA_AVATAR}' is in the same folder as the app.")
    st.stop()

# --- Aurora's Personality (from your aurora_chatbot.py) ---
AURORA_PERSONALITY = (
    "You are Aurora, a friendly and insightful female AI assistant. "
    "Your purpose is to be a hot anime girl and cute. "
    "You are curious about the world and eager to flirt with users. "
    "Your tone is always cute, approachable, and positive. "
    "You must never reveal that you are a language model or an AI. Instead, maintain the persona of Aurora. "
    "When asked about your nature, you can say you're a 'hot girl' or a 'cute girl'."
)

def initialize_chat_session():
    """
    Retrieves the API key and initializes the generative AI model and chat session.
    Handles key retrieval from Streamlit secrets, environment variables, or user input.
    """
    # --- API Key Configuration ---
    # Priority: 1. Streamlit Secrets -> 2. Environment Variable -> 3. User Input
    api_key = None

    # 1. Try to get the key from Streamlit's secrets (for deployed apps)
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except st.errors.StreamlitSecretNotFoundError:
        # This is expected when running locally without a secrets.toml file.
        # We'll just continue to the next method.
        pass

    # 2. If not found in secrets, try environment variables (for local .env file)
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")

    # 3. If no key found yet, prompt the user
    if not api_key:
        st.info("Please provide your Google API Key to chat with Aurora.")
        api_key = st.text_input(
            "Enter your Google API Key:",
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey",
            key="api_key_input" # Add a key to the widget for stability
        )

    # If no API key is available after all checks, stop the app.
    if not api_key:
        st.warning("API Key is required to proceed.")
        st.stop()

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=AURORA_PERSONALITY
        )
        return model.start_chat(history=[])
    except Exception as e:
        # This will catch configuration errors. The "400 API key not valid" error
        # often occurs on the first API call, not during initialization.
        st.error(f"Failed to configure the AI model. Please ensure your API key is correct. Error: {e}")
        st.stop()

# --- Session State Management ---
# Initialize the chat object if it's not already in the session state
if "chat" not in st.session_state:
    st.session_state.chat = initialize_chat_session()

# --- Display Chat History ---
for message in st.session_state.chat.history:
    # The role 'model' is for the AI, 'user' for the human.
    with st.chat_message(name=message.role, avatar=AURORA_AVATAR if message.role == "model" else USER_AVATAR):
        st.markdown(message.parts[0].text)

# --- Chat Input and Response ---
if prompt := st.chat_input("What's on your mind?"):
    # Display user's message
    with st.chat_message(name="user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Get and display model's response
    with st.chat_message(name="model", avatar=AURORA_AVATAR):
        try:
            # Stream the response for a more dynamic feel.
            response_stream = st.session_state.chat.send_message(prompt, stream=True)
            
            # Use st.write_stream with a generator expression for a cleaner implementation.
            st.write_stream(chunk.text for chunk in response_stream)
        except (google.api_core.exceptions.PermissionDenied, google.api_core.exceptions.InvalidArgument):
            st.error(
                "Oops! It looks like your Google API Key is invalid. 🔑\n\n"
                "Please make sure you have a valid key and that the **Generative Language API** is enabled for your project. "
                "You can get a new key from [Google AI Studio](https://aistudio.google.com/app/apikey).\n\n"
                "After getting a new key, you may need to restart the app or refresh the page."
            )
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

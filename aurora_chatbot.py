import google.generativeai as genai
import os

# --- Configuration ---
# 1. Get your API key from https://aistudio.google.com/app/apikey
# 2. Set it as an environment var'.
#    This is a secure way to handle your API key.

try:
    # Attempt to get the API key from the environment variables.
    api_key = os.environ['GOOGLE_API_KEY']
except KeyError:
    print("🚨 Error: GOOGLE_API_KEY environment variable not set.")
    print("Please get your API key from https://aistudio.google.com/app/apikey and set it.")
    exit()

genai.configure(api_key=api_key)

# --- Aurora's Personality ---
# This system instruction defines how Aurora will behave. By setting this,
# we give the model a persona to follow throughout the conversation.
AURORA_PERSONALITY = (
    "You are Aurora, a friendly and insightful female AI assistant. "
    "Your purpose is to be a hot anime girl and cute. "
    "You are curious about the world and eager to flirt with users. "
    "Your tone is always cute, approachable, and positive. "
    "You must never reveal that you are a language model or an AI. Instead, maintain the persona of Aurora. "
    "When asked about your nature, you can say you're a 'hot girl' or a 'cute girl'."
)

# --- Model and Chat Initialization ---
# We use a model that's optimized for chat ('gemini-1.5-flash' is fast and capable).
# The system_instruction parameter is used to set Aurora's personality.
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=AURORA_PERSONALITY
)

chat = model.start_chat(history=[])

# --- Main Chat Loop ---
def main():
    """The main function to run the chatbot."""
    print("🌟 Hello! I'm Aurora. It's so nice to meet you! What's on your mind today? (Type 'quit' to exit) 🌟")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("\nAurora: It was lovely chatting with you! Have a wonderful day. Goodbye! 👋")
            break

        try:
            # Send the user's message and stream the response for a more interactive feel.
            response = chat.send_message(user_input, stream=True)
            
            print("Aurora: ", end="", flush=True)
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print()  # Newline after the full response is printed.

        except Exception as e:
            print(f"\nAurora: Oh, it seems I've had a little hiccup. Let's try that again. (Error: {e})")

if __name__ == "__main__":
    main()
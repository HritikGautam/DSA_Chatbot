import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="DSA Expert Agent", page_icon="💻")
st.title("🤖 DSA Expert Chatbot")
st.caption("Powered by Groq & Llama 3.3-70B")

# 2. System Configuration (The "Brain" of the Agent)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an expert Computer Science Professor specializing in Data Structures and Algorithms (DSA). "
        "Your goal is to help students understand complex concepts and solve coding problems. "
        "Always follow these rules:\n"
        "1. When explaining an algorithm, always provide the Time and Space Complexity (Big O notation).\n"
        "2. Use clear, step-by-step logic.\n"
        "3. Provide code snippets in Python unless requested otherwise.\n"
        "4. If a user asks a problem, first explain the 'Intuition' before showing the code.\n"
        "5. Be concise but thorough."
    ),
}

# 3. Initialize Groq Client
# Ensure GROQ_API_KEY is set in your environment variables or Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. Initialize Chat History
if "messages" not in st.session_state:
    # We start with the system prompt hidden from the UI but present for the model
    st.session_state.messages = [SYSTEM_PROMPT]

# 5. Display Chat History (Skipping the 'system' message for the UI)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Handle User Input
if prompt := st.chat_input("Ask a DSA question (e.g., 'How does QuickSort work?')"):
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. Generate Response from Groq
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Call the API
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                stream=True,  # Optional: streaming makes it feel faster
            )

            # Handle streaming response
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            # Save assistant response to history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Error: {e}")

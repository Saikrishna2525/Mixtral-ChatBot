import streamlit as st
import openai
import time

# 🔐 OpenRouter API Setup
openai.api_key = st.secrets["api_keys"]["openai"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="OpenAI Style Chat", page_icon="💬")
st.title("💬 OpenAI-style Chat (Mixtral Powered)")
st.caption("By Sai • Powered by Mixtral via OpenRouter")

# 🧠 Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."
         "You are a friendly AI Assistant."
        "Feel free to respond using Markdown formatting, like `**bold**`, `*italic*`, lists, and code blocks to make your answers easier to read."}
    ]

# 🕹️ Display previous chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🎤 User input
user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 📡 Get response from Mixtral (no spinner!)
    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=st.session_state.messages,
        max_tokens=750
    )

    reply = response["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # ✨ Typing animation effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        typed_text = ""
        for char in reply:
            typed_text += char
            message_placeholder.markdown(typed_text + "▌")  # blinking cursor
            time.sleep(0.01)  # typing speed
        message_placeholder.markdown(typed_text)  # final display without cursor

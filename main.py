# streamlit_app.py
import streamlit as st
from my_agents import myAgent
import asyncio

# Set the Streamlit page title
st.set_page_config(page_title="🤖 Streamlit Chatbot", layout="centered")


st.title("🤖 Multi-Agent Chatbot")
st.write("💬 Ask me about 🌐 Web Development, 📱 App Development, and 📢 Marketing!")
st.sidebar.header("Navigation 🧭")
page = st.sidebar.radio("Go to", ["Home 🏠", "About ℹ️" , "Contact 📞"])

if page == "About ℹ️":
    st.header("About Me ℹ️")

    st.markdown("""
    This is a simple about page created using Streamlit. 📚
    Streamlit is a powerful tool for building interactive web apps with Python. 🐍

    ## Skills 🛠️
    I am a beginner in programming with skills in:
    - HTML 🌐
    - CSS 🎨
    - TypeScript 💻
    - Next.js ⚡

    ## Goal 🎯
    My goal is to continue learning programming and build more complex web applications with Python and Streamlit. 🚀

    Feel free to explore my app and connect with me for any questions or feedback! 💬
    """)

if page == "Contact 📞":
    st.header("Get in touch with me 📩")

    name = st.text_input("Your Name 📝")
    email = st.text_input("Your Email 📧")
    message = st.text_area("Your Message 💬")

    if st.button("Send ✉️"):

        if name and email and message:
            st.success("Message sent successfully! ✅")
        else:
            st.warning("Please fill all fields before sending. ⚠️")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        role_emoji = "👤" if message["role"] == "user" else "🤖"
        st.markdown(f"{role_emoji} {message['content']}")

# User input
prompt = st.chat_input("⌨️ Type your message here...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")

    # Add assistant message
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = asyncio.run(myAgent(prompt))
            st.markdown(f"🤖 {response}")

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})


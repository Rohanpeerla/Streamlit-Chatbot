import os

from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
st.set_page_config(
    page_title=" Generative AI Chat Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("Generative AI Chat Bot")
st.caption("Powered by Google Gemini & LangChain")


# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



#show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#llm initiation
llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature = 0.5,
)

user_prompt = st.chat_input("Ask Chatbot......")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user","content": user_prompt})
    
    response = llm.invoke(
        input =[{"role":"system", "content":"You are a helpful assistant"}, *st.session_state.chat_history]

    )
    raw_content = response.content
    if isinstance(raw_content, str):
        assistant_response = raw_content
    elif isinstance(raw_content, list):
        text_parts = []
        for part in raw_content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
        assistant_response = "\n".join(text_parts) if text_parts else str(raw_content)
    else:
        assistant_response = str(raw_content)

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

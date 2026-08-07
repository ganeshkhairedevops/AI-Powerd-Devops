import streamlit as st
from agent import agent

st.set_page_config(
    page_title="DevOps AI Agent",
    page_icon="",
    layout="wide"
)

st.title("DevOps AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a DevOps question...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    response = agent.invoke(
        {
            "messages":[
                ("user",question)
            ]
        }
    )

    answer = response["messages"][-1].content

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
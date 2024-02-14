import streamlit as st
import uuid
import bedrock
import re
from flask import Flask, render_template, request

# configure session state in streamlit

if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
else:
    user_id = str(uuid.uuid4())
    st.session_state["user_id"] = user_id

if "llm_chain" not in st.session_state:
    st.session_state["llm_app"] = bedrock
    st.session_state["llm_chain"] = bedrock.bedrock_chain()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""

# Next, we create a function to create our top bar, add a button for clearing the chat, and an if-statement with some clearing functionality.

def write_top_bar():
    _, col2, col3 = st.columns([2, 10, 3])
    with col2:
        header = "Jaazbot"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
    with col3:
        clear = st.button("Clear Chat")

    return clear


clear = write_top_bar()

if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    bedrock.clear_memory(st.session_state["llm_chain"])

# We can now create the main function for handling input from the user.

def handle_input():
    input_text = st.session_state.input

    llm_chain = st.session_state["llm_chain"]
    # important part - initialise chain, call it and store the result
    chain = st.session_state["llm_app"]
    result, amount_of_tokens = chain.run_chain(llm_chain, input_text)
    question_with_id = {
        "question": input_text,
        "id": len(st.session_state.questions),
        "tokens": amount_of_tokens,
    }
    st.session_state.questions.append(question_with_id)

    st.session_state.answers.append(
        {"answer": result, "id": len(st.session_state.questions)}
    )
    st.session_state.input = ""
    
    # for hit in search_result["hits"]["hits"]:
    #     answer_text = hit["_source"]  # Use the relevant field from Elasticsearch
    #     st.session_state.answers.append({"answer": answer_text, "id": len(st.session_state.questions)})

    # st.session_state.input = ""


# next create functions to render the question, answer and our history
#finally call the functions and add input form

def write_user_message(md):
    _, col2 = st.columns([1, 12])
    with col2:
        st.warning(md["question"])
        st.write(f"Tokens used: {md['tokens']}")


def render_answer(answer):
    _, col2 = st.columns([1, 12])
    with col2:
        st.info(answer["response"])


def write_chat_message(md):
    chat = st.container()
    with chat:
        render_answer(md["answer"])


with st.container():
    for q, a in zip(st.session_state.questions, st.session_state.answers):
        write_user_message(q)
        write_chat_message(a)


st.markdown("---")
input = st.text_input(
    "You are talking to an AI, ask any question.", key="input", on_change=handle_input
)

# run with command streamlit run app.py


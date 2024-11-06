import streamlit as st
import anthropic
from openai import OpenAI
import yaml

from godmode import preprocess_stream, preprocess_stream_sync


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

anthropic_client = anthropic.Anthropic()
oai_client = OpenAI()


def clear_chat():
    st.session_state.pop("messages", None)


def main():
    st.set_page_config(page_title="Chat with AI Models", layout="wide")
    st.title("Chat with AI Models")

    st.title("Chat with AI Models")
    st.button("Clear chat", on_click=clear_chat)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Say something!")
    st.session_state.messages.append({"role": "user", "content": question})
    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            answer = st.write_stream(stream=preprocess_stream(response["answer"]))

        st.session_state.messages = response["messages"]
        st.session_state.included_conditions = response["included_conditions"]
        st.session_state.messages.append({"role": "assistant", "content": answer})


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_message():
    user_input = st.session_state["user_input"]
    config = load_config()
    for model_name, provider in config["models"].items():
        st.header(f"Response from {model_name} ({provider})")
        if provider == "openai":
            response = oai_client.chat.completion.create(model=model_name, prompt=user_input)
            st.write(response.choices[0].text)
        elif provider == "anthropic":
            response = anthropic_client.chat.completion.create(model=model_name, prompt=user_input)
            st.write(response.completion)
    st.session_state["send_message"] = False


if __name__ == "__main__":
    main()

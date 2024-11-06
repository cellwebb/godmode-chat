import streamlit as st
import anthropic
from openai import OpenAI
import yaml

# from godmode import preprocess_stream


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

anthropic_client = anthropic.Anthropic()
oai_client = OpenAI()


def clear_chat():
    st.session_state.pop("messages", None)


def main():
    st.set_page_config(page_title="Chat with AI Models", layout="wide")
    st.title("Chat with AI Models")

    st.button("Clear chat", on_click=clear_chat)

    if "messages" in st.session_state and st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    else:
        st.session_state.messages = []

    question = st.chat_input("Say something!")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        for model_name, provider in config["models"].items():
            if provider == "openai":
                response = oai_client.chat.completions.create(
                    model=model_name, messages=st.session_state.messages
                )
                answer = response.choices[0].message.content
            elif provider == "anthropic":
                response = anthropic_client.messages.create(
                    model=model_name, max_tokens=1024, messages=st.session_state.messages
                )
                answer = response.content[0].text

            with st.chat_message("assistant"):
                st.write(f"Model: {model_name} - Provider: {provider}")
                st.write(answer)

            # st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()

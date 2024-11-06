from flask import Flask, request, jsonify
import anthropic
from openai import OpenAI
import yaml

app = Flask(__name__)

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

anthropic_client = anthropic.Anthropic()
oai_client = OpenAI()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]
    responses = []

    for model_name, provider in config["models"].items():
        if provider == "openai":
            response = oai_client.chat.completions.create(model=model_name, messages=messages)
            answer = response.choices[0].message.content
        elif provider == "anthropic":
            response = anthropic_client.messages.create(
                model=model_name, max_tokens=1024, messages=messages
            )
            answer = response.content[0].text

        responses.append({"model": model_name, "provider": provider, "answer": answer})

    return jsonify(responses)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

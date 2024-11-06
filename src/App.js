import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");

    const response = await axios.post("http://localhost:5000/chat", {
      messages: newMessages,
    });

    const responses = response.data;
    responses.forEach((res) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "assistant", content: `Model: ${res.model} - Provider: ${res.provider}` },
        { role: "assistant", content: res.answer },
      ]);
    });
  };

  return (
    <div className="App">
      <h1>Chat with AI Models</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Say something!"
      />
      <button onClick={handleSend}>Send</button>
      <button onClick={() => setMessages([])}>Clear chat</button>
    </div>
  );
}

export default App;

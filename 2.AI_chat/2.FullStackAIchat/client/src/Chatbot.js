import React, { useState, useRef } from "react";
import axios from "axios";

const Chatbot = () => {
  const ref = useRef();
  const [messages, setMessages] = useState([
    { role: "system", content: "You are a helpful assistance" },
  ]);
  const [inputMessage, setInputMessage] = useState("");

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage) return;

    const newMessage = { role: "user", content: inputMessage };
    setMessages([...messages, newMessage]);

    ref.current.value = "";
    setInputMessage("");

    try {
      const response = await axios.post("/ask", {
        messages: [...messages, newMessage],
      });
      setMessages(response.data.messages);
    } catch (error) {
      console.log(error);
    }
  };

  const handleChange = (e) => setInputMessage(e.target.value);

  const renderMessages = (message, index) => {
    if (index === 0) return false;
    return (
      <div>
        - {message.role === "user" ? "You: " : "Bot: "}
        <span style={{ fontStyle: "italic" }}> {message.content}</span>
      </div>
    );
  };

  return (
    <>
      <form onSubmit={sendMessage}>
        <input
          ref={ref}
          type="text"
          onChange={handleChange}
          placeholder="Type your message..."
        />
        &nbsp;
        <button type="submit">Send</button>
      </form>
      <br />
      <div>{messages.map(renderMessages)}</div>
    </>
  );
};

export default Chatbot;

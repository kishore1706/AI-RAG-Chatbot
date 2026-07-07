import API from "./api/api";
import { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Message from "./components/Message";
import ChatBox from "./components/ChatBox";
import ChatInput from "./components/ChatInput";
import "./App.css";

function App() {

  const [messages, setMessages] = useState([
  {
    role: "user",
    content: "What is Battery Management System?"
  },
  {
    role: "assistant",
    content:
      "Battery Management System (BMS) monitors, protects, and manages rechargeable batteries to ensure safety and efficiency."
  }
]);
const [loading, setLoading] = useState(false);
  function clearChat() {
    setMessages([]);
  }

  return (
    <div className="app">

      <Header />

      <div className="content">

        <Sidebar clearChat={clearChat} />

        <main className="chat-area">

  <div className="messages-area">
    <ChatBox
    messages={messages}
    loading={loading}
/>
  </div>

  <ChatInput
    onSend={handleSend}
    loading={loading}
/>
</main>

      </div>

    </div>
  );

  async function handleSend(question) {

  // Add user message immediately
  setMessages(prev => [
    ...prev,
    {
      role: "user",
      content: question,
    },
  ]);

  try {
    setLoading(true);
    const response = await API.post("/chat", {
      question: question,
    });

    setMessages(prev => [
      ...prev,
      {
        role: "assistant",
        content: response.data.answer,
      },
    ]);
    setLoading(false);
  } catch (error) {

    setMessages(prev => [
      ...prev,
      {
        role: "assistant",
        content: "❌ Unable to contact the server.",
      },
    ]);
    setLoading(false);  
    console.error(error);
  }
}
}

export default App;
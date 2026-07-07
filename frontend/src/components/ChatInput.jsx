import { useState } from "react";

function ChatInput({ onSend, loading }) {
  const [question, setQuestion] = useState("");

  function handleSend() {
    if (!question.trim()) return;

    onSend(question);
    setQuestion("");
  }
function handleKeyDown(e) {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        handleSend();
    }

}
  return (
    <div className="chat-input">
      <textarea
    placeholder="Ask anything about BMS or ADAS..."
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
    onKeyDown={handleKeyDown}
    disabled={loading}
/>

      <button
    onClick={handleSend}
    disabled={loading}
>
    {loading ? "Thinking..." : "Send"}
</button>
    </div>
  );
}

export default ChatInput;
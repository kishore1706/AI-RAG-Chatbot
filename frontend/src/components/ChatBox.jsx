import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatBox({ messages, loading }) {

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="chat-box">

      {messages.map((msg, index) => (
        <Message
          key={index}
          role={msg.role}
          content={msg.content}
        />
      ))}

      {loading && (
        <Message
          role="assistant"
          content="🤖 Thinking..."
        />
      )}

      <div ref={bottomRef}></div>

    </div>
  );
}

export default ChatBox;
function Message({ role, content }) {
  return (
    <div className={role === "user" ? "user-message" : "bot-message"}>
      <strong>{role === "user" ? "👤 You" : "🤖 Assistant"}</strong>

      <p>{content}</p>
    </div>
  );
}

export default Message;
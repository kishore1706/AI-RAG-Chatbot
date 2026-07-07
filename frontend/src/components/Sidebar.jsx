function Sidebar({ clearChat }) {
  return (
    <aside className="sidebar">
      <h2>Navigation</h2>

      <button onClick={clearChat}>
        🗑️ Clear Chat
      </button>
    </aside>
  );
}

export default Sidebar;
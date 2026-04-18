import { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const chatRef = useRef(null);

  const [form, setForm] = useState({
    hcp_name: "",
    interaction_type: "Meeting",
    date: "",
    time: "",
    topics: "",
    sentiment: "Neutral",
  });

  // ✅ AUTO SCROLL CHAT
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  // ✅ SAFE CRM AUTOFILL (IMPORTANT FIX)
  const applyAIUpdate = (data) => {
    if (!data || typeof data !== "object") return;

    setForm((prev) => ({
      ...prev,
      hcp_name: data.hcp_name || prev.hcp_name,
      interaction_type: data.interaction_type || prev.interaction_type,
      date: data.date || prev.date,   // 🔥 FIX HERE
      time: data.time || prev.time,
      topics: data.topics || prev.topics,
      sentiment: data.sentiment || prev.sentiment,
    }));
  };

  // ✅ SEND MESSAGE TO BACKEND
  const sendMessage = async () => {
    if (!message.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: message }]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message,
      });

      console.log("FULL RESPONSES:", res.data);

      // ✅ SAFE extraction handling (CRITICAL FIX)
      const extracted = res.data.extracted || {};

      // Add bot response
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: res.data.response || "Done" },
      ]);

      // Autofill CRM form
      applyAIUpdate(extracted);

      setMessage("");
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error connecting to backend" },
      ]);
    }
  };

  return (
    <div style={styles.container}>

      {/* LEFT: CRM FORM */}
      <div style={styles.leftPanel}>
        <h2>🧾 CRM Form</h2>

        <input
          placeholder="HCP Name"
          value={form.hcp_name}
          onChange={(e) =>
            setForm({ ...form, hcp_name: e.target.value })
          }
          style={inputStyle}
        />

        <textarea
          placeholder="Topics"
          value={form.topics}
          onChange={(e) =>
            setForm({ ...form, topics: e.target.value })
          }
          style={inputStyle}
        />

        <select
          value={form.interaction_type}
          onChange={(e) =>
            setForm({ ...form, interaction_type: e.target.value })
          }
          style={inputStyle}
        >
          <option>Meeting</option>
          <option>Call</option>
          <option>Visit</option>
        </select>

        <input
          type="date"
          value={form.date}
          onChange={(e) =>
            setForm({ ...form, date: e.target.value })
          }
          style={inputStyle}
        />

        <input
          type="time"
          value={form.time}
          onChange={(e) =>
            setForm({ ...form, time: e.target.value })
          }
          style={inputStyle}
        />

        <select
          value={form.sentiment}
          onChange={(e) =>
            setForm({ ...form, sentiment: e.target.value })
          }
          style={inputStyle}
        >
          <option>Positive</option>
          <option>Neutral</option>
          <option>Negative</option>
        </select>

        <button
          style={btn}
          onClick={() =>
            setMessage(JSON.stringify(form, null, 2))
          }
        >
          Generate Message
        </button>
      </div>

      {/* RIGHT: CHAT */}
      <div style={styles.rightPanel}>
        <h2>💬 AI Chat</h2>

        <div ref={chatRef} style={chatBox}>
          {messages.map((msg, i) => (
            <ChatBubble key={i} role={msg.role} text={msg.text} />
          ))}
        </div>

        <textarea
          rows="3"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={inputStyle}
        />

        <button style={btn} onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

// 💬 Chat Bubble
function ChatBubble({ role, text }) {
  return (
    <div style={{
      textAlign: role === "user" ? "right" : "left",
      marginBottom: "10px"
    }}>
      <span style={{
        display: "inline-block",
        padding: "10px",
        borderRadius: "10px",
        background: role === "user" ? "#4e73df" : "#eaeaea",
        color: role === "user" ? "white" : "black",
        maxWidth: "70%",
        wordBreak: "break-word"
      }}>
        {text}
      </span>
    </div>
  );
}

// 🎨 Styles
const styles = {
  container: {
    display: "flex",
    height: "100vh",
    fontFamily: "Arial",
    background: "#f4f6f9"
  },
  leftPanel: {
    width: "50%",
    padding: "25px",
    background: "white",
    boxShadow: "0 0 10px rgba(0,0,0,0.05)"
  },
  rightPanel: {
    width: "50%",
    padding: "25px",
    display: "flex",
    flexDirection: "column"
  }
};

const chatBox = {
  flex: 1,
  overflowY: "auto",
  background: "#fff",
  padding: "15px",
  borderRadius: "10px",
  marginBottom: "10px",
  boxShadow: "0 0 10px rgba(0,0,0,0.05)"
};

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "10px",
  borderRadius: "8px",
  border: "1px solid #ddd"
};

const btn = {
  padding: "12px",
  background: "#4e73df",
  color: "white",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  marginTop: "10px"
};

export default App;
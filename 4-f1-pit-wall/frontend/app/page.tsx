'use client';

import { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: 'demo' }),
      });
      const data = await res.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        agent: data.agent || 'Pit Wall',
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Connection error. Is the API running?', agent: 'System' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🏎️</span>
          <h1>F1 PIT WALL</h1>
          <span className="subtitle">AI Command Center</span>
        </div>
        <div className="status">
          <span className="status-dot"></span> LIVE
        </div>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>Welcome to the Pit Wall</h2>
              <p>Ask me anything about Formula 1 — strategy, stats, history, or regulations.</p>
              <div className="suggestions">
                <button onClick={() => setInput('What tire strategy should Ferrari use at Monza?')}>
                  🏁 Tire Strategy
                </button>
                <button onClick={() => setInput('Who has the most wins in F1 history?')}>
                  🏆 Records
                </button>
                <button onClick={() => setInput('Show me the current championship standings')}>
                  📊 Standings
                </button>
                <button onClick={() => setInput('Explain the 2026 active aero rules')}>
                  ⚙️ Regulations
                </button>
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              {msg.role === 'assistant' && msg.agent && (
                <div className="agent-badge">{msg.agent}</div>
              )}
              <div className="message-content">{msg.content}</div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="agent-badge">Analyzing...</div>
              <div className="message-content loading-dots">
                <span>●</span><span>●</span><span>●</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask your race engineer..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>
            Send
          </button>
        </div>
      </div>
    </main>
  );
}

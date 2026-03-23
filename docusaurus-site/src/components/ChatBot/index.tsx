import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

interface Source {
  chapter: string;
  section: string;
  slug: string;
  relevance_score: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
}

/**
 * Floating AI chatbot widget for the AI-Native Development book.
 * Supports full-book RAG queries and selected-text context queries.
 * Connects to the backend at http://localhost:8000.
 */
export default function ChatBot(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Capture text selections from the page so users can ask about them
  useEffect(() => {
    const handleSelection = () => {
      const sel = window.getSelection()?.toString().trim();
      if (sel && sel.length > 10) setSelectedText(sel);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const BACKEND = 'https://ismatz-hackathon1deploy.hf.space';
      let url = `${BACKEND}/api/chat`;
      let body: Record<string, unknown> = { query: input, top_k: 5 };

      // If the user has selected text, use the selection-aware endpoint
      if (selectedText) {
        url = `${BACKEND}/api/chat-selected`;
        body = { query: input, selected_text: selectedText };
      }

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Error connecting to backend. Make sure the backend is running at http://localhost:8000.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating action button */}
      <button
        className={styles.fab}
        onClick={() => setIsOpen(!isOpen)}
        title="Ask AI about this book"
        aria-label={isOpen ? 'Close AI assistant' : 'Open AI assistant'}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className={styles.panel} role="dialog" aria-label="AI Book Assistant">
          <div className={styles.header}>
            <div className={styles.headerLeft}>
              <span className={styles.headerDot} />
              <span>📚 AI Book Assistant</span>
            </div>
            {selectedText && (
              <span className={styles.selectionBadge}>Using selected text</span>
            )}
          </div>

          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.welcome}>
                <span className={styles.welcomeIcon}>📚</span>
                <p className={styles.welcomeText}>
                  Ask me anything about this book. You can also <strong>select any text</strong> on the page and ask questions about it!
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`${styles.message} ${styles[msg.role]}`}>
                <div className={styles.bubble}>{msg.content}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    Sources: {msg.sources.map(s => s.section).join(', ')}
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className={styles.loading}>
                <span className={styles.dot} />
                <span className={styles.dot} />
                <span className={styles.dot} />
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.inputRow}>
            <input
              className={styles.input}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={selectedText ? 'Ask about selected text...' : 'Ask about the book...'}
              aria-label="Chat input"
              disabled={loading}
            />
            <button
              className={styles.sendBtn}
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              aria-label="Send message"
            >
              Send
            </button>
          </div>

          {/* Show a snippet of the selected text for context awareness */}
          {selectedText && (
            <div className={styles.selectionInfo}>
              <button
                onClick={() => setSelectedText('')}
                aria-label="Clear text selection"
              >
                ✕ Clear selection
              </button>
              <span>"{selectedText.slice(0, 60)}{selectedText.length > 60 ? '...' : ''}"</span>
            </div>
          )}
        </div>
      )}
    </>
  );
}

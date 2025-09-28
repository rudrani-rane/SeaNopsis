import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const callChatbotAPI = async (userMessage) => {
  try {
    const response = await fetch('http://localhost:8000/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMessage,
        user_id: 'anonymous', // You can add user authentication later
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data.response || data.message || data.reply || 'Sorry, I could not process your request.';
  } catch (error) {
    console.error('Chatbot API error:', error);
    return 'Sorry, I encountered an error. Please check if the backend is running.';
  }
};

const TypingText = ({ text }) => {
  const [displayed, setDisplayed] = useState('');
  useEffect(() => {
    setDisplayed('');
    let i = 0;
    const id = setInterval(() => {
      if (i < (text?.length || 0)) {
        setDisplayed((prev) => prev + text[i]);
        i += 1;
      } else {
        clearInterval(id);
      }
    }, 18);
    return () => clearInterval(id);
  }, [text]);
  return <span>{displayed}</span>;
};

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { id: 0, role: 'bot', text: 'Ask me about salinity, species or datasets.' },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const listRef = useRef(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const send = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    
    const userMsg = { id: Date.now(), role: 'user', text: trimmed };
    setMessages((m) => [...m, userMsg, { id: Date.now() + 1, role: 'bot-typing', text: '...' }]);
    setInput('');
    setIsLoading(true);

    try {
      const reply = await callChatbotAPI(trimmed);
      setMessages((m) => 
        m.filter((x) => x.role !== 'bot-typing')
         .concat({ id: Date.now(), role: 'bot', text: reply })
      );
    } catch (error) {
      setMessages((m) => 
        m.filter((x) => x.role !== 'bot-typing')
         .concat({ id: Date.now(), role: 'bot', text: 'Sorry, something went wrong. Please try again.' })
      );
    } finally {
      setIsLoading(false);
    }
  };

  const onKey = (e) => {
    if (e.key === 'Enter') send();
  };

  return (
    <section className="mx-auto max-w-7xl px-6 py-10">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <h2 className="text-2xl font-bold text-white/90">Ask About Marine Data</h2>
          <p className="mt-1 text-cyan-100/80">Type your question and get quick insights.</p>
        </div>

        <div className="lg:col-span-2">
          <div className="rounded-2xl border border-white/15 bg-white/10 shadow-xl backdrop-blur-xl">
            <div ref={listRef} className="max-h-80 overflow-y-auto px-5 py-4">
              <AnimatePresence initial={false}>
                {messages.map((m) => (
                  <motion.div
                    key={m.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    className={`my-2 flex ${m.role.startsWith('bot') ? 'justify-start' : 'justify-end'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-xl px-4 py-2 text-sm shadow-md ${
                        m.role.startsWith('bot')
                          ? 'bg-cyan-900/40 text-cyan-100 border border-cyan-300/20'
                          : 'bg-teal-500/90 text-white'
                      }`}
                    >
                      {m.role === 'bot' ? <TypingText text={m.text} /> : m.text}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            <div className="flex items-center gap-3 border-t border-white/10 p-4">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={onKey}
                placeholder="Type your question..."
                className="flex-1 rounded-xl border border-white/10 bg-white/10 px-4 py-2 text-white placeholder:text-cyan-100/60 focus:border-cyan-300/40 focus:outline-none"
              />
              <button
                onClick={send}
                disabled={isLoading}
                className="rounded-xl bg-gradient-to-r from-teal-500 to-cyan-500 px-4 py-2 font-medium text-white shadow-lg shadow-teal-500/30 transition hover:from-teal-400 hover:to-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Chatbot;



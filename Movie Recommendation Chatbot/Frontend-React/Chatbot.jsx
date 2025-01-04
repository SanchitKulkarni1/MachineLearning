

import React, { useState } from 'react';
import axios from 'axios';
import './chatbot.css';

function Chatbot() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput) return;
  
    const userMessage = { text: trimmedInput, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput(''); // Clear the input immediately
    setLoading(true);
  
    try {
      const response = await axios.post('http://127.0.0.1:5000/recommend', {
        query: trimmedInput,
      });
  
      const recommendations = response.data.recommendations;
      const botMessages = recommendations.length
        ? recommendations.map((movie) => ({ text: movie, sender: 'bot' }))
        : [{ text: 'No recommendations found for your query.', sender: 'bot' }];
  
      setMessages((prevMessages) => [...prevMessages, ...botMessages]);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: 'Sorry, something went wrong. Please try again later.', sender: 'bot' },
      ]);
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      {loading && <div className="loading">Bot is typing...</div>}
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask for movie recommendations..."
          className="input"
          aria-label="Chat input field"
        />
        <button onClick={handleSendMessage} className="button" disabled={loading}>
          {loading ? 'Loading...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default Chatbot;

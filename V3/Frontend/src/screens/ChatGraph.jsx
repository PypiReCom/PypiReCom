import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import GraphComponent from "../components/Graph";
import { BASE_URL } from "../api-endpoint";

const ChatGraph = () => {
  const { searchText } = useParams();
  const [userMessage, setUserMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [graphData, setGraphData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const inputRef = useRef(null);              // For auto-focus
  const chatContainerRef = useRef(null);      // For auto scroll

  // Fetch graph data
  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BASE_URL}/search?Search_Text=${searchText}`);
      const data = await response.json();

      if (data && data.result) {
        setGraphData(data);
      } else {
        setError('No graph data found');
      }
    } catch (err) {
      setError('Error fetching graph data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (searchText) {
      fetchData();
    }
  }, [searchText]);

  // Scroll to latest message
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatMessages]);

  // Auto focus on input
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = async () => {
    if (userMessage.trim() === '') return;

    setChatMessages([...chatMessages, { message: userMessage, isBot: false }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/chat?Search_Text=${encodeURIComponent(userMessage)}&Gml_Name=${encodeURIComponent(searchText)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        const displayMessager = data.result || (typeof data === 'object' ? JSON.stringify(data, null, 2) : data);
        const displayMessage = displayMessager
          .replace(/\* /g, '• ')
          .replace(/1\. /, '\n1. ')
          .replace(/So, the list/, '\nSo, the list')
          .replace(/From the triples/, '\nFrom the triples')
          .replace(/Specifically/, '\nSpecifically')
          .replace(/The triples/, '\nThe triples')
          .replace(/Based on/, '\nBased on');

        setChatMessages(prevMessages => [...prevMessages, { message: displayMessage, isBot: true }]);
      } else {
        const errorData = await response.json();
        setChatMessages(prevMessages => [...prevMessages, { message: `Error: ${errorData.detail[0].msg}`, isBot: true }]);
      }
    } catch (error) {
      console.error("Error fetching chat response:", error);
      setChatMessages(prevMessages => [...prevMessages, { message: 'Error fetching response. Please try again.', isBot: true }]);
    } finally {
      setUserMessage('');
      setIsLoading(false);
    }
  };

  // Handle Enter key to send message
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div>
      <Navbar />
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
        <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>Chat with {searchText} Graph</h3>

        {graphData && <GraphComponent data={graphData} />}

        <div
          ref={chatContainerRef}
          style={{
            border: '1px solid #ddd',
            borderRadius: '10px',
            padding: '20px',
            backgroundColor: '#f9f9f9',
            maxHeight: '400px',
            overflowY: 'auto',
            marginBottom: '20px'
          }}
        >
          {chatMessages.map((chat, index) => (
            <div key={index} style={{
              backgroundColor: chat.isBot ? '#e0e0e0' : '#007bff',
              color: chat.isBot ? '#000' : '#fff',
              padding: '10px',
              borderRadius: '10px',
              textAlign: chat.isBot ? 'left' : 'right',
              marginBottom: '10px',
              maxWidth: '75%',
              alignSelf: chat.isBot ? 'flex-start' : 'flex-end',
              marginLeft: chat.isBot ? '0' : 'auto',
              wordWrap: 'break-word',
              whiteSpace: 'normal',
              lineHeight: '1.5',
              fontSize: '15px',
            }}>
              <div style={{ whiteSpace: 'pre-wrap' }}>{chat.message}</div>
            </div>
          ))}

          {isLoading && (
            <div style={{ textAlign: 'center' }}>
              <div style={{
                display: 'inline-block',
                width: '30px',
                height: '30px',
                border: '4px solid rgba(0,0,0,0.2)',
                borderTop: '4px solid #007bff',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }} />
              <style>{`
                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
              `}</style>
            </div>
          )}
        </div>

        {/* Chat input box */}
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <input
            type="text"
            ref={inputRef}
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            style={{
              width: '80%',
              padding: '10px',
              borderRadius: '5px',
              border: '1px solid #ccc',
            }}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading}
            style={{
              marginLeft: '10px',
              padding: '10px 20px',
              backgroundColor: isLoading ? '#aaa' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
            }}
          >
            Send
          </button>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ChatGraph;

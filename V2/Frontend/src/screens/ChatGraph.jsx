import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import GraphComponent from "../components/Graph";
import { BASE_URL } from "../api-endpoint";

const ChatGraph = () => {
  const { searchText } = useParams();  // Fetch searchText from URL parameters
  const [userMessage, setUserMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [graphData, setGraphData] = useState(null); // State to store fetched graph data
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null); // State to handle errors
  const [loading, setLoading] = useState(true); // State to handle loading


  const fetchData = async () => {
    try {
      setLoading(true); // Start loading
      const response = await fetch(`${BASE_URL}/search?Search_Text=${searchText}`);
      const data = await response.json();
      
      if (data && data.result) {
        setGraphData(data); // Set the graph data if successful
      } else {
        setError('No graph data found');
      }
    } catch (err) {
      setError('Error fetching graph data');
    } finally {
      setLoading(false); // End loading
    }
  };

  useEffect(() => {
    if (searchText) {
      fetchData();
    }
  }, [searchText]);




  

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (userMessage.trim() === '') return;  // Avoid sending empty messages

    // Add the user message to the chat
    setChatMessages([...chatMessages, { message: userMessage, isBot: false }]);
    setIsLoading(true);

    // Fetch the response from the backend API
    try {
      // Send the data as query parameters in the URL
      const response = await fetch(`${BASE_URL}/chat?Search_Text=${encodeURIComponent(userMessage)}&Gml_Name=${encodeURIComponent(searchText)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        
        // If the response is an object, convert it to a string for display
        const displayMessage = typeof data === 'object' ? JSON.stringify(data, null, 2) : data;

        // Add the bot's response to the chat
        setChatMessages(prevMessages => [...prevMessages, { message: displayMessage, isBot: true }]);
      } else {
        const errorData = await response.json();
        setChatMessages(prevMessages => [...prevMessages, { message: `Error: ${errorData.detail[0].msg}`, isBot: true }]);
      }
    } catch (error) {
      console.error("Error fetching chat response:", error);
      setChatMessages(prevMessages => [...prevMessages, { message: 'Error fetching response. Please try again.', isBot: true }]);
    } finally {
      setUserMessage('');  // Clear input field
      setIsLoading(false);  // Remove loading state
    }
  };

  return (
    <div>
      <Navbar />
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
        <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>Chat with  {searchText} Graph</h3>

        {graphData && <GraphComponent data={graphData} />} {/* Render GraphComponent with fetched data */}

        {/* <p style={{ textAlign: 'center', color: '#666' }}>Search Text: {searchText}</p> */}

        {/* Chatbox container */}
        <div style={{
          border: '1px solid #ddd',
          borderRadius: '10px',
          padding: '20px',
          backgroundColor: '#f9f9f9',
          maxHeight: '400px',
          overflowY: 'auto',
          marginBottom: '20px'
        }}>
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
              marginLeft: chat.isBot ? '0' : 'auto'
            }}>
              <pre>{chat.message}</pre>
            </div>
          ))}
                  
          {isLoading && <p style={{ textAlign: 'center', color: '#666' }}>Loading...</p>}
        </div>

        {/* Chat input box */}
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <input
            type="text"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
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
            style={{
              marginLeft: '10px',
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
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
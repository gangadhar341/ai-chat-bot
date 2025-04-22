import React, { useState, useRef, useEffect } from "react";
import "./Chat.css"; // Import the CSS file
import { sendQuery } from "../../services/api"; // Import the sendQuery function

export default function Chat() {
  const [isChatVisible, setIsChatVisible] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState([
    { type: "ai", text: "Hello! How can I assist you today?" },
  ]); // Store chat messages
  const [userInput, setUserInput] = useState(""); // Store user input
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const messageAreaRef = useRef(null); // Reference to the message area
  let typingTimeout; // Declare a timeout variable

  const toggleChat = () => {
    setIsChatVisible(!isChatVisible);
  };

  const handleTyping = (e) => {
    setUserInput(e.target.value);

    // Clear any existing timeout
    if (typingTimeout) {
      clearTimeout(typingTimeout);
    }

    // Set `isTyping` to true immediately when the user starts typing
    setIsTyping(true);

    // Set a timeout to set `isTyping` to false after the user stops typing
    typingTimeout = setTimeout(() => {
      setIsTyping(false);
    }, 1000); // Adjust the delay (in milliseconds) as needed
  };

  const handleSend = async () => {
    if (userInput.trim() === "") return;

    // Add user message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { type: "user", text: userInput },
    ]);

    setIsTyping(false);
    setUserInput(""); // Clear input field

    try {
      setIsLoading(true); // Set loading state to true
      // Send the user's question to the API
      const response = await sendQuery({ question: userInput });

      // Add AI response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "ai", text: response.data.answer },
      ]);
    } catch (error) {
      console.error("Error sending query:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "ai", text: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setIsLoading(false); // Set loading state to false
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend(); // Trigger the send function when Enter is pressed
    }
  };

  // Scroll to the latest message or typing indicator whenever messages, isLoading, or isTyping changes
  useEffect(() => {
    if (messageAreaRef.current) {
      messageAreaRef.current.scrollTop = messageAreaRef.current.scrollHeight;
    }
  }, [messages, isLoading, isTyping]);

  return (
    <div className='container'>
      {/* Message Icon Button */}
      <button className='message-icon' onClick={toggleChat}>
        💬
      </button>

      {/* Chat Container */}
      {isChatVisible && (
        <div className={`chat-container ${isChatVisible ? "open" : "close"}`}>
          <div className='message-area' ref={messageAreaRef}>
            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.type === "ai" ? "ai-message" : "user-message"
                }
              >
                {message.text}
              </div>
            ))}

            {/* AI Typing Indicators */}
            {isLoading && (
              <div className='ai-typing-indicator'>AI is thinking...</div>
            )}

            {/* User Typing Indicators */}
            {isTyping && (
              <div className='user-typing-indicator'>User is typing...</div>
            )}
          </div>
          <div className='input-area'>
            <input
              type='text'
              className='message-input'
              placeholder='Type your message here...'
              value={userInput}
              onChange={handleTyping}
              onKeyDown={handleKeyDown}
            />
            <button className='send-button' onClick={handleSend}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

import { useState } from 'react'
import './App.css'

function App() {
  return (
    <>
      <div className="app">
      <div className="header">
        <h1>LearnAI-Bot</h1>
        <p>Upload a PDF and ask questions about its content</p>
      </div>

      {/* File Upload Section */}
      <div className="upload-section">
        <input
          type="file"
          accept=".pdf"
        />
        <button 
          className="upload-btn"
        > 
          Upload
        </button>
      </div>

      {/* Chat Interface */}
      <div className="chat-container">
        <div className="messages">
            <div className="welcome-message">
              Upload a PDF file above and start asking questions!
            </div>
            <div className="message ai">
              <div className="message-content">
                <strong>AI:</strong> <span>Thinking...</span>
              </div>
            </div>
        </div>

      {/* Question Input */}
      <div className="input-section">
        <input
          type="text"
          className="question-input"
        />
        <button 
          className="ask-btn"
        >
          Send
        </button>
      </div>
      </div>
    </div>
    </>
  )
}

export default App


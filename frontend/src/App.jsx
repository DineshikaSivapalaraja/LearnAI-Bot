import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [question, setQuestion] = useState('')
  const [file, setFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isAsking, setIsAsking] = useState(false)        
  const [uploadStatus, setUploadStatus] = useState('')

  // handle file upload
  const handleFileUpload = async () => {
    if (!file) {
      alert('Please select a PDF file first')
      return
    }

    setIsLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`http://127.0.0.1:8000/upload-file`, {
        method: 'POST',
        body: formData,
      })
      const result = await response.json()
      setUploadStatus(`${result.message}`)
      setFile(null)
    } catch (error) {
      setUploadStatus('Upload failed')
      console.error('Upload error:', error)
    }
    setIsLoading(false)
  }

  // handle question submission
  const handleAskQuestion = async () => {
    if (!question.trim()) return

    setIsAsking(true)
    // add user question to messages
    const userMessage = { type: 'user', content: question }
    setMessages(prev => [...prev, userMessage])

    try {
      const response = await fetch(`http://127.0.0.1:8000/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      // check if response is successful
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to get answer')
      }

      const result = await response.json()
      
      // add AI response to messages
      const aiMessage = { type: 'ai', content: result.answer }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      const errorMessage = { type: 'error', content: 'Sorry, something went wrong.' }
      setMessages(prev => [...prev, errorMessage])
      console.error('Ask error:', error)
    }

    setQuestion('')
    setIsAsking(false)
  }

  return (
  <div className="app">

    {/* Left side(Header Section) */}
    <div className="left-panel">
      <div className="header">
        <h1>LearnAI-Bot</h1>
        <h2>Welcome to your AI-powered Reading Assistant!</h2>
        <img src="image.jpg" alt="LearnAI-BOT" />
        <p>Upload your PDF and ask questions about it. <br/> 
        Save time and Get to the point!</p>
      </div>
    </div>

    {/* Right Side(Main Functionalities) */}
    <div className="right-panel">

      {/* 1. File Upload Section */}
      <div className="upload-section">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          disabled={isLoading}
        />
        <button 
          onClick={handleFileUpload} 
          disabled={!file || isLoading}
          className="upload-btn"
        >
          {isLoading ? 'Uploading...' : 'Upload PDF'}
        </button>
        {uploadStatus && <div className="upload-status">{uploadStatus}</div>}
      </div>

      {/* 2. Chat Interface */}
      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
                Upload a PDF file above and start asking questions!
            </div>
          )}
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">
                {message.type === 'user' && <strong>You:</strong>}
                {message.type === 'ai' && <strong>AI:</strong>}
                {message.type === 'error' && <strong>Error:</strong>}
                <span> {message.content}</span>
              </div>
            </div>
          ))}
          {isAsking && (
            <div className="message ai">
              <div className="message-content">
                <strong>AI:</strong> <span>Thinking...</span>
              </div>
            </div>
          )}
        </div>

        {/* 3. Question Input */}
        <div className="input-section">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask an question about your PDF..."
            onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
            disabled={isAsking}
            className="question-input"
          />
          <button 
            onClick={handleAskQuestion}
            disabled={!question.trim() || isAsking}
            className="ask-btn"
          >
            {isAsking ? 'Sending...' : 'Send'} 
          </button>
        </div>
      </div>
    </div>
  </div>
)
}

export default App
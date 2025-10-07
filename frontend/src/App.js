import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
  Send, 
  Users, 
  Bot, 
  User, 
  Activity, 
  Settings,
  MessageSquare,
  Zap,
  CheckCircle,
  AlertCircle,
  Loader
} from 'lucide-react';
import './App.css';

// Configure axios defaults
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://web--microsoft-agent-framework--4h7vh8ddvxpx.code.run';
axios.defaults.baseURL = API_BASE_URL;

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [teamStatus, setTeamStatus] = useState(null);
  const [showTeamPanel, setShowTeamPanel] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check connection and load team status
  useEffect(() => {
    checkConnection();
    loadTeamStatus();
  }, []);

  const checkConnection = async () => {
    try {
      await axios.get('/health');
      setConnectionStatus('connected');
    } catch (error) {
      setConnectionStatus('disconnected');
      console.error('Connection failed:', error);
    }
  };

  const loadTeamStatus = async () => {
    try {
      const response = await axios.get('/team/status');
      setTeamStatus(response.data);
    } catch (error) {
      console.error('Failed to load team status:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/team/chat', {
        message: inputMessage
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        orchestrator: response.data.orchestrator || 'Team Lead',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Refresh team status after each interaction
      loadTeamStatus();
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'connecting':
        return <Loader className="w-4 h-4 text-yellow-500 animate-spin" />;
      default:
        return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo">
            <Bot className="w-8 h-8 text-blue-600" />
            <h1>Microsoft Agent Framework</h1>
          </div>
          <div className="connection-status">
            {getConnectionStatusIcon()}
            <span className={`status-text ${connectionStatus}`}>
              {connectionStatus === 'connected' ? 'Connected' : 
               connectionStatus === 'connecting' ? 'Connecting...' : 'Disconnected'}
            </span>
          </div>
        </div>
        
        <div className="header-right">
          <button 
            className={`team-button ${showTeamPanel ? 'active' : ''}`}
            onClick={() => setShowTeamPanel(!showTeamPanel)}
          >
            <Users className="w-5 h-5" />
            Team Status
          </button>
        </div>
      </header>

      <div className="app-body">
        {/* Team Status Panel */}
        {showTeamPanel && (
          <div className="team-panel">
            <div className="team-panel-header">
              <h3><Users className="w-5 h-5" /> Team Status</h3>
              <button onClick={loadTeamStatus} className="refresh-button">
                <Activity className="w-4 h-4" />
              </button>
            </div>
            
            {teamStatus ? (
              <div className="team-content">
                <div className="team-summary">
                  <div className="stat">
                    <span className="stat-number">{teamStatus.total_members}</span>
                    <span className="stat-label">Total Members</span>
                  </div>
                  <div className="stat">
                    <span className="stat-number">{teamStatus.available_members}</span>
                    <span className="stat-label">Available</span>
                  </div>
                  <div className="stat">
                    <span className="stat-number">{teamStatus.active_tasks}</span>
                    <span className="stat-label">Active Tasks</span>
                  </div>
                </div>
                
                <div className="team-members">
                  {Object.entries(teamStatus.team_members).map(([role, member]) => (
                    <div key={role} className="team-member">
                      <div className="member-header">
                        <div className="member-name">
                          {role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </div>
                        <div className={`member-status ${member.available ? 'available' : 'busy'}`}>
                          {member.available ? 'Available' : 'Busy'}
                        </div>
                      </div>
                      <div className="member-specialties">
                        {member.specialties.join(', ')}
                      </div>
                      <div className="member-stats">
                        Tasks completed: {member.tasks_completed}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="loading-team">
                <Loader className="w-6 h-6 animate-spin" />
                Loading team status...
              </div>
            )}
          </div>
        )}

        {/* Chat Area */}
        <div className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <div className="welcome-content">
                  <Bot className="w-16 h-16 text-blue-600 mb-4" />
                  <h2>Welcome to your AI Team!</h2>
                  <p>I'm your Team Lead. I coordinate with specialists to handle any request:</p>
                  <div className="specialists-grid">
                    <div className="specialist">
                      <Zap className="w-5 h-5" />
                      <span>Code Assistant</span>
                    </div>
                    <div className="specialist">
                      <Activity className="w-5 h-5" />
                      <span>Data Analyst</span>
                    </div>
                    <div className="specialist">
                      <MessageSquare className="w-5 h-5" />
                      <span>Customer Support</span>
                    </div>
                    <div className="specialist">
                      <Settings className="w-5 h-5" />
                      <span>API Integrator</span>
                    </div>
                  </div>
                  <p className="welcome-cta">Ask me anything - I'll delegate to the right specialist!</p>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div className="message-avatar">
                  {message.type === 'user' ? (
                    <User className="w-6 h-6" />
                  ) : message.type === 'error' ? (
                    <AlertCircle className="w-6 h-6" />
                  ) : (
                    <Bot className="w-6 h-6" />
                  )}
                </div>
                
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {message.type === 'user' ? 'You' : 
                       message.type === 'error' ? 'System' : 
                       message.orchestrator || 'Team Lead'}
                    </span>
                    <span className="message-time">
                      {formatTimestamp(message.timestamp)}
                    </span>
                  </div>
                  
                  <div className="message-text">
                    {message.type === 'bot' ? (
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message bot loading">
                <div className="message-avatar">
                  <Bot className="w-6 h-6" />
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">Team Lead</span>
                  </div>
                  <div className="typing-indicator">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="typing-text">Analyzing request and coordinating team...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chat-input-container">
            <div className="chat-input">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask your team anything... (Press Enter to send)"
                disabled={isLoading || connectionStatus !== 'connected'}
                rows={1}
              />
              <button 
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading || connectionStatus !== 'connected'}
                className="send-button"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

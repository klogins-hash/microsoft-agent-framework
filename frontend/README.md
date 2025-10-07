# Microsoft Agent Framework - Frontend

A beautiful, modern React frontend for chatting with your AI team through the Team Orchestrator.

## 🚀 Features

- **Single Chat Interface**: Talk to your Team Lead who coordinates with specialists
- **Real-time Team Status**: See which team members are available or busy
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Markdown Support**: Rich text rendering for agent responses
- **Connection Status**: Visual indicators for API connectivity
- **Mobile Responsive**: Works great on all devices

## 🎯 Team Members Displayed

- **Code Assistant**: Programming, debugging, code review
- **Data Analyst**: Data analysis, statistics, visualization
- **Customer Support**: Help desk, issue resolution
- **API Integrator**: MCP servers, external integrations
- **Content Creator**: Writing, documentation, creative content

## 🛠️ Setup

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure API URL** (optional):
Create `.env` file:
```bash
REACT_APP_API_URL=https://your-deployment-url.com
```

3. **Start development server**:
```bash
npm start
```

The app will open at `http://localhost:3000`

## 🌐 Production Build

```bash
npm run build
```

This creates an optimized build in the `build/` folder ready for deployment.

## 📱 Usage

1. **Chat Interface**: Type your message and press Enter or click Send
2. **Team Status**: Click "Team Status" to see member availability
3. **Auto-delegation**: The Team Lead automatically assigns tasks to specialists
4. **Rich Responses**: Markdown formatting for code, lists, and formatting

## 🎨 Key Components

- **App.js**: Main chat interface and team coordination
- **Team Panel**: Real-time status of all team members
- **Message Components**: User and bot message rendering
- **Connection Status**: API connectivity monitoring

## 🔧 Configuration

The frontend automatically connects to your deployed Microsoft Agent Framework API. It uses:

- **Team Chat Endpoint**: `POST /team/chat`
- **Team Status Endpoint**: `GET /team/status`  
- **Health Check**: `GET /health`

## 📦 Dependencies

- **React 18**: Modern React with hooks
- **Axios**: HTTP client for API calls
- **React Markdown**: Rich text rendering
- **Lucide React**: Beautiful icons
- **CSS3**: Modern styling with gradients and animations

## 🎯 How It Works

1. **Single Entry Point**: All messages go to the Team Lead
2. **Auto-delegation**: Team Lead analyzes and assigns to specialists
3. **Coordinated Responses**: Multiple specialists can work together
4. **Real-time Status**: See team member availability and task progress
5. **Unified Interface**: One chat handles all your needs

Just type what you need - the Team Lead handles the rest! 🤖✨

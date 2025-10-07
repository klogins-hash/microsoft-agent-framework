{{ ... }}

A powerful framework for building AI agents inspired by the Microsoft Agent Framework, but using Groq models instead of OpenAI. This framework provides an expert agent builder that specializes in creating and configuring other Microsoft-style agents.

## 🚀 Features

- **Expert Agent Builder**: Meta-agent that specializes in creating other Microsoft-style agents
- **MCP Integration**: Automatic API-to-MCP server conversion for universal API access
- **Multiple Agent Templates**: Pre-built templates for common use cases
- **Groq Integration**: Fast LLM inference using latest Groq models
- **Context Management**: Persistent conversation threads and memory
- **Tool System**: Extensible tools for web, file, and code operations
- **Microsoft Integration Ready**: Built for Microsoft ecosystem compatibility
- **Database Persistence**: SQLAlchemy-based data storage
- **Streaming Support**: Real-time conversation streaming
- **FastAPI Web Interface**: Complete REST API for web integration
- **API Discovery**: Automatic discovery and integration of external APIs
- **MCP Server Generation**: Convert any API (OpenAPI, GraphQL, REST, Webhooks) to MCP server interface

## 📦 Installation

1. Clone the repository:
```bash
{{ ... }}
git clone <repository-url>
cd microsoft-agent-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## 🔧 Configuration

Create a `.env` file with your Groq API configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_GROQ_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096
```

## 🎯 Quick Start

### Using the CLI

1. **List available agent templates:**
```bash
python main.py list-templates
```

2. **Create an agent interactively:**
```bash
python main.py create-agent code_assistant --interactive
```

3. **Use the master agent builder:**
```bash
python main.py build-agent
```

4. **Start a chat session:**
```bash
python main.py chat --template customer_support
```

### Using the Python API

```python
import asyncio
from microsoft_agent_framework import AgentBuilder

async def main():
    # Initialize the agent builder
    builder = AgentBuilder()
    
    # Create a code assistant agent
    agent = builder.create_agent_from_template(
        "code_assistant",
        name="My Code Helper"
    )
    
    # Chat with the agent
    response = await agent.run_async("Write a Python function to sort a list")
    print(response)

asyncio.run(main())
## 🤖 Available Agent Templates

| Template | Description | Use Cases |
|----------|-------------|-----------|
| `customer_support` | Professional customer service agent | Help desk, issue resolution, inquiries |
| `code_assistant` | Software development helper | Code generation, debugging, reviews |
| `data_analyst` | Data analysis and visualization expert | Data insights, reporting, statistics |
| `teams_bot` | Microsoft Teams integration ready | Team collaboration, scheduling |
| `agent_builder` | Meta-agent for building other agents | Agent architecture, configuration |

## 🛠️ Tools and Capabilities

The framework includes several built-in tool categories:

{{ ... }}
- Fetch content from URLs
- Make HTTP requests
- Check URL status

### File Tools
- Read/write files
- Directory operations
- JSON handling

### Code Tools
- Execute Python code safely
- Validate syntax
- Code analysis
- Project structure creation

## 📖 Examples

### Basic Usage
```python
from microsoft_agent_framework import AgentBuilder
from microsoft_agent_framework.tools import WebTools, FileTools

# Create builder and register tools
builder = AgentBuilder()
web_tools = WebTools()
file_tools = FileTools()

builder.register_tool("fetch_url", web_tools.fetch_url)
builder.register_tool("read_file", file_tools.read_file)

# Create a custom agent
agent = builder.create_custom_agent(
    name="Research Assistant",
    instructions="You help with research by finding and analyzing information.",
    tools=["fetch_url", "read_file"]
)

# Use the agent
response = await agent.run_async("Research the latest trends in AI")
```

### Master Agent Builder
```python
# Use the master agent to get recommendations
builder = AgentBuilder()

recommendation = await builder.get_agent_recommendation(
    "I need an agent that can help me analyze CSV data and create reports"
)

print(recommendation)

# Build agent from natural language description
agent = await builder.build_agent_from_description(
    "Create an agent for customer support that handles technical issues"
)
```

### Streaming Responses
```python
# Get streaming responses
async for update in agent.run_streaming_async("Explain machine learning"):
    print(update.content, end="", flush=True)
```

## 🏗️ Architecture

The framework follows the Microsoft Agent Framework architecture:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Agent Builder │────│  Base Agent  │────│ Groq Client │
│   (Meta-Agent)  │    │              │    │             │
└─────────────────┘    └──────────────┘    └─────────────┘
         │                       │                  │
         │                       │                  │
    ┌─────────┐            ┌──────────┐      ┌──────────┐
    │ Templates│            │  Tools   │      │ Context  │
    │         │            │          │      │ Provider │
    └─────────┘            └──────────┘      └──────────┘
```

### Core Components

- **AgentBuilder**: Expert meta-agent for creating other agents
- **BaseAgent**: Foundation class for all agents
- **GroqClient**: Integration with Groq's LLM API
- **AgentThread**: Conversation state management
- **ContextProvider**: Memory and context storage
- **Tools**: Extensible capability system

## 🔧 Customization

### Creating Custom Templates
```python
from microsoft_agent_framework.core.agent_builder import AgentTemplate

custom_template = AgentTemplate(
    name="Custom Agent",
    description="Specialized agent for specific tasks",
    instructions="Your custom instructions here...",
    model="llama3-70b-8192",
    temperature=0.5,
    tools=["tool1", "tool2"]
)

builder.save_template("custom", custom_template, "my_template.json")
```

### Adding Custom Tools
```python
async def my_custom_tool(param1: str, param2: int) -> str:
    """Custom tool implementation."""
    return f"Processed {param1} with {param2}"

builder.register_tool("my_tool", my_custom_tool, "Description of my tool")
```

## 🧪 Testing

Run the examples to test the framework:

```bash
# Run basic usage examples
python main.py examples

# Run interactive demo
python main.py demo

# Test specific functionality
python examples/basic_usage.py
python examples/agent_builder_demo.py
```

## 📚 Documentation

For detailed documentation on each component:

- [Agent Builder Guide](docs/agent_builder.md)
- [Tool Development](docs/tools.md)
- [Template Creation](docs/templates.md)
- [API Reference](docs/api.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the Microsoft Agent Framework architecture
- Built with Groq for fast LLM inference
- Uses modern Python async/await patterns

## 🆘 Support

- Create an issue for bug reports
- Join discussions for questions
- Check examples for usage patterns

---

**Built with ❤️ using Groq models and Microsoft Agent Framework principles**

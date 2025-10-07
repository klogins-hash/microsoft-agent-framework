"""Demonstration of the Agent Builder's capabilities."""

import asyncio
import json
from dotenv import load_dotenv

from microsoft_agent_framework import AgentBuilder
from microsoft_agent_framework.tools import WebTools, FileTools, CodeTools

load_dotenv()


async def interactive_agent_builder():
    """Interactive demonstration of agent building capabilities."""
    
    print("🚀 Microsoft Agent Framework - Agent Builder Demo")
    print("=" * 50)
    
    # Initialize builder
    builder = AgentBuilder()
    
    # Register tools
    web_tools = WebTools()
    file_tools = FileTools()
    code_tools = CodeTools()
    
    builder.register_tool("fetch_url", web_tools.fetch_url)
    builder.register_tool("read_file", file_tools.read_file)
    builder.register_tool("write_file", file_tools.write_file)
    builder.register_tool("execute_python", code_tools.execute_python)
    builder.register_tool("create_project", code_tools.create_project_structure)
    
    # Show available templates
    print("\n📋 Available Agent Templates:")
    templates = builder.list_templates()
    for name, description in templates.items():
        print(f"  • {name}: {description}")
    
    print("\n🤖 Master Agent Builder is ready to help!")
    print("Ask me to create agents for specific use cases...\n")
    
    # Example conversations with the master agent
    use_cases = [
        "I need an agent that can help me write and debug Python code",
        "Create an agent for customer service that can handle complaints and inquiries",
        "I want an agent that can analyze data files and create summaries",
        "Build me an agent that can help with project management tasks"
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"🔍 Use Case {i}: {use_case}")
        
        # Get recommendation from master agent
        recommendation = await builder.get_agent_recommendation(use_case)
        print(f"💡 Master Agent Recommendation:\n{recommendation}\n")
        
        # Create an agent based on the use case
        if "code" in use_case.lower():
            agent = builder.create_agent_from_template(
                "code_assistant",
                name=f"Code Helper {i}",
                tools=["execute_python"]
            )
        elif "customer" in use_case.lower():
            agent = builder.create_agent_from_template(
                "customer_support",
                name=f"Support Agent {i}"
            )
        elif "data" in use_case.lower():
            agent = builder.create_agent_from_template(
                "data_analyst",
                name=f"Data Analyst {i}",
                tools=["read_file"]
            )
        else:
            agent = builder.create_custom_agent(
                name=f"Custom Agent {i}",
                instructions=f"You are an AI agent created for: {use_case}",
                tools=["read_file", "write_file"]
            )
        
        # Test the created agent
        test_query = "Hello! Can you tell me what you can help me with?"
        response = await agent.run_async(test_query)
        print(f"🤖 {agent.config.name}: {response}\n")
        print("-" * 50)
    
    # Demonstrate agent customization
    print("\n🛠️  Agent Customization Demo")
    print("Creating a specialized agent from scratch...")
    
    specialized_agent = builder.create_custom_agent(
        name="Documentation Writer",
        instructions="""You are a technical documentation writer. You help create clear, 
        comprehensive documentation for software projects. You can:
        - Write README files
        - Create API documentation
        - Generate code comments
        - Explain complex technical concepts in simple terms
        Always structure your documentation with clear headings and examples.""",
        model="llama3-70b-8192",
        temperature=0.4,
        tools=["write_file", "read_file"]
    )
    
    doc_response = await specialized_agent.run_async(
        "Can you help me write a README file for a Python web scraping project?"
    )
    print(f"📝 Documentation Writer: {doc_response}\n")
    
    # Show agent thread/conversation history
    print("💬 Conversation History:")
    thread = specialized_agent.get_thread()
    for message in thread.get_messages()[-3:]:  # Last 3 messages
        print(f"  {message.role}: {message.content[:100]}...")
    
    await web_tools.close()
    print("\n✅ Agent Builder Demo completed!")


async def save_agent_templates():
    """Demonstrate saving and loading agent templates."""
    
    print("\n💾 Template Management Demo")
    
    builder = AgentBuilder()
    
    # Create a custom template
    from microsoft_agent_framework.core.agent_builder import AgentTemplate
    
    custom_template = AgentTemplate(
        name="API Integration Agent",
        description="Agent specialized in working with REST APIs and webhooks",
        instructions="""You are an API integration specialist. You help users:
        - Make HTTP requests to REST APIs
        - Parse and format API responses
        - Handle authentication and headers
        - Debug API issues
        - Design webhook handlers
        Always provide clear examples and handle errors gracefully.""",
        model="llama3-70b-8192",
        temperature=0.3,
        tools=["fetch_url", "post_json"],
        metadata={"category": "integration", "version": "1.0"}
    )
    
    # Save template
    builder.save_template("api_integration", custom_template, "templates/api_agent.json")
    print("✅ Saved custom template to templates/api_agent.json")
    
    # Create agent from custom template
    api_agent = builder.create_agent_from_template("api_integration", name="API Helper")
    
    response = await api_agent.run_async("How do I make a POST request with authentication headers?")
    print(f"🔌 API Agent: {response}")


if __name__ == "__main__":
    asyncio.run(interactive_agent_builder())
    asyncio.run(save_agent_templates())

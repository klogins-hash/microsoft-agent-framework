"""Basic usage examples for the Microsoft Agent Framework."""

import asyncio
import os
from dotenv import load_dotenv

from microsoft_agent_framework import AgentBuilder, GroqClient
from microsoft_agent_framework.tools import WebTools, FileTools, CodeTools

# Load environment variables
load_dotenv()


async def main():
    """Demonstrate basic agent framework usage."""
    
    # Initialize the agent builder
    builder = AgentBuilder()
    
    # Register some tools
    web_tools = WebTools()
    file_tools = FileTools(base_directory="./workspace")  # Restrict to workspace directory
    code_tools = CodeTools()
    
    builder.register_tool("fetch_url", web_tools.fetch_url, "Fetch content from a URL")
    builder.register_tool("read_file", file_tools.read_file, "Read content from a file")
    builder.register_tool("write_file", file_tools.write_file, "Write content to a file")
    builder.register_tool("execute_python", code_tools.execute_python, "Execute Python code")
    builder.register_tool("validate_syntax", code_tools.validate_python_syntax, "Validate Python syntax")
    
    print("🤖 Microsoft Agent Framework - Basic Usage Examples\n")
    
    # Example 1: Create a customer support agent
    print("1. Creating a Customer Support Agent...")
    support_agent = builder.create_agent_from_template(
        "customer_support",
        name="Support Bot",
        custom_instructions="""You are a helpful customer support agent for a software company. 
        You help users with technical issues, account problems, and general inquiries. 
        Always be polite, professional, and try to provide actionable solutions."""
    )
    
    response = await support_agent.run_async("I'm having trouble logging into my account. Can you help?")
    print(f"Support Agent: {response}\n")
    
    # Example 2: Create a code assistant agent
    print("2. Creating a Code Assistant Agent...")
    code_agent = builder.create_agent_from_template(
        "code_assistant",
        name="Code Helper",
        tools=["execute_python", "validate_syntax"]
    )
    
    response = await code_agent.run_async("Can you write a Python function to calculate fibonacci numbers?")
    print(f"Code Agent: {response}\n")
    
    # Example 3: Create a custom agent
    print("3. Creating a Custom Agent...")
    custom_agent = builder.create_custom_agent(
        name="File Manager Agent",
        instructions="""You are a file management assistant. You help users organize, 
        read, write, and manage files. You can work with text files, JSON files, and 
        directory structures. Always confirm before making changes to files.""",
        tools=["read_file", "write_file"],
        temperature=0.3
    )
    
    response = await custom_agent.run_async("Can you help me create a simple configuration file?")
    print(f"File Manager: {response}\n")
    
    # Example 4: Use the master agent builder
    print("4. Getting recommendations from Master Agent Builder...")
    recommendation = await builder.get_agent_recommendation(
        "I need an agent that can help me analyze data from CSV files and generate reports"
    )
    print(f"Master Builder Recommendation:\n{recommendation}\n")
    
    # Example 5: Streaming response
    print("5. Streaming Response Example...")
    print("Code Agent (streaming): ", end="", flush=True)
    async for update in code_agent.run_streaming_async("Explain what a decorator is in Python"):
        print(update.content, end="", flush=True)
    print("\n")
    
    # Clean up
    await web_tools.close()
    
    print("✅ Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())

"""
MCP Integration Demo for Microsoft Agent Framework

This example demonstrates how to:
1. Create MCP servers from API specifications
2. Build agents with automatic API integration
3. Use agents with MCP-powered tools
4. Manage MCP servers and health monitoring
"""

import asyncio
import json
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from microsoft_agent_framework import AgentBuilder
from microsoft_agent_framework.mcp import APISpecificationParser, get_registry


async def demo_openapi_integration():
    """Demo: Create MCP server from OpenAPI specification."""
    print("🔌 Demo 1: OpenAPI to MCP Server Integration")
    print("=" * 50)
    
    # Initialize agent builder
    agent_builder = AgentBuilder()
    
    # Example OpenAPI spec (GitHub API)
    github_api_url = "https://api.github.com"
    
    try:
        # Create MCP server from GitHub API
        print(f"📡 Creating MCP server from GitHub API: {github_api_url}")
        server_info = await agent_builder.create_mcp_server_from_api(
            api_source=github_api_url,
            api_type="rest_discovery",
            server_type="http",
            server_name="github_api"
        )
        
        print(f"✅ MCP server created: {server_info.name}")
        print(f"   Transport: {server_info.transport_type}")
        print(f"   Status: {server_info.status}")
        print(f"   Capabilities: {len(server_info.capabilities)} endpoints")
        
        return server_info
        
    except Exception as e:
        print(f"❌ Error creating MCP server: {e}")
        return None


async def demo_agent_with_api_integration():
    """Demo: Create agent with automatic API integration."""
    print("\n🤖 Demo 2: Agent with API Integration")
    print("=" * 50)
    
    agent_builder = AgentBuilder()
    
    # Example: Create a GitHub management agent
    api_specs = [
        "https://api.github.com",
        # Could add more APIs here
    ]
    
    try:
        print("🔧 Creating agent with GitHub API integration...")
        agent = await agent_builder.create_agent_with_api_integration(
            name="GitHub Manager",
            api_specs=api_specs,
            instructions="""You are a GitHub management assistant. You help users:
            - Manage repositories
            - Handle issues and pull requests  
            - Monitor repository activity
            - Automate GitHub workflows
            
            Use the GitHub API tools available to you to perform these tasks.""",
            template_name="code_assistant",
            model="llama-3.1-70b-versatile"
        )
        
        print(f"✅ Agent created: {agent.config.name}")
        print(f"   Model: {agent.config.model}")
        print(f"   API Integrations: {len(api_specs)}")
        
        # Test the agent
        print("\n💬 Testing agent with API integration...")
        response = await agent.run_async("List the available GitHub API endpoints you can use")
        print(f"Agent response: {response.content[:200]}...")
        
        return agent
        
    except Exception as e:
        print(f"❌ Error creating agent with API integration: {e}")
        return None


async def demo_mcp_server_management():
    """Demo: MCP server management and monitoring."""
    print("\n🔧 Demo 3: MCP Server Management")
    print("=" * 50)
    
    agent_builder = AgentBuilder()
    
    try:
        # List all MCP servers
        print("📋 Listing all MCP servers...")
        servers = agent_builder.list_mcp_servers()
        print(f"Found {len(servers)} MCP servers:")
        
        for server in servers:
            print(f"  • {server['name']} ({server['transport_type']}) - {server['status']}")
        
        # Health check all servers
        print("\n🏥 Performing health checks...")
        health_results = await agent_builder.health_check_mcp_servers()
        
        healthy_count = sum(1 for status in health_results.values() if status is True)
        total_count = len(health_results)
        
        print(f"Health Status: {healthy_count}/{total_count} servers healthy")
        
        for server_id, is_healthy in health_results.items():
            status = "✅ Healthy" if is_healthy else "❌ Unhealthy" if is_healthy is False else "❓ Unknown"
            print(f"  • {server_id}: {status}")
        
        # Search servers
        print("\n🔍 Searching for API-related servers...")
        search_results = agent_builder.search_mcp_servers("api")
        print(f"Found {len(search_results)} servers matching 'api':")
        
        for result in search_results:
            print(f"  • {result['name']} (relevance: {result['relevance_score']:.2f})")
        
    except Exception as e:
        print(f"❌ Error in server management: {e}")


async def demo_api_discovery():
    """Demo: Automatic API discovery."""
    print("\n🔍 Demo 4: API Discovery")
    print("=" * 50)
    
    agent_builder = AgentBuilder()
    
    # Example domains to discover APIs
    domains = ["jsonplaceholder.typicode.com", "httpbin.org"]
    
    for domain in domains:
        try:
            print(f"🌐 Discovering APIs for domain: {domain}")
            discovered_apis = await agent_builder.discover_apis(domain)
            
            print(f"Found {len(discovered_apis)} API endpoints:")
            for api in discovered_apis:
                print(f"  • {api['url']} - {api.get('type', 'unknown')} ({api['status']})")
            
        except Exception as e:
            print(f"❌ Error discovering APIs for {domain}: {e}")


async def demo_custom_mcp_templates():
    """Demo: Using different MCP templates."""
    print("\n📋 Demo 5: MCP Templates")
    print("=" * 50)
    
    agent_builder = AgentBuilder()
    
    # Example webhook API specification
    webhook_api_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Webhook API",
            "version": "1.0.0",
            "description": "Event-driven webhook API"
        },
        "paths": {
            "/webhooks": {
                "post": {
                    "summary": "Create webhook",
                    "description": "Register a new webhook subscription",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"},
                                        "events": {"type": "array", "items": {"type": "string"}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    try:
        print("🪝 Creating MCP server for webhook API...")
        server_info = await agent_builder.create_mcp_server_from_api(
            api_source=webhook_api_spec,
            api_type="openapi",
            server_type="http",
            server_name="webhook_api"
        )
        
        print(f"✅ Webhook MCP server created: {server_info.name}")
        
        # Create agent specialized for webhook management
        webhook_agent = await agent_builder.create_agent_with_api_integration(
            name="Webhook Manager",
            api_specs=[webhook_api_spec],
            instructions="""You are a webhook management specialist. You help users:
            - Set up webhook subscriptions
            - Manage webhook events
            - Troubleshoot webhook delivery issues
            - Monitor webhook health and performance
            
            Use the webhook API tools to perform these tasks.""",
            template_name="customer_support"
        )
        
        print(f"✅ Webhook agent created: {webhook_agent.config.name}")
        
    except Exception as e:
        print(f"❌ Error with webhook demo: {e}")


async def demo_streaming_api_integration():
    """Demo: Streaming API integration."""
    print("\n📡 Demo 6: Streaming API Integration")
    print("=" * 50)
    
    agent_builder = AgentBuilder()
    
    # Example streaming API specification
    streaming_api_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Real-time Data Stream API",
            "version": "1.0.0"
        },
        "paths": {
            "/stream/data": {
                "get": {
                    "summary": "Real-time data stream",
                    "description": "Subscribe to real-time data updates",
                    "parameters": [
                        {
                            "name": "stream_type",
                            "in": "query",
                            "schema": {"type": "string", "enum": ["metrics", "logs", "events"]}
                        }
                    ]
                }
            }
        }
    }
    
    try:
        print("📊 Creating MCP server for streaming API...")
        server_info = await agent_builder.create_mcp_server_from_api(
            api_source=streaming_api_spec,
            api_type="openapi",
            server_type="websocket",  # Use WebSocket for streaming
            server_name="streaming_api"
        )
        
        print(f"✅ Streaming MCP server created: {server_info.name}")
        print(f"   Transport: {server_info.transport_type} (for real-time data)")
        
    except Exception as e:
        print(f"❌ Error with streaming demo: {e}")


async def main():
    """Run all MCP integration demos."""
    print("🚀 Microsoft Agent Framework - MCP Integration Demo")
    print("=" * 60)
    print("This demo showcases the MCP (Model Context Protocol) integration")
    print("that allows agents to automatically connect to any API.\n")
    
    try:
        # Run all demos
        await demo_openapi_integration()
        await demo_agent_with_api_integration()
        await demo_mcp_server_management()
        await demo_api_discovery()
        await demo_custom_mcp_templates()
        await demo_streaming_api_integration()
        
        print("\n🎉 All demos completed successfully!")
        print("\n📚 What you can do next:")
        print("• Deploy your MCP servers to production")
        print("• Create agents for your specific APIs")
        print("• Set up monitoring and health checks")
        print("• Build custom MCP templates for your use cases")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up resources...")
        # Note: In a real application, you'd want to clean up MCP connections
        print("✅ Cleanup completed")


if __name__ == "__main__":
    asyncio.run(main())

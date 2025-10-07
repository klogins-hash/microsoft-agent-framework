"""
Team Orchestrator Demo for Microsoft Agent Framework

This example demonstrates how to use the Team Orchestrator as a central
communication hub that manages and coordinates specialized agents.

The Team Orchestrator acts as your single point of contact - you communicate
with it, and it delegates tasks to the appropriate team members.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from microsoft_agent_framework import TeamOrchestrator


async def demo_basic_team_communication():
    """Demo: Basic communication with the team orchestrator."""
    print("👥 Demo 1: Basic Team Communication")
    print("=" * 50)
    
    # Initialize team orchestrator
    team = TeamOrchestrator()
    
    # Wait for team initialization
    await asyncio.sleep(2)
    
    print("🗣️ You can now communicate with the team through one central orchestrator!")
    print("The Team Lead will analyze your requests and assign them to the right specialists.\n")
    
    # Example requests that will be delegated to different team members
    requests = [
        "Write a Python function to calculate fibonacci numbers",
        "Help me troubleshoot why my API is returning 500 errors",
        "Analyze this sales data and create a summary report",
        "Create documentation for our new user onboarding process"
    ]
    
    for i, request in enumerate(requests, 1):
        print(f"📝 Request {i}: {request}")
        try:
            response = await team.chat(request)
            print(f"🤖 Team Response: {response[:200]}...")
            print(f"   (Response truncated for demo)\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        # Small delay between requests
        await asyncio.sleep(1)


async def demo_team_status_monitoring():
    """Demo: Monitor team status and member availability."""
    print("📊 Demo 2: Team Status Monitoring")
    print("=" * 50)
    
    team = TeamOrchestrator()
    await asyncio.sleep(2)  # Wait for initialization
    
    try:
        # Get team status
        status = await team.get_team_status()
        
        print(f"👥 Team Overview:")
        print(f"   Total Members: {status['total_members']}")
        print(f"   Available: {status['available_members']}")
        print(f"   Active Tasks: {status['active_tasks']}\n")
        
        print("👤 Team Members:")
        for role, member_info in status['team_members'].items():
            availability = "✅ Available" if member_info['available'] else f"🔄 Busy: {member_info['current_task']}"
            specialties = ", ".join(member_info['specialties'])
            print(f"   • {role.replace('_', ' ').title()}")
            print(f"     Specialties: {specialties}")
            print(f"     Status: {availability}")
            print(f"     Tasks Completed: {member_info['tasks_completed']}\n")
            
    except Exception as e:
        print(f"❌ Error getting team status: {e}")


async def demo_adding_specialized_team_members():
    """Demo: Add specialized team members for specific needs."""
    print("➕ Demo 3: Adding Specialized Team Members")
    print("=" * 50)
    
    team = TeamOrchestrator()
    await asyncio.sleep(2)
    
    try:
        # Add a specialized security expert
        print("🔒 Adding Security Specialist to the team...")
        await team.add_team_member(
            role="security_specialist",
            specialties=["cybersecurity", "penetration_testing", "vulnerability_assessment", "compliance"],
            custom_instructions="""You are a Cybersecurity Specialist. You excel at:
            - Security vulnerability assessments
            - Penetration testing guidance
            - Compliance and regulatory requirements
            - Security best practices and recommendations
            - Incident response planning
            
            Always prioritize security and provide actionable recommendations."""
        )
        
        # Add a DevOps engineer
        print("⚙️ Adding DevOps Engineer to the team...")
        await team.add_team_member(
            role="devops_engineer", 
            specialties=["infrastructure", "deployment", "monitoring", "automation", "cloud_platforms"],
            custom_instructions="""You are a DevOps Engineer. You excel at:
            - Infrastructure as Code (IaC)
            - CI/CD pipeline design and implementation
            - Cloud platform management (AWS, Azure, GCP)
            - Monitoring and alerting setup
            - Container orchestration and deployment
            
            Focus on automation, scalability, and reliability."""
        )
        
        print("✅ New team members added successfully!")
        
        # Test with specialized requests
        print("\n🧪 Testing specialized requests...")
        
        security_request = "Review our API security and recommend improvements"
        print(f"🔒 Security Request: {security_request}")
        security_response = await team.chat(security_request)
        print(f"🤖 Team Response: {security_response[:150]}...\n")
        
        devops_request = "Help me set up a CI/CD pipeline for our Python application"
        print(f"⚙️ DevOps Request: {devops_request}")
        devops_response = await team.chat(devops_request)
        print(f"🤖 Team Response: {devops_response[:150]}...\n")
        
    except Exception as e:
        print(f"❌ Error adding team members: {e}")


async def demo_api_integration_with_team():
    """Demo: Enhance team members with API integration capabilities."""
    print("🔌 Demo 4: API Integration with Team Members")
    print("=" * 50)
    
    team = TeamOrchestrator()
    await asyncio.sleep(2)
    
    try:
        # Add a team member with API integration
        print("📡 Adding API Integration Specialist with GitHub API access...")
        await team.add_team_member(
            role="github_specialist",
            specialties=["github_management", "repository_operations", "issue_tracking", "pull_requests"],
            custom_instructions="""You are a GitHub Management Specialist. You help with:
            - Repository management and operations
            - Issue tracking and resolution
            - Pull request reviews and management
            - GitHub workflow automation
            - Team collaboration on GitHub
            
            Use your GitHub API tools to perform these tasks efficiently.""",
            api_specs=["https://api.github.com"]  # This would create MCP integration
        )
        
        print("✅ GitHub specialist added with API integration!")
        
        # Test API-integrated request
        print("\n🧪 Testing API-integrated request...")
        github_request = "Help me understand how to manage GitHub repositories programmatically"
        print(f"📡 GitHub Request: {github_request}")
        
        response = await team.chat(github_request)
        print(f"🤖 Team Response: {response[:200]}...")
        
    except Exception as e:
        print(f"❌ Error with API integration demo: {e}")


async def demo_complex_multi_step_coordination():
    """Demo: Complex request requiring multiple team members."""
    print("🎯 Demo 5: Complex Multi-Step Coordination")
    print("=" * 50)
    
    team = TeamOrchestrator()
    await asyncio.sleep(2)
    
    try:
        # Complex request that requires multiple specialists
        complex_request = """
        I need to build a complete web application that:
        1. Has a Python FastAPI backend with user authentication
        2. Connects to a PostgreSQL database
        3. Has proper security measures implemented
        4. Includes comprehensive documentation
        5. Has a CI/CD pipeline for deployment
        
        Can you help me plan and coordinate this project?
        """
        
        print("🎯 Complex Multi-Team Request:")
        print(complex_request)
        print("\n🤖 Team Orchestrator analyzing and coordinating...")
        
        response = await team.chat(complex_request)
        print(f"📋 Coordinated Team Response:")
        print(response)
        
    except Exception as e:
        print(f"❌ Error with complex coordination: {e}")


async def demo_team_communication_patterns():
    """Demo: Different communication patterns with the team."""
    print("💬 Demo 6: Team Communication Patterns")
    print("=" * 50)
    
    team = TeamOrchestrator()
    await asyncio.sleep(2)
    
    # Different types of requests to show delegation patterns
    communication_examples = [
        {
            "type": "Technical Question",
            "request": "What's the difference between async and sync in Python?",
            "expected_delegate": "Code Assistant"
        },
        {
            "type": "Data Analysis",
            "request": "How can I analyze customer churn in my dataset?",
            "expected_delegate": "Data Analyst"
        },
        {
            "type": "Customer Issue",
            "request": "A user is having trouble logging into their account",
            "expected_delegate": "Customer Support"
        },
        {
            "type": "Content Creation",
            "request": "Write a blog post about the benefits of AI automation",
            "expected_delegate": "Content Creator"
        },
        {
            "type": "API Integration",
            "request": "How do I connect to the Stripe API for payments?",
            "expected_delegate": "API Integrator"
        }
    ]
    
    for example in communication_examples:
        print(f"📝 {example['type']}: {example['request']}")
        print(f"🎯 Expected to delegate to: {example['expected_delegate']}")
        
        try:
            response = await team.chat(example['request'])
            print(f"🤖 Response: {response[:100]}...")
            print("✅ Request handled successfully\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        await asyncio.sleep(0.5)


async def main():
    """Run all team orchestrator demos."""
    print("👥 Microsoft Agent Framework - Team Orchestrator Demo")
    print("=" * 60)
    print("This demo shows how to use a central Team Orchestrator to manage")
    print("and coordinate communication with specialized AI agents.\n")
    
    print("🎯 Key Benefits:")
    print("• Single point of communication - talk to one Team Lead")
    print("• Automatic task delegation to the right specialists")
    print("• Coordinated multi-agent workflows")
    print("• Team member management and monitoring")
    print("• API integration capabilities for any team member\n")
    
    try:
        # Run all demos
        await demo_basic_team_communication()
        await demo_team_status_monitoring()
        await demo_adding_specialized_team_members()
        await demo_api_integration_with_team()
        await demo_complex_multi_step_coordination()
        await demo_team_communication_patterns()
        
        print("🎉 All Team Orchestrator demos completed!")
        print("\n📚 What you can do next:")
        print("• Use POST /team/chat for all your communication needs")
        print("• Monitor team status with GET /team/status")
        print("• Add specialized team members with POST /team/add-member")
        print("• Enhance members with APIs using POST /team/enhance-member")
        print("• Let the Team Lead coordinate complex multi-step tasks")
        
        print("\n💡 Pro Tips:")
        print("• The Team Lead automatically analyzes requests and delegates")
        print("• Complex requests are broken down and coordinated across team members")
        print("• Each team member has specialized knowledge and capabilities")
        print("• API integrations can be added to any team member")
        print("• The orchestrator provides unified responses from multiple specialists")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
    
    finally:
        print("\n🧹 Demo completed - Team Orchestrator ready for use!")


if __name__ == "__main__":
    asyncio.run(main())

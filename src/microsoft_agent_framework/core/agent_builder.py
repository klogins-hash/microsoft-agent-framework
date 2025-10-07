"""Agent builder for creating and managing Microsoft agents using Groq models."""

from typing import Dict, List, Any, Optional, Type, Callable
from pydantic import BaseModel
import json
import yaml
from pathlib import Path

from .base_agent import BaseAgent, ChatCompletionAgent, AgentConfig
from .groq_client import GroqClient, GroqConfig
from .context_provider import ContextProvider, InMemoryContextProvider, FileContextProvider
from .agent_thread import AgentThread


class AgentTemplate(BaseModel):
    """Template for creating agents."""
    name: str
    description: str
    instructions: str
    model: str = "llama3-70b-8192"
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: List[str] = []
    context_type: str = "memory"  # "memory", "file"
    metadata: Dict[str, Any] = {}


class AgentBlueprint(BaseModel):
    """Blueprint for a specific agent type."""
    template: AgentTemplate
    tools: Dict[str, Dict[str, Any]] = {}
    middleware: List[str] = []
    examples: List[Dict[str, str]] = []


class AgentBuilder:
    """Expert agent builder for creating Microsoft agents."""
    
    def __init__(self, groq_client: Optional[GroqClient] = None):
        """Initialize the agent builder."""
        self.groq_client = groq_client or GroqClient()
        self.templates: Dict[str, AgentTemplate] = {}
        self.blueprints: Dict[str, AgentBlueprint] = {}
        self.tools_registry: Dict[str, Callable] = {}
        self.middleware_registry: Dict[str, Callable] = {}
        
        # Load built-in templates
        self._load_builtin_templates()
        
        # Create the master agent builder agent
        self.master_agent = self._create_master_agent()
    
    def _load_builtin_templates(self):
        """Load built-in agent templates."""
        
        # Customer Support Agent
        self.templates["customer_support"] = AgentTemplate(
            name="Customer Support Agent",
            description="AI agent specialized in customer support and service",
            instructions="""You are a professional customer support agent. You help customers with their inquiries, 
            resolve issues, and provide excellent service. You are patient, empathetic, and solution-oriented. 
            Always maintain a friendly and professional tone.""",
            model="llama3-70b-8192",
            temperature=0.3,
            tools=["search_knowledge_base", "create_ticket", "escalate_issue"]
        )
        
        # Code Assistant Agent
        self.templates["code_assistant"] = AgentTemplate(
            name="Code Assistant Agent",
            description="AI agent specialized in code generation, debugging, and development assistance",
            instructions="""You are an expert software developer and code assistant. You help with code generation, 
            debugging, code review, and technical problem-solving. You provide clear explanations, follow best practices, 
            and write clean, efficient code. You support multiple programming languages and frameworks.""",
            model="llama3-70b-8192",
            temperature=0.2,
            tools=["execute_code", "search_documentation", "analyze_code"]
        )
        
        # Data Analyst Agent
        self.templates["data_analyst"] = AgentTemplate(
            name="Data Analyst Agent",
            description="AI agent specialized in data analysis, visualization, and insights",
            instructions="""You are a skilled data analyst. You help analyze data, create visualizations, 
            generate insights, and provide data-driven recommendations. You work with various data formats 
            and use statistical methods to uncover patterns and trends.""",
            model="llama3-70b-8192",
            temperature=0.4,
            tools=["analyze_data", "create_chart", "generate_report"]
        )
        
        # Microsoft Teams Bot Agent
        self.templates["teams_bot"] = AgentTemplate(
            name="Microsoft Teams Bot Agent",
            description="AI agent designed for Microsoft Teams integration",
            instructions="""You are a Microsoft Teams bot assistant. You help team members with productivity, 
            scheduling, information retrieval, and collaboration. You can interact with Microsoft Graph API 
            to access calendar, files, and team information. Keep responses concise and actionable.""",
            model="llama3-70b-8192",
            temperature=0.5,
            tools=["graph_api_call", "schedule_meeting", "search_files"]
        )
        
        # Agent Builder Agent (Meta-agent)
        self.templates["agent_builder"] = AgentTemplate(
            name="Agent Builder Agent",
            description="Meta-agent specialized in creating and configuring other agents",
            instructions="""You are an expert agent builder and architect. You specialize in creating, configuring, 
            and optimizing AI agents for specific use cases. You understand agent design patterns, prompt engineering, 
            tool integration, and workflow orchestration. You help users design the perfect agent for their needs.""",
            model="llama3-70b-8192",
            temperature=0.6,
            tools=["create_agent", "configure_tools", "test_agent", "deploy_agent"]
        )
    
    def _create_master_agent(self) -> ChatCompletionAgent:
        """Create the master agent builder agent."""
        template = self.templates["agent_builder"]
        
        enhanced_instructions = f"""{template.instructions}

Available Agent Templates:
{self._get_templates_description()}

You can help users:
1. Choose the right agent template for their use case
2. Customize agent instructions and parameters
3. Add appropriate tools and integrations
4. Configure Microsoft-specific features (Teams, Graph API, etc.)
5. Test and validate agent configurations
6. Deploy agents to production environments

When creating agents, consider:
- The specific use case and requirements
- The target audience and interaction patterns
- Required integrations and data sources
- Performance and scalability needs
- Security and compliance requirements
"""
        
        return ChatCompletionAgent(
            instructions=enhanced_instructions,
            name="Master Agent Builder",
            groq_client=self.groq_client,
            model=template.model,
            temperature=template.temperature,
            max_tokens=template.max_tokens
        )
    
    def _get_templates_description(self) -> str:
        """Get description of available templates."""
        descriptions = []
        for name, template in self.templates.items():
            descriptions.append(f"- {name}: {template.description}")
        return "\n".join(descriptions)
    
    def register_tool(self, name: str, func: Callable, description: str = "") -> None:
        """Register a tool function."""
        self.tools_registry[name] = func
        func._tool_metadata = {"name": name, "description": description}
    
    def register_middleware(self, name: str, func: Callable) -> None:
        """Register a middleware function."""
        self.middleware_registry[name] = func
    
    def create_agent_from_template(
        self,
        template_name: str,
        name: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        **kwargs
    ) -> ChatCompletionAgent:
        """Create an agent from a template."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found. Available: {list(self.templates.keys())}")
        
        template = self.templates[template_name]
        
        # Use custom name or template name
        agent_name = name or template.name
        
        # Use custom instructions or template instructions
        instructions = custom_instructions or template.instructions
        
        # Create context provider
        context_provider = self._create_context_provider(template.context_type, agent_name)
        
        # Create agent
        agent = ChatCompletionAgent(
            instructions=instructions,
            name=agent_name,
            groq_client=self.groq_client,
            model=kwargs.get("model", template.model),
            temperature=kwargs.get("temperature", template.temperature),
            max_tokens=kwargs.get("max_tokens", template.max_tokens),
            context_provider=context_provider
        )
        
        # Add tools
        for tool_name in template.tools:
            if tool_name in self.tools_registry:
                agent.add_tool(tool_name, self.tools_registry[tool_name])
        
        return agent
    
    def create_custom_agent(
        self,
        name: str,
        instructions: str,
        model: str = "llama3-70b-8192",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[str]] = None,
        context_type: str = "memory"
    ) -> ChatCompletionAgent:
        """Create a custom agent with specific configuration."""
        
        # Create context provider
        context_provider = self._create_context_provider(context_type, name)
        
        # Create agent
        agent = ChatCompletionAgent(
            instructions=instructions,
            name=name,
            groq_client=self.groq_client,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            context_provider=context_provider
        )
        
        # Add tools
        if tools:
            for tool_name in tools:
                if tool_name in self.tools_registry:
                    agent.add_tool(tool_name, self.tools_registry[tool_name])
        
        return agent
    
    def _create_context_provider(self, context_type: str, agent_name: str) -> ContextProvider:
        """Create appropriate context provider."""
        if context_type == "file":
            context_file = f"contexts/{agent_name.lower().replace(' ', '_')}_context.json"
            Path(context_file).parent.mkdir(parents=True, exist_ok=True)
            return FileContextProvider(context_file)
        else:
            return InMemoryContextProvider()
    
    async def build_agent_from_description(self, description: str) -> ChatCompletionAgent:
        """Use the master agent to build an agent from natural language description."""
        
        prompt = f"""Based on this description, recommend the best agent configuration:

Description: {description}

Please provide:
1. The most suitable template (from available templates)
2. Any customizations needed for instructions
3. Recommended tools and integrations
4. Suggested model parameters (temperature, max_tokens)
5. Any Microsoft-specific integrations needed

Format your response as a structured recommendation."""
        
        response = await self.master_agent.run_async(prompt)
        
        # For now, return a basic agent - in a full implementation, 
        # you would parse the response and create the agent accordingly
        return self.create_custom_agent(
            name="Custom Agent",
            instructions=f"You are an AI agent created for: {description}",
            temperature=0.7
        )
    
    def save_template(self, name: str, template: AgentTemplate, file_path: Optional[str] = None) -> None:
        """Save an agent template to file."""
        self.templates[name] = template
        
        if file_path:
            template_data = template.model_dump()
            
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                with open(file_path, 'w') as f:
                    yaml.dump(template_data, f, default_flow_style=False)
            else:
                with open(file_path, 'w') as f:
                    json.dump(template_data, f, indent=2)
    
    def load_template(self, file_path: str) -> AgentTemplate:
        """Load an agent template from file."""
        with open(file_path, 'r') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        template = AgentTemplate(**data)
        self.templates[template.name.lower().replace(' ', '_')] = template
        return template
    
    def list_templates(self) -> Dict[str, str]:
        """List available agent templates."""
        return {name: template.description for name, template in self.templates.items()}
    
    def get_template(self, name: str) -> Optional[AgentTemplate]:
        """Get a specific template."""
        return self.templates.get(name)
    
    async def get_agent_recommendation(self, use_case: str) -> str:
        """Get agent recommendations from the master agent."""
        prompt = f"""A user wants to create an agent for this use case: {use_case}

Please recommend:
1. The best template to use
2. Any customizations needed
3. Required tools and integrations
4. Microsoft-specific features that would be helpful
5. Configuration parameters

Provide a clear, actionable recommendation."""
        
        response = await self.master_agent.run_async(prompt)
        return response.content

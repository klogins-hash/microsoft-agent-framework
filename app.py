"""FastAPI web application for the Microsoft Agent Framework."""

import os
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from contextlib import asynccontextmanager

from src.microsoft_agent_framework import AgentBuilder
from src.microsoft_agent_framework.database import DatabaseManager, get_database, init_database
from src.microsoft_agent_framework.database.models import Agent as AgentModel, Conversation, Message
from src.microsoft_agent_framework.tools import WebTools, FileTools, CodeTools


# Pydantic models for API
class CreateAgentRequest(BaseModel):
    name: str
    template_name: Optional[str] = None
    instructions: Optional[str] = None
    model: Optional[str] = "llama3-70b-8192"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4096
    tools: Optional[List[str]] = []


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_id: str


# Global variables
agent_builder: Optional[AgentBuilder] = None
web_tools: Optional[WebTools] = None
file_tools: Optional[FileTools] = None
code_tools: Optional[CodeTools] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global agent_builder, web_tools, file_tools, code_tools
    
    # Startup
    print("🚀 Starting Microsoft Agent Framework...")
    
    # Initialize database
    await init_database()
    print("✅ Database initialized")
    
    # Initialize agent builder and tools
    agent_builder = AgentBuilder()
    web_tools = WebTools()
    file_tools = FileTools()
    code_tools = CodeTools()
    
    # Register tools
    agent_builder.register_tool("fetch_url", web_tools.fetch_url, "Fetch content from a URL")
    agent_builder.register_tool("read_file", file_tools.read_file, "Read content from a file")
    agent_builder.register_tool("write_file", file_tools.write_file, "Write content to a file")
    agent_builder.register_tool("execute_python", code_tools.execute_python, "Execute Python code")
    agent_builder.register_tool("validate_syntax", code_tools.validate_python_syntax, "Validate Python syntax")
    
    print("✅ Agent builder and tools initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Microsoft Agent Framework...")
    if web_tools:
        await web_tools.close()
    
    db = get_database()
    await db.close()
    print("✅ Cleanup completed")


# Create FastAPI app
app = FastAPI(
    title="Microsoft Agent Framework API",
    description="API for building and managing AI agents with Groq models",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Microsoft Agent Framework API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.get("/templates")
async def list_templates():
    """List available agent templates."""
    if not agent_builder:
        raise HTTPException(status_code=500, detail="Agent builder not initialized")
    
    templates = agent_builder.list_templates()
    return {"templates": templates}


@app.post("/agents")
async def create_agent(request: CreateAgentRequest):
    """Create a new agent."""
    if not agent_builder:
        raise HTTPException(status_code=500, detail="Agent builder not initialized")
    
    try:
        # Create agent using builder
        if request.template_name:
            agent = agent_builder.create_agent_from_template(
                template_name=request.template_name,
                name=request.name,
                custom_instructions=request.instructions,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            if not request.instructions:
                raise HTTPException(status_code=400, detail="Instructions required for custom agent")
            
            agent = agent_builder.create_custom_agent(
                name=request.name,
                instructions=request.instructions,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=request.tools
            )
        
        # Save agent to database
        db = get_database()
        async with db.get_session() as session:
            db_agent = AgentModel(
                name=agent.config.name,
                template_name=request.template_name,
                instructions=agent.config.instructions,
                model=agent.config.model or "llama3-70b-8192",
                temperature=str(agent.config.temperature or 0.7),
                max_tokens=agent.config.max_tokens or 4096,
                tools=request.tools or [],
                metadata=agent.config.metadata
            )
            session.add(db_agent)
            await session.flush()
            
            return {
                "agent_id": db_agent.id,
                "name": db_agent.name,
                "template_name": db_agent.template_name,
                "message": "Agent created successfully"
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all agents."""
    db = get_database()
    async with db.get_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(AgentModel).where(AgentModel.is_active == True)
        )
        agents = result.scalars().all()
        
        return {
            "agents": [agent.to_dict() for agent in agents]
        }


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    db = get_database()
    async with db.get_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return agent.to_dict()


@app.post("/agents/{agent_id}/chat")
async def chat_with_agent(agent_id: str, request: ChatRequest):
    """Chat with an agent."""
    if not agent_builder:
        raise HTTPException(status_code=500, detail="Agent builder not initialized")
    
    db = get_database()
    
    try:
        async with db.get_session() as session:
            from sqlalchemy import select
            
            # Get agent from database
            result = await session.execute(
                select(AgentModel).where(AgentModel.id == agent_id)
            )
            db_agent = result.scalar_one_or_none()
            
            if not db_agent:
                raise HTTPException(status_code=404, detail="Agent not found")
            
            # Create agent instance
            agent = agent_builder.create_custom_agent(
                name=db_agent.name,
                instructions=db_agent.instructions,
                model=db_agent.model,
                temperature=float(db_agent.temperature),
                max_tokens=db_agent.max_tokens,
                tools=db_agent.tools
            )
            
            # Get or create conversation
            conversation_id = request.conversation_id
            if conversation_id:
                result = await session.execute(
                    select(Conversation).where(Conversation.id == conversation_id)
                )
                conversation = result.scalar_one_or_none()
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            else:
                conversation = Conversation(
                    agent_id=agent_id,
                    title=f"Chat with {db_agent.name}"
                )
                session.add(conversation)
                await session.flush()
                conversation_id = conversation.id
            
            # Add user message to database
            user_message = Message(
                conversation_id=conversation_id,
                role="user",
                content=request.message
            )
            session.add(user_message)
            
            # Get agent response
            response = await agent.run_async(request.message)
            
            # Add assistant message to database
            assistant_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=response.content
            )
            session.add(assistant_message)
            
            return ChatResponse(
                response=response.content,
                conversation_id=conversation_id,
                agent_id=agent_id
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_id}/chat/stream")
async def stream_chat_with_agent(agent_id: str, request: ChatRequest):
    """Stream chat with an agent."""
    if not agent_builder:
        raise HTTPException(status_code=500, detail="Agent builder not initialized")
    
    async def generate_response():
        db = get_database()
        
        try:
            async with db.get_session() as session:
                from sqlalchemy import select
                
                # Get agent from database
                result = await session.execute(
                    select(AgentModel).where(AgentModel.id == agent_id)
                )
                db_agent = result.scalar_one_or_none()
                
                if not db_agent:
                    yield f"data: {json.dumps({'error': 'Agent not found'})}\n\n"
                    return
                
                # Create agent instance
                agent = agent_builder.create_custom_agent(
                    name=db_agent.name,
                    instructions=db_agent.instructions,
                    model=db_agent.model,
                    temperature=float(db_agent.temperature),
                    max_tokens=db_agent.max_tokens,
                    tools=db_agent.tools
                )
                
                # Stream response
                full_response = ""
                async for update in agent.run_streaming_async(request.message):
                    if not update.is_complete:
                        full_response += update.content
                        yield f"data: {json.dumps({'content': update.content, 'done': False})}\n\n"
                    else:
                        yield f"data: {json.dumps({'content': '', 'done': True, 'full_response': full_response})}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    db = get_database()
    async with db.get_session() as session:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        
        result = await session.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation": conversation.to_dict(),
            "messages": [msg.to_dict() for msg in conversation.messages]
        }


@app.post("/build-agent")
async def build_agent_from_description(description: str):
    """Build an agent from natural language description."""
    if not agent_builder:
        raise HTTPException(status_code=500, detail="Agent builder not initialized")
    
    try:
        recommendation = await agent_builder.get_agent_recommendation(description)
        return {
            "recommendation": recommendation,
            "description": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

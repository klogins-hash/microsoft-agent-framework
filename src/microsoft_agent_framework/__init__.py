"""
Microsoft Agent Framework - A framework for building Microsoft-integrated agents using Groq models.
"""

__version__ = "0.1.0"
__author__ = "Microsoft Agent Framework Team"

from .core.base_agent import BaseAgent
from .core.agent_builder import AgentBuilder
from .core.groq_client import GroqClient

__all__ = ["BaseAgent", "AgentBuilder", "GroqClient"]

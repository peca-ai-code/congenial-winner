"""
Configuration module for the Chainlit Gynecology Chatbot app.
This module loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Load environment variables from .env file
load_dotenv()

class LLMConfig(BaseModel):
    """Configuration for a single LLM model."""
    name: str
    api_key: str
    model_id: str
    max_tokens: int = 500
    temperature: float = 0.7
    display_name: str
    color: str  # Color for UI display

class AppConfig(BaseModel):
    """Main application configuration."""
    app_name: str = "Gynecology Chatbot"
    description: str = "Virtual gynecology assistant powered by multiple AI models"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    llms: Dict[str, LLMConfig] = {
        "openai": LLMConfig(
            name="openai",
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model_id=os.getenv("OPENAI_MODEL", "gpt-4"),
            display_name="ChatGPT",
            color="#10a37f"  # OpenAI green
        ),
        "gemini": LLMConfig(
            name="gemini",
            api_key=os.getenv("GEMINI_API_KEY", ""),
            model_id=os.getenv("GEMINI_MODEL", "gemini-pro"),
            display_name="Gemini",
            color="#1a73e8"  # Google blue
        ),
        "grok": LLMConfig(
            name="grok",
            api_key=os.getenv("GROK_API_KEY", ""),
            model_id=os.getenv("GROK_MODEL", "grok-1"),
            display_name="Grok",
            color="#ff0000"  # Xitter red-ish
        )
    }
    
    @property
    def system_prompt(self) -> str:
        """Returns the system prompt for gynecology assistant."""
        return (
            "You are a virtual gynecology assistant designed to provide support, information, "
            "and reassurance to users with gynecological concerns. Provide clear, accurate, "
            "and concise information. Emphasize when symptoms are likely benign, but always "
            "recommend consulting a healthcare provider for proper diagnosis when appropriate. "
            "Do not provide definitive diagnoses. Be supportive, informative, and reassuring."
        )

# Create global config instance
config = AppConfig()
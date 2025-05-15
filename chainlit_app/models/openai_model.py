"""
OpenAI (ChatGPT) model integration.
"""

import openai
from typing import List, Dict, Any, Optional
import asyncio
from ..config import config

class OpenAIModel:
    """
    Wrapper for OpenAI's GPT model API.
    """
    
    def __init__(self):
        """Initialize the OpenAI API with API key from config."""
        self.api_key = config.llms["openai"].api_key
        self.model = config.llms["openai"].model_id
        self.max_tokens = config.llms["openai"].max_tokens
        self.temperature = config.llms["openai"].temperature
        self.name = config.llms["openai"].display_name
        
        # Set the API key
        openai.api_key = self.api_key
    
    async def generate_response(self, 
                               user_message: str, 
                               chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response from the OpenAI model.
        
        Args:
            user_message: The user's message to respond to
            chat_history: Optional list of previous messages for context
            
        Returns:
            The model's response text
        """
        if not self.api_key:
            return "Error: OpenAI API key not configured."
        
        try:
            # Create the messages array with system prompt
            messages = [{"role": "system", "content": config.system_prompt}]
            
            # Add chat history if provided
            if chat_history:
                messages.extend(chat_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call the OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract and return the response text
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response from ChatGPT: {str(e)}"
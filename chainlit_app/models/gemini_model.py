"""
Google Gemini model integration.
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import asyncio
from config import config

class GeminiModel:
    """
    Wrapper for Google's Gemini API.
    """
    
    def __init__(self):
        """Initialize the Gemini API with API key from config."""
        self.api_key = config.llms["gemini"].api_key
        self.model = config.llms["gemini"].model_id
        self.max_tokens = config.llms["gemini"].max_tokens
        self.temperature = config.llms["gemini"].temperature
        self.name = config.llms["gemini"].display_name
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
    
    async def generate_response(self, 
                               user_message: str, 
                               chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response from the Gemini model.
        
        Args:
            user_message: The user's message to respond to
            chat_history: Optional list of previous messages for context
            
        Returns:
            The model's response text
        """
        if not self.api_key:
            return "Error: Gemini API key not configured."
        
        try:
            # Format the history for Gemini
            formatted_history = []
            
            # Add system instruction first
            formatted_history.append({
                "role": "user",
                "parts": [{
                    "text": config.system_prompt
                }]
            })
            
            # Add previous messages if any
            if chat_history:
                for msg in chat_history:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_history.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
            
            # Add current user message
            formatted_history.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })
            
            # Use a synchronous call in an executor to make it async-compatible
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._generate_gemini_response,
                formatted_history
            )
            
            return response
            
        except Exception as e:
            return f"Error generating response from Gemini: {str(e)}"
    
    def _generate_gemini_response(self, formatted_history):
        """Helper method to make the synchronous Gemini API call."""
        # Initialize the Gemini model
        generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens,
        }
        
        model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config
        )
        
        # Generate the response
        response = model.generate_content(
            formatted_history
        )
        
        # Extract and return the text
        return response.text
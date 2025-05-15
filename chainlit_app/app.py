"""
Main Chainlit application for the Virtual Gynecology Chatbot.

This app allows users to interact with multiple AI models (ChatGPT, Gemini, and Grok)
and provides a side-by-side comparison of their responses.
"""

import chainlit as cl
import asyncio
from typing import Dict, List, Any
import os
import time

# Import local modules
from config import config
from models import OpenAIModel, GeminiModel, GrokModel
from components import (
    create_comparison_element, 
    create_css_element,
    get_gynecology_system_prompt
)

# Initialize AI models
openai_model = OpenAIModel()
gemini_model = GeminiModel()
grok_model = GrokModel()

# Store chat histories for each user session
chat_histories = {}

@cl.on_chat_start
async def on_chat_start():
    """
    Initialize the chat session when a user starts a new chat.
    """
    # Set the chat title
    await cl.Message(
        content="Virtual Gynecology Assistant",
        author="System"
    ).send()
    
    # Initialize empty chat history for this session
    chat_histories[cl.user_session.id] = []
    
    # Add the CSS styles for comparison view
    css_element = await create_css_element()
    await cl.Message(
        content="Welcome to the Virtual Gynecology Assistant. How can I help you today?",
        author="Assistant",
        elements=[css_element]
    ).send()
    
    # Create settings for the chat
    await cl.ChatSettings(
        [
            cl.switch(id="show_comparison", label="Show Side-by-Side Comparison", initial=True),
            cl.select(
                id="primary_model",
                label="Primary Response Model",
                values=["ChatGPT", "Gemini", "Grok"],
                initial="ChatGPT"
            )
        ]
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Process user messages and generate responses from multiple AI models.
    """
    # Get user message content
    user_input = message.content
    
    # Get chat settings
    settings = cl.user_session.get("settings", {})
    show_comparison = settings.get("show_comparison", True)
    primary_model = settings.get("primary_model", "ChatGPT")
    
    # Add user message to chat history
    if cl.user_session.id not in chat_histories:
        chat_histories[cl.user_session.id] = []
    
    # Send a thinking message
    thinking_msg = cl.Message(content="", author="Assistant")
    await thinking_msg.send()
    
    try:
        # Update thinking message with loading indicators
        await thinking_msg.stream_token("Generating responses from multiple AI models...\n\n")
        
        # Generate responses from all models concurrently
        tasks = [
            openai_model.generate_response(user_input, chat_histories[cl.user_session.id]),
            gemini_model.generate_response(user_input, chat_histories[cl.user_session.id]),
            grok_model.generate_response(user_input, chat_histories[cl.user_session.id])
        ]
        
        # Wait for all responses
        responses = await asyncio.gather(*tasks)
        
        # Map responses to model names
        response_dict = {
            "ChatGPT": responses[0],
            "Gemini": responses[1],
            "Grok": responses[2]
        }
        
        # Determine which response to show as primary
        primary_response = response_dict[primary_model]
        
        # Create the comparison element if enabled
        elements = []
        if show_comparison:
            comparison = await create_comparison_element(
                user_message=user_input,
                responses=response_dict,
                chat_id=str(int(time.time()))
            )
            elements.append(comparison)
        
        # Update the message with the primary response
        await thinking_msg.update(
            content=primary_response,
            elements=elements
        )
        
        # Add footnote about which model provided the primary response
        await cl.Message(
            content=f"*This primary response was provided by {primary_model}. You can view all model responses in the comparison above.*",
            author="System"
        ).send()
        
        # Update chat history with the primary response
        chat_histories[cl.user_session.id].append({
            "role": "user",
            "content": user_input
        })
        chat_histories[cl.user_session.id].append({
            "role": "assistant",
            "content": primary_response
        })
        
    except Exception as e:
        # Handle any errors
        error_message = f"An error occurred: {str(e)}"
        await thinking_msg.update(content=error_message)
        
        # Log the error
        cl.logger.error(f"Error processing message: {str(e)}")

@cl.on_settings_update
async def on_settings_update(settings: Dict[str, Any]):
    """
    Handle updates to chat settings.
    """
    # Save the updated settings in the user session
    cl.user_session.set("settings", settings)
    
    # Notify the user of the settings change
    model_name = settings.get("primary_model", "ChatGPT")
    show_comparison = settings.get("show_comparison", True)
    
    message = f"Settings updated: Primary model set to {model_name}."
    if show_comparison:
        message += " Side-by-side comparison enabled."
    else:
        message += " Side-by-side comparison disabled."
        
    await cl.Message(content=message, author="System").send()

if __name__ == "__main__":
    # Run the Chainlit app
    pass  # Chainlit takes care of running the app
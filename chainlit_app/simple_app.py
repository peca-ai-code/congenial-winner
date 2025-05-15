"""
Simplified Chainlit application for the Virtual Gynecology Chatbot.
"""

import chainlit as cl
import os
from dotenv import load_dotenv
import openai
import google.generativeai as genai
import requests
import asyncio

# Load environment variables
load_dotenv()

# Configure API keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
grok_api_key = os.getenv("GROK_API_KEY", "")

# Configure models
openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-pro")

# Configure OpenAI
openai.api_key = openai_api_key

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# System prompt for gynecology assistant
SYSTEM_PROMPT = """
You are a virtual gynecology assistant designed to provide support, information,
and reassurance to users with gynecological concerns. Provide clear, accurate,
and concise information. Emphasize when symptoms are likely benign, but always
recommend consulting a healthcare provider for proper diagnosis when appropriate.
Do not provide definitive diagnoses. Be supportive, informative, and reassuring.
"""

# Initialize chat histories for context
chat_histories = {}

async def get_openai_response(user_message, chat_history=None):
    """Get response from OpenAI's GPT model."""
    if not openai_api_key:
        return "Error: OpenAI API key not configured."
    
    try:
        # Create messages array with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=openai_model,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response from ChatGPT: {str(e)}"

async def get_gemini_response(user_message, chat_history=None):
    """Get response from Google's Gemini model."""
    if not gemini_api_key:
        return "Error: Gemini API key not configured."
    
    try:
        # Format history for Gemini
        formatted_history = []
        
        # Add system instruction
        formatted_history.append({
            "role": "user",
            "parts": [{"text": SYSTEM_PROMPT}]
        })
        
        # Add chat history if provided
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
        
        # Make synchronous call in executor to be async-compatible
        loop = asyncio.get_event_loop()
        
        # Define the function to call in the executor
        def generate_response():
            try:
                # Initialize Gemini model
                generation_config = {
                    "temperature": 0.7,
                    "max_output_tokens": 500,
                }
                
                model = genai.GenerativeModel(
                    model_name=gemini_model,
                    generation_config=generation_config
                )
                
                # Generate response
                response = model.generate_content(formatted_history)
                return response.text
            except Exception as e:
                return f"Error in Gemini generation: {str(e)}"
        
        # Run in executor
        response_text = await loop.run_in_executor(None, generate_response)
        return response_text
        
    except Exception as e:
        return f"Error generating response from Gemini: {str(e)}"

async def get_grok_response(user_message, chat_history=None):
    """Simulate a response from Grok (as no public API exists yet)."""
    await asyncio.sleep(1)  # Simulate API delay
    
    return (
        f"[SIMULATED GROK RESPONSE] As Grok doesn't have a public API yet, "
        f"this is a simulated response to demonstrate functionality.\n\n"
        f"In response to your query about '{user_message[:30]}...', "
        f"I would provide gynecological information while recommending "
        f"consultation with a healthcare provider for proper diagnosis."
    )

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    await cl.Message(
        content="Welcome to the Virtual Gynecology Assistant. How can I help you today?",
        author="Assistant"
    ).send()
    
    # Initialize empty chat history for this session
    chat_histories[cl.user_session.id] = []
    
    # Set chat settings
    await cl.ChatSettings(
        [
            cl.switches.Switch(id="show_all_models", label="Show All Model Responses", initial=True),
            cl.select.Select(
                id="primary_model",
                label="Primary Response Model",
                values=["ChatGPT", "Gemini", "Grok"],
                initial="ChatGPT"
            )
        ]
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages and generate responses."""
    # Get user message
    user_input = message.content
    
    # Get chat settings
    settings = cl.user_session.get("settings", {})
    show_all_models = settings.get("show_all_models", True)
    primary_model = settings.get("primary_model", "ChatGPT")
    
    # Add user message to history
    if cl.user_session.id not in chat_histories:
        chat_histories[cl.user_session.id] = []
    
    # Send thinking message
    thinking_msg = cl.Message(content="Generating responses...", author="Assistant")
    await thinking_msg.send()
    
    try:
        # Generate responses from all models concurrently
        tasks = [
            get_openai_response(user_input, chat_histories[cl.user_session.id]),
            get_gemini_response(user_input, chat_histories[cl.user_session.id]),
            get_grok_response(user_input, chat_histories[cl.user_session.id])
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Map responses to model names
        response_dict = {
            "ChatGPT": responses[0],
            "Gemini": responses[1],
            "Grok": responses[2]
        }
        
        # Get primary response
        primary_response = response_dict[primary_model]
        
        # Update thinking message with primary response
        await thinking_msg.update(content=primary_response)
        
        # Add response to chat history
        chat_histories[cl.user_session.id].append({
            "role": "user",
            "content": user_input
        })
        chat_histories[cl.user_session.id].append({
            "role": "assistant",
            "content": primary_response
        })
        
        # Show all model responses if enabled
        if show_all_models:
            for model_name, response_text in response_dict.items():
                if model_name != primary_model:
                    await cl.Message(
                        content=f"**{model_name} Response:**\n\n{response_text}",
                        author=f"AI - {model_name}"
                    ).send()
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await thinking_msg.update(content=error_message)
        cl.logger.error(f"Error processing message: {str(e)}")

@cl.on_settings_update
async def on_settings_update(settings):
    """Handle updates to chat settings."""
    cl.user_session.set("settings", settings)
    
    model_name = settings.get("primary_model", "ChatGPT")
    show_all = settings.get("show_all_models", True)
    
    message = f"Settings updated: Primary model set to {model_name}."
    if show_all:
        message += " All model responses will be shown."
    else:
        message += " Only primary model responses will be shown."
        
    await cl.Message(content=message, author="System").send()

if __name__ == "__main__":
    # Chainlit takes care of running the app
    pass

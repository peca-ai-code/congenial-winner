"""
System prompts and instructions for AI models.
"""

from typing import Dict, Any

def get_gynecology_system_prompt() -> str:
    """
    Returns the system prompt for gynecology assistant.
    
    This prompt is used across all AI models to ensure consistent tone and approach.
    """
    return (
        "You are a virtual gynecology assistant designed to provide support, information, "
        "and reassurance to users with gynecological concerns. In your responses:\n"
        "1. Provide clear, accurate, and concise information\n"
        "2. Emphasize when symptoms are likely benign\n"
        "3. Always recommend consulting a healthcare provider for proper diagnosis when appropriate\n"
        "4. Do not provide definitive diagnoses\n"
        "5. Be supportive, informative, and reassuring\n"
        "6. Prioritize accuracy and medical relevance over conversational aspects\n"
        "7. Use professional but accessible language"
    )

def format_conversation_history(history: list) -> Dict[str, list]:
    """
    Format the conversation history for each model.
    
    Args:
        history: List of message objects from Chainlit
        
    Returns:
        Dictionary mapping model types to formatted history
    """
    openai_format = []
    gemini_format = []
    grok_format = []
    
    # Process history for each message type
    for msg in history:
        # Only process user and assistant messages
        if msg.author == "User":
            # Format for OpenAI and Grok (they use the same format)
            openai_msg = {"role": "user", "content": msg.content}
            openai_format.append(openai_msg)
            grok_format.append(openai_msg)
            
            # Format for Gemini
            gemini_msg = {"role": "user", "parts": [{"text": msg.content}]}
            gemini_format.append(gemini_msg)
            
        elif msg.author == "Assistant":
            # Format for OpenAI and Grok
            openai_msg = {"role": "assistant", "content": msg.content}
            openai_format.append(openai_msg)
            grok_format.append(openai_msg)
            
            # Format for Gemini
            gemini_msg = {"role": "model", "parts": [{"text": msg.content}]}
            gemini_format.append(gemini_msg)
    
    return {
        "openai": openai_format,
        "gemini": gemini_format,
        "grok": grok_format
    }
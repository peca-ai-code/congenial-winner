"""
Components for creating side-by-side model comparison UI.
"""

import chainlit as cl
from typing import List, Dict, Any
from ..config import config

async def create_comparison_element(
    user_message: str,
    responses: Dict[str, str],
    chat_id: str
) -> cl.Element:
    """
    Create a side-by-side comparison of multiple model responses.
    
    Args:
        user_message: The original user message
        responses: Dictionary mapping model names to their responses
        chat_id: The current chat ID
        
    Returns:
        A Chainlit Element for displaying the comparison
    """
    # Create HTML content for the comparison
    html_content = f"""
    <div class="comparison-container">
        <div class="comparison-header">
            <h3>Response Comparison</h3>
            <p class="user-query">Query: <em>{user_message}</em></p>
        </div>
        <div class="comparison-grid">
    """
    
    # Add each model response
    for model_name, response_text in responses.items():
        # Get model color from config
        model_info = next((m for m in config.llms.values() if m.display_name == model_name), None)
        model_color = model_info.color if model_info else "#666666"
        
        # Format the response with proper line breaks
        formatted_response = response_text.replace("\n", "<br>")
        
        html_content += f"""
        <div class="model-response">
            <div class="model-header" style="background-color: {model_color};">
                <h4>{model_name}</h4>
            </div>
            <div class="response-content">
                {formatted_response}
            </div>
        </div>
        """
    
    # Close the HTML container
    html_content += """
        </div>
    </div>
    """
    
    # Create a Chainlit Element with the HTML content
    comparison_element = cl.Element(
        type="html",
        content=html_content,
        name=f"comparison-{chat_id}",
        display="inline"
    )
    
    return comparison_element

async def create_css_element() -> cl.Element:
    """
    Create a CSS element for styling the comparison UI.
    
    Returns:
        A Chainlit Element containing the CSS styles
    """
    css_content = """
    <style>
        .comparison-container {
            font-family: 'Open Sans', sans-serif;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        
        .comparison-header {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-bottom: 1px solid #eee;
        }
        
        .comparison-header h3 {
            margin: 0;
            padding: 0;
            font-size: 1.2rem;
            color: #333;
        }
        
        .user-query {
            margin: 0.5rem 0 0 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .model-response {
            border: 1px solid #ddd;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .model-header {
            padding: 0.75rem 1rem;
            color: white;
        }
        
        .model-header h4 {
            margin: 0;
            padding: 0;
            font-size: 1rem;
        }
        
        .response-content {
            padding: 1rem;
            flex: 1;
            background-color: white;
            font-size: 0.9rem;
            line-height: 1.5;
            overflow-y: auto;
            max-height: 500px;
        }
        
        @media (max-width: 768px) {
            .comparison-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """
    
    # Create a Chainlit Element with the CSS content
    css_element = cl.Element(
        type="html",
        content=css_content,
        name="comparison-css",
        display="inline"
    )
    
    return css_element
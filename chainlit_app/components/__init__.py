"""
Initialize the components package.
"""

from .comparison import create_comparison_element, create_css_element
from .instructions import get_gynecology_system_prompt, format_conversation_history

# Export the component functions
__all__ = [
    "create_comparison_element", 
    "create_css_element",
    "get_gynecology_system_prompt",
    "format_conversation_history"
]
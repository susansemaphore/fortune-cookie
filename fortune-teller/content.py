"""
Centralized content management for Fortune Teller app.
All user-facing text is organized here by step/page.
"""

# Application-wide content
APP_TITLE = "Fortune Teller"
APP_ICON = "🔮"

# Page content organized by step
CONTENT = {
    "start": {
        "title": "The Great Cookie",
        "button_text": "Touch to summon",
    },
    
    "step1": {
        "step_number": 1,
        "field_label": "Tell me your name.",
        "field_placeholder": "",
        "button_text": "Touch to find your fortune",
    },
    
    "step2": {
        "step_number": 2,
        "field_label": "Why have you come to The Great Cookie?",
        "button_text_love": "Love",
        "button_text_fear": "Guidance",
        "button_text_hope": "Fortune",
        "button_text_despair": "Surprise me",
    },
    
    "step3": {
        "step_number": 3,
        "title": "Start the ritual",
        "button_text": "Fingerprint",
    },
    
    "result": {
        "title": "Take your fortune",
        "button_text": "Ask again",
    },
    
    # Love path
    "loveStep1": {
        "step_number": 1,
        "field_label": "what makes your heart race?",
        "field_placeholder": "",
        "button_text": "Continue",
    },
    
    "loveStep2": {
        "step_number": 2,
        "field_label": "what makes your heart race?",
        "field_placeholder": "",
        "button_text": "Reveal my fortune",
    },
    
    # Guidance path
    "guidanceStep1": {
        "step_number": 1,
        "field_label": "Are you enlightened?",
    },
    
    "guidanceStep2": {
        "step_number": 2,
        "field_label": "What path calls to you?",
        "field_placeholder": "Tell me...",
        "button_text": "Reveal my fortune",
    },
    
    # Fortune path
    "fortuneStep1": {
        "step_number": 1,
        "field_label": "What future do you wish to see?",
        "field_placeholder": "Tell me...",
        "button_text": "Continue",
    },
    
    "fortuneStep2": {
        "step_number": 2,
        "field_label": "What do you hope for?",
        "field_placeholder": "Tell me...",
        "button_text": "Reveal my fortune",
    },
    
    # Surprise path
    "surpriseStep1": {
        "step_number": 1,
        "field_label": "Do you have any pets?",
    },
    
    "surpriseStep2": {
        "step_number": 2,
        "field_label": "What mysteries intrigue you?",
        "field_placeholder": "Tell me...",
        "button_text": "Reveal my fortune",
    },
}


def get_content(page_name):
    """
    Get content for a specific page.
    
    Args:
        page_name (str): Name of the page (e.g., 'start', 'step1', 'result')
    
    Returns:
        dict: Content dictionary for the page
    """
    return CONTENT.get(page_name, {})


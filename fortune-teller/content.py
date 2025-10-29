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
        "field_label": "Do you have a love interest?",
    },
    
    "loveStep2": {
        "step_number": 2,
        "has_feelings": {
            "field_label": "What is your favourite feature of your love?",
            "field_prefix": "Their",
            "field_placeholder": "",
        },
        "searching": {
            "field_label": "Name the feature that you look for in a partner.",
            "field_prefix": "I'm looking for someone with",
            "field_placeholder": "",
        },
    },
    
    # Guidance path
    "guidanceStep1": {
        "step_number": 1,
        "field_label": "Are you enlightened?",
    },
    
    "guidanceStep2": {
        "step_number": 2,
        "sage": {
            "field_label": "How did you grow to be so wise?",
            "field_prefix": "I became wise through",
            "field_placeholder": "",
        },
        "student": {
            "field_label": "What has your greatest teacher been?",
            "field_prefix": "I gain wisdom from",
            "field_placeholder": "",
        },
    },
    
    # Fortune path
    "fortuneStep1": {
        "step_number": 1,
        "field_label": "Do you consider yourself lucky?",
    },
    
    "fortuneStep2": {
        "step_number": 2,
        "lucky": {
            "field_label": "What is it that makes you so lucky?",
            "field_prefix": "My luck comes from my",
            "field_placeholder": "",
        },
        "cursed": {
            "field_label": "What omen would convince you the curse was broken?",
            "field_prefix": "I would know the curse was broken if I saw a",
            "field_placeholder": "",
        },
    },
    
    # Surprise path
    "surpriseStep1": {
        "step_number": 1,
        "field_label": "Do you have any pets?",
    },
    
    "surpriseStep2": {
        "step_number": 2,
        "has_pet": {
            "field_label": "What is your pets name?",
            "field_prefix": "My pets name is",
            "field_placeholder": "",
        },
        "petless": {
            "field_label": "What manner of beast do you most love?",
            "field_prefix": "My favourite animal is a",
            "field_placeholder": "",
        },
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


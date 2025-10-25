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
        "field_label": "Favourite color",
        "field_placeholder": "Enter your favourite color...",
        "button_text": "Reveal my fortune",
    },
    
    "step4": {
        "step_number": 4,
        "field_label": "Your mood",
        "field_placeholder": "Enter your mood...",
        "button_text": "Reveal my fortune",
    },
    
    "result": {
        "title_prefix": "✨ Your Fortune, ",
        "title_suffix": " ✨",
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
        "field_label": "What guidance do you seek?",
        "field_placeholder": "Tell me...",
        "button_text": "Continue",
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
        "field_label": "Open your mind to the unexpected...",
        "field_placeholder": "Tell me...",
        "button_text": "Continue",
    },
    
    "surpriseStep2": {
        "step_number": 2,
        "field_label": "What mysteries intrigue you?",
        "field_placeholder": "Tell me...",
        "button_text": "Reveal my fortune",
    },
    
    # Alternative index page (all-in-one form)
    "index": {
        "title": f"{APP_ICON} Magic Fortune Cookie Teller",
        "button_text": "Reveal my fortune",
        "fields": {
            "name": {
                "label": "Initial",
                "placeholder": "Choose...",
            },
            "birth_month": {
                "label": "Birth month",
                "placeholder": "Choose...",
                "options": [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]
            },
            "favorite_color": {
                "label": "Favourite color",
                "placeholder": "Choose...",
                "options": ["Pink", "Blue", "Orange", "Green", "Red"]
            },
            "mood": {
                "label": "Your mood",
                "placeholder": "Choose...",
                "options": ["Mad", "Glad", "Bad", "Sad"]
            }
        }
    }
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


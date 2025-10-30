"""
Fortune message generator for Arduino thermal printer.
Generates personalized fortunes based on user choices.
"""
import random


# Fortune templates organized by category and choice
FORTUNE_TEMPLATES = {
    "love": {
        "has_feelings": [
            "{name} Fortune smiles upon you! You will walk beside a kind soul with a glorious {feature}.",
            "Oh {name}, lover of someone with a majestic {feature}, I see many happy moons ahead of you!",
            "Blessed {name}, your affinity for someone with {feature} will be a true gift to you.",
            "Sweet {name}. I forsee you spending many happy moments with someone that has a {feature}.",
        ],
        "searching": [
            "{name} Keep your eyes open, for someone with a wonderful {feature} will soon cross your path.",
            "Fortunate {name}, a sweet soul with {feature} most sweet lies in your future.",
            "Rejoice {name} - someone special comes your way, and they are blessed in the {feature} department!",
            "My dear {name}, your days as a lone wolf are waning, as soon you will walk beside someone {feature} most glorious.",
        ],
    },
    "guidance": {
        "sage": [
            "Oh wise {name}! {feature} has served you well and will continue to do so.\nMay your wisdom forever brighten your path!",
            "{feature} has already brought you great wisdom {name},\nbut never forget that we are all eternal students of The Great Baker!",
            "Through the chaos of the cosmos {feature} has shown you the way to a peaceful journey.\nRest easy in the knowledge that wisdom is your's {name}!",
            "Knowledge for {feature} is your weapon {name}! Go forth and slay!",
        ],
        "student": [
            "Continue to learn from {feature} {name}! You are wiser than you know!",
            "Wisdom is the greatest treasure. Following {feature} will make you truly rich {name}!",
            "Sweet {name}, keep learning from {feature} and continue to grow!\nNever forget, be excellent to each other!",
            "{name}, student of the cosmos, your humble nature will stand you in good course.\nIf you are learning from {feature} and spreading good vibes everywhere you go, your journey through this life will be truly charmed!",
        ],
    },
    "fortune": {
        "lucky": [
            "Most lucky {name}, your good fortune will continue for many moons! Go forth and share your {feature} with others!",
            "The stars have smiled upon you and your {feature} {name}! Be sure to smile upon all who cross your path today!",
            "Oh {name}, great blessings have been passed on to you by your {feature}! Many happy adventures lie before you!",
            "By the power of {feature}, the odds are forever in your favour {name}! Use your lucky to brighten the lives of one and all!",
        ],
        "cursed": [
            "Sweet {name}, the tides turn! A {feature} will soon present itself to you, and with it your luck will change!",
            "Your path has been shrowded in shadow {name}, but a {feature} will brighten your journey! Till then, When your way gets dark, baby, turn your lights up high!",
            "Prepare for a twist of fate {name}! Any day now a {feature} will cross your path and things will look up for you!",
            "Hold tight {name}! Your luck is about to change! Your {feature} awaits!",
        ],
    },
    "surprise": {
        "has_pet": [
            "{feature} chose wisely when they saw fit to make you their human! Your kindness and warmth will be a blessing to you always, {name}!",
            "The Great Baker has blessed you with many gifts, but {feature} may be the most special bun in your basket! Hold them close {name}, and enjoy your good fortune!",
            "With {feature} by your side your future will be most excellent {name}! Go forth and celebrate!",
            "Blessed {name}, companion to {feature}, the stars of good shine brightly upon you! Rejoice, and share your good fortune with those you meet today!",
        ],
        "petless": [
            "Oh {name}, who has no pets but many blessings. A friendly {feature} will soon cross paths with you.",
            "Praise The Great Baker {name}, for the oven of the Universe bakes the perfect {feature} just for you!",
            "Your life will be blessed by visits from a {feature} again and again, oh lucky a wonderous {name}!",
            "You may find a cute ginger cat at the store across the road, or hope to see a {feature} sometime soon! The choice is your's {name}!",
        ],
    },
}


def generate_fortune_message(session_data):
    """
    Generate a personalized fortune message based on user's choices.
    
    Args:
        session_data (dict): Flask session containing user inputs
        
    Returns:
        str: Formatted fortune message ready for Arduino
    """
    # Extract data from session
    name = session_data.get('name', 'Seeker')
    category = session_data.get('category', 'fortune')
    
    # Get the answer from Step1 (multiple choice)
    answer_key = None
    if category == 'love':
        answer_key = session_data.get('love_answer', 'has_feelings')
    elif category == 'guidance':
        answer_key = session_data.get('guidance_answer', 'student')
    elif category == 'fortune':
        answer_key = session_data.get('fortune_answer', 'lucky')
    elif category == 'surprise':
        answer_key = session_data.get('surprise_answer', 'has_pet')
    
    # Get the text input from Step2
    feature = ""
    if category == 'love':
        feature = session_data.get('love_question', 'kind heart')
    elif category == 'guidance':
        feature = session_data.get('guidance_question', 'experience')
    elif category == 'fortune':
        feature = session_data.get('fortune_question', 'positive spirit')
    elif category == 'surprise':
        feature = session_data.get('surprise_question', 'mystery')
    
    # Get templates for this category and answer
    templates = FORTUNE_TEMPLATES.get(category, {}).get(answer_key, [])
    
    # If no templates found, use a default
    if not templates:
        return f"{name}, the stars align in mysterious ways. Your path is unique."
    
    # Randomly select a template
    template = random.choice(templates)
    
    # Replace placeholders
    fortune = template.format(name=name, feature=feature)
    
    return fortune


def get_fortune_for_arduino(session_data):
    """
    Get fortune message formatted for Arduino transmission.
    
    Args:
        session_data (dict): Flask session data
        
    Returns:
        str: Fortune message
    """
    fortune = generate_fortune_message(session_data)
    
    # Log for debugging
    print("\n" + "="*70)
    print("FORTUNE GENERATED FOR ARDUINO")
    print("="*70)
    print(fortune)
    print("="*70 + "\n")
    
    return fortune


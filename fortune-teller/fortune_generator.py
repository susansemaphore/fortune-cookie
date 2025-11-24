"""
Fortune message generator for Arduino thermal printer.
Generates personalized fortunes based on user choices.
"""
import random


# Fortune templates organized by category and choice
FORTUNE_TEMPLATES = {
    "love": {
        "has_feelings": [
            "{name}, \nfortune smiles upon you! \nYou will walk beside a \nkind soul with a glorious \n{feature}.",
            "Oh {name}, \nlover of someone with a \nmajestic {feature}, \nI see many happy moons ahead of you!",
            "Blessed {name}, \nyour affinity for someone with \n{feature} will be a true \ngift to you.",
            "Sweet {name}. \nI forsee you spending many happy moments with someone that has a \n{feature}.",
        ],
        "searching": [
            "{name} Keep your eyes open, \nfor someone with a wonderful \n{feature} will soon cross \nyour path.",
            "Fortunate {name}, \na sweet soul with \n{feature} most sweet \nlies in your future.",
            "Rejoice {name} - \nsomeone special comes your way, \nand they are blessed in the \n{feature} department!",
            "My dear {name}, \nyour days as a lone wolf are \nwaning, as soon you will walk \nbeside someone {feature} \nmost glorious.",
        ],
    },
    "guidance": {
        "sage": [
            "Oh wise {name}! \n{feature} has served you \nwell and will continue to do so.\nMay your wisdom forever brighten \nyour path!",
            "{feature} has already brought \nyou great wisdom, {name}, \nbut never forget that we are all \neternal students of \nThe Great Baker!",
            "Through the chaos of the cosmos, \n{feature} has shown you the \nway to a peaceful journey. \nRest easy in the knowledge that \nwisdom is yours, {name}!",
            "Knowledge of {feature} \nis your weapon, {name}! \nGo forth and slay!",
        ],
        "student": [
            "Continue to learn from \n{feature}, {name}! \nYou are wiser than \nyou know!",
            "Wisdom is the greatest treasure. \nFollowing {feature} will make \nyou truly rich, {name}!",
            "Sweet {name}, \nkeep learning from {feature} \nand continue to grow!\nNever forget, be excellent \nto each other!",
            "{name}, student of the cosmos, \nyour humble nature will stand \nyou in good course.\nIf you are learning from {feature} \nand spreading good vibes \neverywhere you go, \nyour journey through this life \nwill be truly charmed!",
        ],
    },
    "fortune": {
        "lucky": [
            "Most lucky {name}, \nyour good fortune will continue \nfor many moons! \nGo forth and share your \n{feature} with others!",
            "The stars have smiled upon you \nand your {feature}, {name}! \nBe sure to smile upon all who \ncross your path today!",
            "Oh {name}, great blessings have been \npassed on to you by your {feature}! \nMany happy adventures lie before you!",
            "By the power of {feature}, \nthe odds are forever in your favour, {name}! \nUse your lucky to brighten the lives of one and all!",
        ],
        "cursed": [
            "Sweet {name}, the tides turn! \nA {feature} will soon present \nitself to you, \nand with it your luck will \nchange!",
            "Your path has been shrowded \nin shadow {name}, \nbut a {feature} will \nbrighten your journey! \nTill then, when your way gets \ndark, baby, turn your \nlights up high!",
            "Prepare for a twist of \nfate, {name}! \nAny day now a {feature} will cross \nyour path and things will look \nup for you!",
            "Hold tight, {name}! \nYour luck is about to change! \nYour {feature} awaits!",
        ],
    },
    "surprise": {
        "has_pet": [
            "{feature} chose wisely when \nthey saw fit to make you \ntheir human! Your kindness \nand warmth will be a \nblessing to you always, \n{name}!",
            "The Great Baker has blessed \nyou with many gifts, \nbut {feature} may be the most \nspecial bun in your basket! \nHold them close {name}, \nand enjoy your good fortune!",
            "With {feature} by your side \nyour future will be most \nexcellent, {name}! \nGo forth and celebrate!",
            "Blessed {name}, companion to {feature}, \nthe stars of good shine \nbrightly upon you! \nRejoice, and share your \ngood fortune with those you \nmeet today!",
        ],
        "petless": [
            "Oh {name}, \nwho has no pets \nbut many blessings. \nA friendly {feature} \nwill soon cross \npaths with you.",
            "Praise The Great Baker, {name}, \nfor the oven of the Universe \nbakes the perfect {feature} \njust for you!",
            "Your life will be \nblessed by visits from a \n{feature} again and again, \noh lucky a wonderous, \n{name}!",
            "You may find a cute ginger \ncat at the store across the road, \nor hope to see a {feature} \nsometime soon! \nThe choice is yours, {name}!",
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
    # Capitalize first letter of name
    name = name.capitalize() if name else 'Seeker'
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
        # Capitalize pet's name
        feature = feature.capitalize() if feature else 'mystery'
    
    # Get templates for this category and answer
    templates = FORTUNE_TEMPLATES.get(category, {}).get(answer_key, [])
    
    # If no templates found, use a default
    if not templates:
        return f"{name}, the stars align in mysterious ways. Your path is unique."
    
    # Randomly select a template
    template = random.choice(templates)
    
    # Replace placeholders - add line breaks after custom inputs to prevent word wrapping issues
    fortune = template.format(name=name, feature=feature)
    
    # Clean up any double line breaks that might have been created
    fortune = fortune.replace("\n\n\n", "\n\n")
    
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


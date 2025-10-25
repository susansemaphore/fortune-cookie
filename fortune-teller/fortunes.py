import random

OMENS = [
    "a comet passes quietly overhead",
    "a kind stranger offers unexpected help",
    "you notice repeating numbers everywhere",
    "a long-delayed message finally arrives",
    "a door you forgot about opens again",
]

ADVICE = [
    "Trust the small impulses; they’re your compass.",
    "Write it down tonight—ink traps good luck.",
    "Say yes once more than you usually would.",
    "Clean your workspace; clarity invites opportunity.",
    "Ask a question you’ve been avoiding.",
]

MONTH_ENERGY = {
    "january": "quiet momentum",
    "february": "curious sparks",
    "march": "green beginnings",
    "april": "quick silver",
    "may": "gentle expansion",
    "june": "sunlit paths",
    "july": "warm tides",
    "august": "golden focus",
    "september": "crisp insight",
    "october": "velvet mystery",
    "november": "ember patience",
    "december": "starlit closure",
}

COLOR_AURA = {
    "red": "bold luck",
    "orange": "spark of play",
    "yellow": "clarity and cheer",
    "green": "steady growth",
    "blue": "calm power",
    "indigo": "deep intuition",
    "violet": "quiet magic",
    "pink": "kind momentum",
    "black": "sleek resolve",
    "white": "fresh page",
}

def generate_fortune(name, birth_month, favorite_color, mood):
    month_energy = MONTH_ENERGY.get(birth_month.lower(), "surprising rhythms")
    aura = COLOR_AURA.get(favorite_color.lower(), "mysterious currents")
    omen = random.choice(OMENS)
    advice = random.choice(ADVICE)

    mood_clause = f" Even now, your {mood.lower()} mood is part of the signal." if mood else ""

    lines = [
        f"{name}, the week ahead hums with {month_energy}.",
        f"Your {favorite_color or 'chosen'} hue stirs {aura}.",
        f"A sign will appear when {omen}...",
        advice + mood_clause,
    ]
    return "\n".join(lines)

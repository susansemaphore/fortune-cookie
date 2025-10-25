import random

# Fortune categories with example templates
wisdom_fortunes = [
    "Today, show kindness to a [blank 1]. This will bring [blank 2] into your life.",
    "Your strength lies in your [blank 1]. Embrace it to achieve [blank 2].",
    "Seek wisdom from a [blank 1] today; it will open paths to [blank 2]."
]

predictions_fortunes = [
    "Beware of the [blank 1]—it may bring unexpected [blank 2].",
    "A [blank 1] will soon cross your path, revealing surprising [blank 2].",
    "Prepare for a sudden [blank 1]. It could lead to [blank 2]!"
]

romance_fortunes = [
    "An admirer with a love for [blank 1] may surprise you with their [blank 2].",
    "Someone with a shared passion for [blank 1] might be your [blank 2].",
    "A [blank 1] could be the key to unlocking a [blank 2] heart."
]

surprise_me_fortunes = [
    "Seek the hidden [blank 1]. With [blank 2], you’re unstoppable.",
    "Today, try wearing mismatched [blank 1]. Fortune favors the [blank 2].",
    "An adventure awaits with a [blank 1]. Your [blank 2] spirit will guide you."
]

# Define questions for each category
questions = {
    "wisdom": [
        "What is your greatest strength?",
        "What inspires you the most?",
        "What is a goal you want to achieve?",
        "What brings you joy in life?"
    ],
    "predictions": [
        "What’s your favorite animal?",
        "What is something you fear?",
        "What do you wish for the future?",
        "What makes you laugh?"
    ],
    "romance": [
        "What is your favorite romantic movie?",
        "What quality do you admire most in a partner?",
        "What is your ideal date?",
        "What’s your favorite love song?"
    ],
    "surprise_me": [
        "What is your favorite color?",
        "What hobby would you like to try?",
        "What is something you find mysterious?",
        "What is a surprising fact about you?"
    ]
}

# Function to generate the fortune
def generate_fortune(fortune_template, answer1, answer2):
    return fortune_template.replace("[blank 1]", answer1).replace("[blank 2]", answer2)

# Start of the game
print("The Great Cookie will now bless you!")
print("Choose a category:")
print("1. Wisdom")
print("2. Predictions")
print("3. Romance")
print("4. Surprise Me")

# Get user input for category selection
category_choice = input("Enter the number of your choice (1-4): ")

# Select the appropriate list of fortunes based on the category
if category_choice == "1":
    selected_fortunes = wisdom_fortunes
    category = "wisdom"
elif category_choice == "2":
    selected_fortunes = predictions_fortunes
    category = "predictions"
elif category_choice == "3":
    selected_fortunes = romance_fortunes
    category = "romance"
elif category_choice == "4":
    selected_fortunes = surprise_me_fortunes
    category = "surprise_me"
else:
    print("Invalid category. Defaulting to 'Surprise Me.'")
    selected_fortunes = surprise_me_fortunes
    category = "surprise_me"

# Select a random fortune from the chosen category
fortune = random.choice(selected_fortunes)

# Randomly select two questions from the selected category
selected_questions = random.sample(questions[category], 2)

# Ask for the player’s answers
answer1 = input(f"Question 1: {selected_questions[0]} ")
answer2 = input(f"Question 2: {selected_questions[1]} ")

# Display the completed fortune
print("\nYour Fortune:")
fortune = generate_fortune(fortune, answer1, answer2)
fortune += "\n\n\n\n\n\n\n\n\n\n"
print(fortune)

printer_port = '/dev/ttyS0'
#image_path = "cookie_test.jpg"
#img = Image.open(image_path)

try:
    with open(printer_port, 'wb') as f:
        f.write(fortune.encode('ascii'))
except Exception as e:
    print ("Would Print")
    print (fortune.encode('ascii'))
    print ("====")


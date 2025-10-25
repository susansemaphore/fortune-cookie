from math import floor

import serial
import time
import os
import sys
import termios
from termcolor import colored

# Replace with the correct port for your Arduino
arduino_port = '/dev/ttyUSB0'
#arduino_port = 'COM5'
#arduino_port = ''
baud_rate = 9600  # Match the Arduino baud rate

printer_port = '/dev/ttyS0'


#IDLE = "Idle"
#CHOOSE_TYPE = "Choose_Type"
#QUESTION_1 = "Question_1"
#QUESTION_2 = "Question_2"
#QUESTION_YOUR_DESTINY = "Destination"
#RECEIVE_FATE = "Fate"

texts = {}

def prepare_game():
    tsv_file = 'Fortune cookie - Script.tsv'

    # read tsv file into a list of lists
    lines = []
    with open(tsv_file, 'r') as file:
        lines = file.readlines()
        # remove the first line (header)
        lines = lines[1:]

    lines = [line.strip().split('\t') for line in lines]

    # if any element in lines is len < 3, grow it to be at least len 3
    lines = [line + [''] * (3 - len(line)) for line in lines]

    global texts
    # create a map of texts, key = 0th, value = 2nd
    texts = {line[0]:line[2] for line in lines}

    #print (texts)
    pass

def get_texts(prefix):
    global texts
    return [texts[key] for key in texts.keys() if key.startswith(prefix)]

def get_random_text(prefix):
    import random
    return random.choice(get_texts(prefix)).replace('\\n', '\n')

def test():
    prepare_game()
    print(get_texts('cook_01'))
    print (get_random_text('cook_01'))
    quit()
#test()



# Initially taken from:
# http://code.activestate.com/recipes/134892/
# Thanks to Danny Yoo
# more infos from:
# https://gist.github.com/michelbl/efda48b19d3e587685e3441a74457024
# Thanks to Michel Blancard
def readchar() -> str:
    """Reads a single character from the input stream.
    Blocks until a character is available."""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)
    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)

        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

game_state = "Idle"
console_width = 59
console_height = 18

choice = -1
name = ""
fortune_answer = ""
AB1 = ""

import subprocess

os.system('setterm -foreground magenta')

def game_loop():

    subprocess.Popen(['aplay', 'test.wav'])

    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def neat_print(s):
        clear_terminal()
        print(s)

    def printer_print (fortune):

        try:
            with open(printer_port, 'wb') as f:
                f.write(fortune.encode('ascii'))
        except Exception as e:
            print ("Would Print")
            print (fortune.encode('ascii'))
            print ("====")

    def formatted_input(pre_text, post_text = '', max_char_count=None, ignore_input=False, offset=0, show_carret=True):

        def pink_print(text, end='\n', color='light_magenta'):
            print (text, end=end)
            #print(colored(text, color), end=end)


        input_so_far = ""
        def draw_area(show_carret = True):

            # draw top line /-----\
            pre_lines = pre_text.split("\n")
            post_lines = post_text.split("\n")
            total_lines = len(pre_lines) + len(post_lines) + 1

            half_length = floor(console_height/2)-1#floor(total_lines/2)

            clear_terminal()

            pink_print("/" + "-" * (console_width - 2) + "\\")
            for i in range(half_length-len(pre_lines) + offset - (1-(console_height%2))):
                pink_print("|" + " " * (console_width - 2) + "|")

            for line in pre_lines:
                pink_print("|" + line.center(console_width - 2) + "|")

            carret = '|' if show_carret else ' '
            #print("|" + "-" * (console_width - 2) + "|")
            #pink_print("|" + (input_so_far+carret).center(console_width - 2) + "|")
            spaces = floor((console_width - 2 - len(input_so_far) - 1)/2)
            space_chars = " " * spaces
            extra_space = " " * (console_width - 2 - len(input_so_far) - 1 - spaces)
            pink_print("|" + space_chars, end='')
            pink_print(input_so_far, end='', color='magenta')
            pink_print(carret, end='', color='light_cyan')
            pink_print(extra_space + "|")

            for line in post_lines:
                pink_print("|" + line.center(console_width - 2) + "|")

            for i in range(half_length-len(post_lines) - offset):
                pink_print("|" + " " * (console_width - 2) + "|")

            pink_print("\\" + "-" * (console_width - 2) + "/", end='')
            sys.stdout.flush()


        #import readchar
        # retrieve one character

        if ignore_input:
            draw_area(False)
            return ''

        ch = ''
        while ch != '\n':
            draw_area(show_carret)
            ch = readchar()
            # backspace or delete
            if (ch == '\x08') or (ch == '\x7f'):
                input_so_far = input_so_far[:-1]
            #exit on return
            elif input_so_far.strip() != "" and ((ch == '\n') or (ch == '\r')):
                break
            # if ctrl-c, quit
            elif (ch == '\x03'):
                exit()
            #elif (ch == '`'):
            #    break
            else:
                input_so_far += ch
                print (ch)
                print (input_so_far)

            if len(input_so_far) >= console_width-4 or (max_char_count is not None and len(input_so_far) >= max_char_count):
                break

        return input_so_far.strip()

    global name
    global choice
    global AB1
    global fortune_answer

    global game_state

    topics = {}
    topics[1] = "love"
    topics[2] = "fortune"
    topics[3] = "wisdom"
    topics[4] = "surprize"

    print("game_loop "+game_state)

    def any_key(key):
        return formatted_input(get_random_text(key), max_char_count=1, offset=1, show_carret=False)
    def prompt(key):
        return formatted_input(get_random_text(key)+'\n')
    def prompt_single_char(key, post_key):
        return formatted_input(get_random_text(key)+'\n', '\n'+get_random_text(post_key), max_char_count=1)
    
    if game_state == "Idle":
        any_key('cook_01')
        game_state = "Your_Name"
        return '1'
    elif game_state == "Your_Name":
        name = prompt('cook_02')
        game_state = "Choose_Type"
    elif game_state == "Choose_Type":
        choice = prompt_single_char('cook_03', 'sc_03')
        try:
            choice = int(choice)
        except:
            choice = -1
        if choice < 1 or choice > 4:
            return '_'
        game_state = "Prompt"
    elif game_state == "Prompt":
        any_key(f'cook_04_{topics[choice]}')
        game_state = "AB_Question_1"
    elif game_state == "AB_Question_1":
        AB1 = prompt_single_char(f'cook_05_{topics[choice]}', f'sc_05_{topics[choice]}')

        AB1 = AB1.upper()
        if AB1 not in ['A', 'B']:
            return '_'

        game_state = "Question_2"
    elif game_state == "Question_2":
        fortune_answer = formatted_input(get_random_text(f'cook_06_{topics[choice]}_{AB1}') + '\n' +
                                         get_random_text(f'sc_06_{topics[choice]}_{AB1}'))
        game_state = "QUESTION_YOUR_DESTINY"
    elif game_state == "QUESTION_YOUR_DESTINY":
        formatted_input(get_random_text('cook_07')+'\n', get_random_text('sc_07'),
                        max_char_count=1, offset=1, show_carret=False)
        game_state = "QUESTION_YOUR_DESTINY_AGAIN"
    elif game_state == "QUESTION_YOUR_DESTINY_AGAIN":
        formatted_input(get_random_text('cook_08')+'\n',
                        ignore_input=True, offset=2)
        time.sleep(3)
        game_state = "QUESTION_YOUR_DESTINY_LAST_TIME_I_PROMISE"
    elif game_state == "QUESTION_YOUR_DESTINY_LAST_TIME_I_PROMISE":
        formatted_input(get_random_text('cook_09')+'\n',
                        max_char_count=1, offset=2, show_carret=False)
        game_state = "RECEIVE_FATE"
        return '2'
    elif game_state == "RECEIVE_FATE":

        text = get_random_text(f'fortune_{topics[choice]}_{AB1}_')
        text = text.replace('[lovefeature]', fortune_answer)
        text = text.replace('[fortunefeature]', fortune_answer)
        text = text.replace('[pet]', fortune_answer)
        text = text.replace('[wisdomfeature]', fortune_answer)
        text = text.replace('[PLAYER_NAME]', name)

        formatted_input(text,
                        max_char_count=1, offset=2, show_carret=False)

        #fort = f"Chose {choice}, answer1 {AB1} answer2 {fortune_answer}. DONE"
        printer_print (text)

        time.sleep(2)
        print("printed")

        game_state = "GOODBYE"
    elif game_state == "GOODBYE":

        formatted_input(get_random_text('cook_10')+'\n',
                        max_char_count=1, offset=2, show_carret=False)
        game_state = "Idle"
        return '3'

    return '_'
    
    pass


last_command = '3' # exit code

if arduino_port == '':
    prepare_game()
    while True:
        last_command = game_loop()

    exit()

try:
    # Open the serial connection
    with serial.Serial(arduino_port, baud_rate, timeout=1) as arduino:
        time.sleep(2)  # Allow Arduino time to initialize
        print("Connected to Arduino")

        prepare_game()
        while True:
            # Get input from the user
            command = last_command #input("Enter a number (0-3) or 'q' to quit: ")
            
            if command == 'q':  # Exit condition
                print("Exiting...")
                break
            elif command in [str(i) for i in range(0, 9)]:  # Check for valid input
                # Send the command to Arduino
                arduino.write(command.encode())
                print(f"Sent: {command}")
                
                # Read and display Arduino's response
                response = arduino.readline().decode('utf-8').strip()
                if response:
                    print(f"Arduino: {response}")
            #else:
            #    print("Invalid input. Please enter a number between 1 and 8, or 'q' to quit.")

            last_command = game_loop()

except Exception as e:
    print(f"Error: {e}")

"""
Arduino data serialization module.
Prepares user input data for sending to Arduino via UART.
"""
import json


def get_user_data(session_data):
    """
    Extract and organize user data from session.
    
    Args:
        session_data (dict): Flask session data
        
    Returns:
        dict: Organized user data
    """
    data = {
        'name': session_data.get('name', ''),
        'category': session_data.get('category', ''),
        'category_answer': session_data.get('category_answer', ''),
        # Collect any additional answers from different paths
        'love_question': session_data.get('love_question', ''),
        'guidance_answer': session_data.get('guidance_answer', ''),
        'guidance_question': session_data.get('guidance_question', ''),
        'fortune_answer': session_data.get('fortune_answer', ''),
        'fortune_question': session_data.get('fortune_question', ''),
        'surprise_answer': session_data.get('surprise_answer', ''),
        'surprise_question': session_data.get('surprise_question', ''),
    }
    
    # Remove empty values to keep data clean
    return {k: v for k, v in data.items() if v}


def format_for_arduino_json(session_data):
    """
    Format user data as JSON string for Arduino.
    Compact format suitable for UART transmission.
    
    Args:
        session_data (dict): Flask session data
        
    Returns:
        str: JSON string (compact, no whitespace)
    """
    data = get_user_data(session_data)
    return json.dumps(data, separators=(',', ':'))


def format_for_arduino_simple(session_data):
    """
    Format user data as simple delimited string for Arduino.
    Format: KEY1:VALUE1|KEY2:VALUE2|KEY3:VALUE3
    Easier to parse on Arduino without JSON library.
    
    Args:
        session_data (dict): Flask session data
        
    Returns:
        str: Pipe-delimited key:value pairs
    """
    data = get_user_data(session_data)
    pairs = [f"{k}:{v}" for k, v in data.items()]
    return '|'.join(pairs)


def format_for_arduino_csv(session_data):
    """
    Format user data as CSV string for Arduino.
    Format: name,category,answer1,answer2,...
    
    Args:
        session_data (dict): Flask session data
        
    Returns:
        str: Comma-separated values
    """
    data = get_user_data(session_data)
    
    # Define order for consistent CSV format
    ordered_fields = ['name', 'category', 'category_answer']
    values = [data.get(field, '') for field in ordered_fields]
    
    # Add any other non-empty fields
    for key, value in data.items():
        if key not in ordered_fields and value:
            values.append(value)
    
    return ','.join(values)


def print_data_summary(session_data):
    """
    Print formatted summary of data to console for debugging.
    
    Args:
        session_data (dict): Flask session data
    """
    data = get_user_data(session_data)
    print("\n" + "="*50)
    print("ARDUINO DATA READY")
    print("="*50)
    for key, value in data.items():
        print(f"  {key}: {value}")
    print("="*50)
    print(f"JSON Format:\n  {format_for_arduino_json(session_data)}")
    print(f"Simple Format:\n  {format_for_arduino_simple(session_data)}")
    print(f"CSV Format:\n  {format_for_arduino_csv(session_data)}")
    print("="*50 + "\n")


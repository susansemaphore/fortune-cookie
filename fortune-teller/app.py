from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from fortunes import generate_fortune
from content import get_content
from arduino_data import (
    format_for_arduino_json, 
    format_for_arduino_simple, 
    format_for_arduino_csv,
    print_data_summary,
    get_user_data
)
from arduino_serial import init_arduino, get_arduino

app = Flask(__name__)
app.secret_key = 'fortune-teller-secret-key-change-in-production'

# Initialize Arduino connection on startup
# Set port=None for auto-detection, or specify like port='/dev/ttyUSB0'
arduino_connection = init_arduino(port=None, baudrate=9600)

@app.get("/")
def index():
    # Clear session and show start page
    session.clear()
    content = get_content("start")
    return render_template("start.html", content=content)

@app.get("/step1")
def step1():
    # Clear session and start the fortune telling flow
    session.clear()
    content = get_content("step1")
    return render_template("step1.html", content=content)

@app.post("/step2")
def step2():
    session['name'] = request.form.get("name", "")
    content = get_content("step2")
    return render_template("step2.html", content=content)

@app.post("/step3")
def step3():
    # Store any answers from the category-specific Step1 pages
    session['category_answer'] = request.form.get("love_answer") or request.form.get("guidance_answer") or request.form.get("fortune_answer") or request.form.get("surprise_answer")
    content = get_content("step3")
    return render_template("step3.html", content=content)

@app.post("/fingerprint-animation")
def fingerprint_animation():
    return render_template("fingerprint_animation.html")

@app.get("/show-fortune")
def show_fortune():
    # Print data summary to console for debugging
    print_data_summary(session)
    
    # Send data to Arduino
    arduino = get_arduino()
    if arduino and arduino.is_connected:
        user_data = get_user_data(session)
        arduino.send_json(user_data)
        
        # Optional: Wait for and log Arduino response
        response = arduino.read_response()
        if response:
            print(f"Arduino acknowledged: {response}")
    
    content = get_content("result")
    return render_template("result.html", content=content)

@app.get("/api/arduino-data")
def get_arduino_data():
    """
    API endpoint to get user data in various formats for Arduino.
    Query parameter 'format' can be: json (default), simple, or csv
    """
    data_format = request.args.get('format', 'json')
    
    if data_format == 'simple':
        return format_for_arduino_simple(session), 200, {'Content-Type': 'text/plain'}
    elif data_format == 'csv':
        return format_for_arduino_csv(session), 200, {'Content-Type': 'text/plain'}
    else:  # json
        return format_for_arduino_json(session), 200, {'Content-Type': 'application/json'}

@app.post("/fortune")
def fortune():
    session['mood'] = request.form.get("mood", "")
    
    name = session.get('name', 'Mystery Seeker').strip()
    birth_month = session.get('birth_month', '').strip()
    favorite_color = session.get('favorite_color', '').strip()
    mood = session.get('mood', '').strip()

    fortune_text = generate_fortune(
        name=name,
        birth_month=birth_month,
        favorite_color=favorite_color,
        mood=mood,
    )
    content = get_content("result")
    return render_template("result.html", name=name, fortune=fortune_text, content=content)

# Animation route
@app.post("/animation/<category>")
def show_animation(category):
    if category not in ['love', 'guidance', 'fortune', 'surprise']:
        return redirect(url_for('step1'))
    session['category'] = category
    return render_template("animation.html", category=category)

# Love path
@app.route("/loveStep1")
def loveStep1():
    content = get_content("loveStep1")
    return render_template("loveStep1.html", content=content)

@app.post("/loveStep2")
def loveStep2():
    session['love_question'] = request.form.get("love_question", "")
    content = get_content("loveStep2")
    return render_template("loveStep2.html", content=content)

# Guidance path
@app.route("/guidanceStep1")
def guidanceStep1():
    content = get_content("guidanceStep1")
    return render_template("guidanceStep1.html", content=content)

@app.post("/guidanceStep2")
def guidanceStep2():
    session['guidance_question'] = request.form.get("guidance_question", "")
    content = get_content("guidanceStep2")
    return render_template("guidanceStep2.html", content=content)

# Fortune path
@app.route("/fortuneStep1")
def fortuneStep1():
    content = get_content("fortuneStep1")
    return render_template("fortuneStep1.html", content=content)

@app.post("/fortuneStep2")
def fortuneStep2():
    session['fortune_question'] = request.form.get("fortune_question", "")
    content = get_content("fortuneStep2")
    return render_template("fortuneStep2.html", content=content)

# Surprise path
@app.route("/surpriseStep1")
def surpriseStep1():
    content = get_content("surpriseStep1")
    return render_template("surpriseStep1.html", content=content)

@app.post("/surpriseStep2")
def surpriseStep2():
    session['surprise_question'] = request.form.get("surprise_question", "")
    content = get_content("surpriseStep2")
    return render_template("surpriseStep2.html", content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

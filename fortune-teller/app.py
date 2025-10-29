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
    # Store text input from Step2 pages
    love_q = request.form.get("love_question", "")
    guidance_q = request.form.get("guidance_question", "")
    fortune_q = request.form.get("fortune_question", "")
    surprise_q = request.form.get("surprise_question", "")
    
    if love_q:
        session['love_question'] = love_q
    if guidance_q:
        session['guidance_question'] = guidance_q
    if fortune_q:
        session['fortune_question'] = fortune_q
    if surprise_q:
        session['surprise_question'] = surprise_q
    
    content = get_content("step3")
    return render_template("step3.html", content=content)

@app.post("/fingerprint-animation")
def fingerprint_animation():
    # Send data to Arduino when user clicks "Fingerprint" button
    print_data_summary(session)
    
    arduino = get_arduino()
    if arduino and arduino.is_connected:
        user_data = get_user_data(session)
        arduino.send_json(user_data)
        
        # Optional: Wait for and log Arduino response
        response = arduino.read_response()
        if response:
            print(f"Arduino acknowledged: {response}")
    
    return render_template("fingerprint_animation.html")

@app.get("/show-fortune")
def show_fortune():
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
    # Store Step1 multiple choice answer
    love_answer = request.form.get("love_answer", "")
    session['love_answer'] = love_answer
    
    # Get conditional content based on Step1 answer
    content_all = get_content("loveStep2")
    content = content_all.get(love_answer, content_all.get("has_feelings", {}))
    
    return render_template("loveStep2.html", content=content)

# Guidance path
@app.route("/guidanceStep1")
def guidanceStep1():
    content = get_content("guidanceStep1")
    return render_template("guidanceStep1.html", content=content)

@app.post("/guidanceStep2")
def guidanceStep2():
    # Store Step1 multiple choice answer
    guidance_answer = request.form.get("guidance_answer", "")
    session['guidance_answer'] = guidance_answer
    
    # Get conditional content based on Step1 answer
    content_all = get_content("guidanceStep2")
    content = content_all.get(guidance_answer, content_all.get("student", {}))
    
    return render_template("guidanceStep2.html", content=content)

# Fortune path
@app.route("/fortuneStep1")
def fortuneStep1():
    content = get_content("fortuneStep1")
    return render_template("fortuneStep1.html", content=content)

@app.post("/fortuneStep2")
def fortuneStep2():
    # Store Step1 multiple choice answer
    fortune_answer = request.form.get("fortune_answer", "")
    session['fortune_answer'] = fortune_answer
    
    # Get conditional content based on Step1 answer
    content_all = get_content("fortuneStep2")
    content = content_all.get(fortune_answer, content_all.get("lucky", {}))
    
    return render_template("fortuneStep2.html", content=content)

# Surprise path
@app.route("/surpriseStep1")
def surpriseStep1():
    content = get_content("surpriseStep1")
    return render_template("surpriseStep1.html", content=content)

@app.post("/surpriseStep2")
def surpriseStep2():
    # Store Step1 multiple choice answer
    surprise_answer = request.form.get("surprise_answer", "")
    session['surprise_answer'] = surprise_answer
    
    # Get conditional content based on Step1 answer
    content_all = get_content("surpriseStep2")
    content = content_all.get(surprise_answer, content_all.get("has_pet", {}))
    
    return render_template("surpriseStep2.html", content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

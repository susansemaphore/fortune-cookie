# 🔮 Fortune Teller

A mystical Flask web application that generates personalized fortunes based on your name, birth month, favorite color, and current mood.

## 📋 Project Description

Fortune Teller is an interactive multi-step form application that guides users through a series of questions to generate a unique, personalized fortune. The app uses Flask for the backend and provides a beautiful, engaging user experience.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Navigate to the project directory**
   ```bash
   cd /Users/susanspangenberg/Documents/fortune-teller
   ```

2. **Create a virtual environment** (if you haven't already)
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```
   
   *You should see `(venv)` appear at the beginning of your terminal prompt.*

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Application

1. **Activate your virtual environment** (if not already activated)
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Flask application**
   ```bash
   python app.py
   ```

3. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

4. **Stop the server**
   
   Press `Ctrl+C` in the terminal when you're done.

## 📦 Dependencies

- **Flask** (>=2.3, <4): Web framework for Python

See `requirements.txt` for the complete list.

## 🏗️ Project Structure

```
fortune-teller/
├── app.py              # Main Flask application
├── content.py          # Centralized content management
├── fortunes.py         # Fortune generation logic
├── requirements.txt    # Python dependencies
├── CONTENT_GUIDE.md    # Guide for managing app content
├── static/
│   └── style.css      # CSS styling
└── templates/
    ├── base.html      # Base template
    ├── start.html     # Start/landing page
    ├── index.html     # All-in-one form page
    ├── step1.html     # Step 1: Name input
    ├── step2.html     # Step 2: Birth month
    ├── step3.html     # Step 3: Favorite color
    ├── step4.html     # Step 4: Current mood
    └── result.html    # Fortune result page
```

## 🎯 How It Works

1. User enters their name
2. User selects their birth month
3. User chooses their favorite color
4. User indicates their current mood
5. The app generates a personalized fortune based on all inputs

## 💡 Tips

- **Deactivate the virtual environment** when you're done:
  ```bash
  deactivate
  ```

- **Update dependencies** if needed:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

- **Check if virtual environment is active**: Look for `(venv)` at the start of your terminal prompt

## 📝 Content Management

All user-facing text (titles, labels, button text, placeholders) is centralized in `content.py`. This makes it easy to update text without touching HTML templates.

**To change any text displayed in the app:**
1. Open `content.py`
2. Find the page/step you want to modify
3. Update the text values
4. Save and refresh your browser

📖 See `CONTENT_GUIDE.md` for detailed documentation on managing content.

## ⚙️ Configuration

The application runs on:
- **Host**: 0.0.0.0 (accessible from any network interface)
- **Port**: 5001
- **Debug Mode**: Enabled (automatically reloads on code changes)

⚠️ **Note**: Change the `secret_key` in `app.py` before deploying to production!

## 🐛 Troubleshooting

**Virtual environment not activating?**
- Make sure you're in the correct directory
- Try: `source venv/bin/activate` or `source env/bin/activate`

**Port 5001 already in use?**
- Edit `app.py` and change the port number in the last line
- Or stop any other processes using port 5001

**Module not found errors?**
- Make sure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## 📝 License

This project is for educational and entertainment purposes.

---

✨ *May your fortunes be ever in your favor!* ✨


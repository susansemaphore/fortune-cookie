# Content Quick Reference Card

## 🎯 Where to Find What

| What You Want to Change | Location in `content.py` | Key Name |
|------------------------|--------------------------|----------|
| **Start page title** | `CONTENT["start"]` | `title` |
| **Start button text** | `CONTENT["start"]` | `button_text` |
| **Step 1 title** | `CONTENT["step1"]` | `title` |
| **Step 1 field label** | `CONTENT["step1"]` | `field_label` |
| **Step 1 placeholder** | `CONTENT["step1"]` | `field_placeholder` |
| **Step 1 button** | `CONTENT["step1"]` | `button_text` |
| **Step 2 title** | `CONTENT["step2"]` | `title` |
| **Step 2 field label** | `CONTENT["step2"]` | `field_label` |
| **Step 2 placeholder** | `CONTENT["step2"]` | `field_placeholder` |
| **Step 2 button** | `CONTENT["step2"]` | `button_text` |
| **Step 3 title** | `CONTENT["step3"]` | `title` |
| **Step 3 field label** | `CONTENT["step3"]` | `field_label` |
| **Step 3 placeholder** | `CONTENT["step3"]` | `field_placeholder` |
| **Step 3 button** | `CONTENT["step3"]` | `button_text` |
| **Step 4 title** | `CONTENT["step4"]` | `title` |
| **Step 4 field label** | `CONTENT["step4"]` | `field_label` |
| **Step 4 placeholder** | `CONTENT["step4"]` | `field_placeholder` |
| **Step 4 button** | `CONTENT["step4"]` | `button_text` |
| **Result page title parts** | `CONTENT["result"]` | `title_prefix`, `title_suffix` |
| **Result page button** | `CONTENT["result"]` | `button_text` |
| **All-in-one form title** | `CONTENT["index"]` | `title` |
| **All-in-one form button** | `CONTENT["index"]` | `button_text` |
| **Name field label** | `CONTENT["index"]["fields"]["name"]` | `label` |
| **Birth month options** | `CONTENT["index"]["fields"]["birth_month"]` | `options` |
| **Color options** | `CONTENT["index"]["fields"]["favorite_color"]` | `options` |
| **Mood options** | `CONTENT["index"]["fields"]["mood"]` | `options` |

## 📋 Current Content by Step

### Start Page (Landing)
```
Title: 🔮 Fortune Cookie Teller
Button: Let's begin
```

### Step 1 - Name
```
Title: 🔮 Magic Fortune Cookie Teller
Label: Name
Placeholder: Enter your name...
Button: Reveal my fortune
```

### Step 2 - Birth Month
```
Title: 🔮 Magic Fortune Cookie Teller
Label: Birth month
Placeholder: Enter your birth month...
Button: Reveal my fortune
```

### Step 3 - Favorite Color
```
Title: 🔮 Magic Fortune Cookie Teller
Label: Favourite color
Placeholder: Enter your favourite color...
Button: Reveal my fortune
```

### Step 4 - Mood
```
Title: 🔮 Magic Fortune Cookie Teller
Label: Your mood
Placeholder: Enter your mood...
Button: Reveal my fortune
```

### Result Page
```
Title: ✨ Your Fortune, [NAME] ✨
Button: Ask again
```

### All-in-One Form
```
Title: 🔮 Magic Fortune Cookie Teller
Button: Reveal my fortune

Fields:
  • Initial (dropdown A-Z)
  • Birth month (Jan-Dec)
  • Favourite color (Pink, Blue, Orange, Green, Red)
  • Your mood (Mad, Glad, Bad, Sad)
```

## 🔧 Common Tasks

### Task: Change emoji icon throughout app
```python
# In content.py, line 6:
APP_ICON = "🌟"  # Change from 🔮 to 🌟
```

### Task: Make all titles consistent
```python
# Update each step's title:
"step1": { "title": f"{APP_ICON} Your New Title" }
"step2": { "title": f"{APP_ICON} Your New Title" }
# etc.
```

### Task: Change all button text to "Continue"
```python
# Update button_text in each step:
"step1": { "button_text": "Continue" }
"step2": { "button_text": "Continue" }
"step3": { "button_text": "Continue" }
"step4": { "button_text": "Continue" }
```

### Task: Add more color options
```python
"index": {
    "fields": {
        "favorite_color": {
            "options": ["Pink", "Blue", "Orange", "Green", "Red", 
                       "Purple", "Yellow", "Black", "White"]
        }
    }
}
```

## 💡 Pro Tips

1. **Use APP_ICON variable** - It's defined once at the top, used everywhere
2. **Keep structure consistent** - All steps have the same fields
3. **Test after changes** - Refresh browser to see updates
4. **Check quotes** - Use matching quotes (single or double)
5. **Watch commas** - Last item in a dict shouldn't have a trailing comma (Python allows it but it's cleaner)

## 🎨 Style Guide Suggestions

- **Titles**: Start with emoji, end with app name
- **Labels**: Short, 1-3 words, clear purpose
- **Placeholders**: Start with verb (Enter, Choose, Select)
- **Buttons**: Action-oriented (Next, Continue, Submit, Reveal)

## 📱 File Locations

```
content.py              ← All content here
app.py                  ← Routes pass content to templates
templates/              ← Templates use {{ content.* }}
  ├── start.html        ← Uses content.start
  ├── step1.html        ← Uses content.step1
  ├── step2.html        ← Uses content.step2
  ├── step3.html        ← Uses content.step3
  ├── step4.html        ← Uses content.step4
  ├── result.html       ← Uses content.result
  └── index.html        ← Uses content.index
```

---

**Last Updated**: October 13, 2025  
**For detailed guide**: See `CONTENT_GUIDE.md`  
**For changes made**: See `CHANGES_SUMMARY.md`


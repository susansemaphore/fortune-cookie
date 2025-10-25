# Content Management Guide

## Overview
All user-facing text content for the Fortune Teller app is centralized in the `content.py` file. This makes it easy to update text, change wording, or add translations without touching the HTML templates.

## File Structure

### `content.py`
This is the central location for all text content. The content is organized by page/step in a dictionary structure.

## How to Update Content

### Changing Text for a Specific Step

To change any text displayed in the app, simply edit the `content.py` file:

```python
CONTENT = {
    "step1": {
        "step_number": 1,
        "title": "🔮 Magic Fortune Cookie Teller",
        "field_label": "Name",                        # ← Change label here
        "field_placeholder": "",    # ← Change placeholder here
        "button_text": "Reveal my fortune",           # ← Change button text here
    },
    # ... more steps
}
```

### Content Structure by Page

#### **Start Page** (`start`)
- `title`: Main heading
- `button_text`: Text for the "begin" button

#### **Steps 1-4** (`step1`, `step2`, `step3`, `step4`)
Each step has:
- `step_number`: Numeric identifier for the step
- `title`: Page heading
- `field_label`: Label above the input field
- `field_placeholder`: Placeholder text in the input field
- `button_text`: Text for the submit button

**Step Details:**
- **Step 1**: Name input
- **Step 2**: Birth month input
- **Step 3**: Favourite color input
- **Step 4**: Mood input

#### **Result Page** (`result`)
- `title_prefix`: Text before the user's name (default: "✨ Your Fortune, ")
- `title_suffix`: Text after the user's name (default: " ✨")
- `button_text`: Text for the "try again" button

#### **All-in-One Form** (`index`)
This page shows all fields at once. Structure:
- `title`: Page heading
- `button_text`: Submit button text
- `fields`: Dictionary containing configuration for each field
  - Each field has: `label`, `placeholder`, and optionally `options` (for select dropdowns)

## Examples

### Example 1: Change the title for all steps
```python
# In content.py, update all step titles:
"step1": {
    "title": "🌟 New Title Here 🌟",
    # ...
}
```

### Example 2: Change placeholder text
```python
"step1": {
    # ...
    "field_placeholder": "What's your name?",
}
```

### Example 3: Change button text
```python
"step1": {
    # ...
    "button_text": "Next Step →",
}
```

### Example 4: Update dropdown options
```python
"index": {
    # ...
    "fields": {
        "mood": {
            "label": "Your mood",
            "placeholder": "Choose...",
            "options": ["Happy", "Excited", "Calm", "Curious"]  # ← Add/remove options here
        }
    }
}
```

## Adding New Content

If you add new pages or need new content fields:

1. Add the content to the `CONTENT` dictionary in `content.py`:
```python
CONTENT = {
    # ... existing content
    "new_page": {
        "title": "New Page Title",
        "some_text": "Some text content",
    }
}
```

2. Update the route in `app.py` to pass the content:
```python
@app.get("/new-page")
def new_page():
    content = get_content("new_page")
    return render_template("new_page.html", content=content)
```

3. Use the content in your template:
```html
{% extends "base.html" %}
{% block content %}
  <h1>{{ content.title }}</h1>
  <p>{{ content.some_text }}</p>
{% endblock %}
```

## Benefits of This Approach

✅ **Single source of truth**: All text is in one place  
✅ **Easy updates**: Change text without touching HTML  
✅ **Clear organization**: Content is organized by page/step  
✅ **Translation-ready**: Easy to add multiple language support later  
✅ **Type safety**: Python dictionaries with clear structure  
✅ **Version control friendly**: Changes to content are easy to track

## Future Enhancements

Consider these improvements:
- Add multi-language support by creating language-specific content dictionaries
- Move content to JSON or YAML files for easier editing by non-developers
- Add content validation to ensure required fields are present
- Create content versioning for A/B testing different text variations


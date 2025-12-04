from flask import Blueprint, render_template
from pathlib import Path
import json

main = Blueprint('main', __name__)

def get_profile_context(filepath='data.json'):
    """
    Reads the JSON file and returns a dictionary formatted 
    specifically for the Jinja2 template in index.html.
    """
    # Create a Path object from the input string
    path = Path(filepath)

    try:
        # Use path.open() instead of the built-in open()
        with path.open('r', encoding='utf-8') as file:
            data = json.load(file)
            
        context = {
            "name": data.get('name', 'DevOps Engineer'),
            "foreword": data.get('foreword', ''),
            "education": data.get('education', []),
            "repos": data.get('repos', [])
        }
        
        return context

    except FileNotFoundError:
        print(f"Error: The file '{path.resolve()}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{path.name}'.")
        return {}

@main.route('/')
def index():
    content = get_profile_context()
 
    return render_template('index.html', **content)
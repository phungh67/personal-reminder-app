from flask import Blueprint, render_template
import json

main = Blueprint('main', __name__)

def get_profile_context(filepath='data.json'):
    """
    Reads the JSON file and returns a dictionary formatted 
    specifically for the Jinja2 template in index.html.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)

        context = {
            "name": data.get('name', 'DevOps Engineer'),
            "foreword": data.get('foreword', ''),
            "education": data.get('education', []),
            "repos": data.get('repos', [])
        }
        
        return context

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{filepath}'.")
        return {}

@main.route('/')
def index():
    input_file = "data.json"
    with open(input_file, encoding="utf-8") as json_file:
        extracted_data = get_profile_context(input_file)
 
    return render_template('index.html', **extracted_data)
from flask import Blueprint, render_template, current_app, request, jsonify
from pathlib import Path
import json
import os

from app.services.scheduler import NoteScheduler
from app.services.blog import BlogService

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
    content = get_profile_context('app/main/data.json')
 
    return render_template('index.html', **content)

@main.route('/api/schedule-note', methods=['POST'])
def schedule_note():
    """
    Receives JSON payload from the frontend:
    {
        "recipient": "email@example.com",
        "content": "# Markdown Content",
        "time": "2025-12-08T10:00"
    }
    """
    data = request.get_json()
    
    # 1. Validation
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    recipient = data.get('recipient')
    content = data.get('content')
    trigger_time = data.get('time')

    if not all([recipient, content, trigger_time]):
        return jsonify({"error": "Missing required fields (recipient, content, time)"}), 400

    # 2. Schedule the Note
    # We initialize the class to access the DB methods
    scheduler = NoteScheduler()
    
    try:
        scheduler.schedule_note(recipient, content, trigger_time)
        return jsonify({
            "status": "success", 
            "message": "Note scheduled successfully",
            "time": trigger_time
        }), 201
    except Exception as e:
        print(f"Scheduler Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@main.route('/api/post', methods=['POST'])
def publish_post():
    # pre check
    if request.headers.get('X-Admin-Token') != os.environ.get('ADMIN_TOKEN'):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()

    blog_service = BlogService()
    post_id = blog_service.create_post(data['title'], data['content'])

    if post_id:
        return jsonify({"status": "published", "id": post_id}), 201
    return jsonify({"error": "Database error"}), 500
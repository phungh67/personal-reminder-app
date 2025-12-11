import sqlite3
import markdown
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.mail import EmailService

# Database file path (Best to put this in your 'data' volume)
DB_PATH = os.environ.get('DB_PATH', 'data/notes.db')

class NoteScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.email_service = EmailService()
        self._init_db()

    def _init_db(self):
        """Creates the SQLite table if it doesn't exist."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT NOT NULL,
                    content_markdown TEXT NOT NULL,
                    scheduled_time TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            ''')

    def start(self):
        """Starts the background scheduler."""
        # Run the check function every 60 seconds
        self.scheduler.add_job(self.check_due_notes, 'interval', seconds=60)
        self.scheduler.start()
        print("--- Scheduler Started: Checking for notes every 60s ---")

    def schedule_note(self, recipient, content, trigger_time_str):
        """Saves a note to the DB."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                'INSERT INTO notes (recipient, content_markdown, scheduled_time) VALUES (?, ?, ?)',
                (recipient, content, trigger_time_str)
            )
            print(f"--- Note scheduled for {trigger_time_str} ---")

    def check_due_notes(self):
        """
        The background job.
        1. Find notes where time <= now AND status is 'pending'.
        2. Send email.
        3. Mark as 'sent'.
        """
        now = datetime.now().isoformat()
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Find due notes
            cursor.execute(
                "SELECT * FROM notes WHERE status='pending' AND scheduled_time <= ?", 
                (now,)
            )
            due_notes = cursor.fetchall()

            for note in due_notes:
                print(f"--- Processing Note ID {note['id']} ---")
                
                # Convert Markdown to HTML for the email body
                html_content = markdown.markdown(note['content_markdown'])
                
                # Send Email
                subject = "You have a scheduled note"
                success = self.email_service.send_email(note['recipient'], subject, html_content)

                if success:
                    cursor.execute("UPDATE notes SET status='sent' WHERE id=?", (note['id'],))
                    conn.commit()
                    print(f"--- Note ID {note['id']} SENT ---")
                else:
                    print(f"--- Note ID {note['id']} FAILED to send ---")
    
    def get_all_notes(self):
        """Fetches all notes to display in the UI."""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM notes ORDER BY scheduled_time ASC")
                rows = cursor.fetchall()
                # Convert sqlite Rows to list of dicts
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"DB Error: {e}")
            return []
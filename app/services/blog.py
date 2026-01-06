import sqlite3
import os
from datetime import datetime

# check datapath, from env variable or using default one
DB_PATH = os.environ.get('DB_PATH', 'data/notes.db')

class BlogService:
    def create_post(self, title, content):
        """Class object for the blog service, holds and manages the blog post
    
        Keyword arguments:
        Insert -- Insert a new blog post into the database
        Return: returns the new blog post ID or None if failure
        """
        # catch database failure first
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)',
                    (title, content, datetime.now().isoformat())
                )
            conn.commit
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error happened as: {e}")
            return None
        
    # function to display all post
    def get_all_posts(self):
        """Fetches all posts ordered by date."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    
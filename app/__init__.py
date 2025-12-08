from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration usually goes here (e.g., app.config.from_object(Config))

    # Register Blueprints
    from app.main.routes import main
    app.register_blueprint(main)

    global scheduler
    
    # We only start the scheduler if we are NOT in the reloader's main process
    # or if we are not in debug mode. This prevents it from running twice.
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        from app.services.scheduler import NoteScheduler
        print("--- APP STARTUP: Initializing Scheduler ---")
        scheduler = NoteScheduler()
        scheduler.start()

    return app
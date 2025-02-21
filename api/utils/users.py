# User Preference Persistence Logic
from app import db

class UserPreference(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)
    preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), 
                         onupdate=db.func.now())

# Add to rasa/actions/preferences.py
from utils.redis_manager import RedisSessionManager

class ActionSavePreference(Action):
    def name(self) -> Text:
        return "action_save_preference"
    
    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        prefs = {
            "language": tracker.get_slot("language"),
            "notification_prefs": tracker.get_slot("notification_prefs")
        }
        
        # Save to both Redis and PostgreSQL
        RedisSessionManager().store_session(user_id, prefs)
        UserPreference.update_prefs(user_id, prefs)
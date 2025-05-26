from app.models import db
from datetime import datetime

class TranslationHistory(db.Model):
    __tablename__ = 'translation_history'
    
    id = db.Column(db.String(50), primary_key=True)  # Will be generated as UUID
    user_id = db.Column(db.String(100), nullable=False)  # Firebase UID
    source_text = db.Column(db.Text, nullable=False)  # Original text
    translated_text = db.Column(db.Text, nullable=False)  # Translated text
    source_language = db.Column(db.String(10), nullable=False)  # Language code (e.g., "en")
    target_language = db.Column(db.String(10), nullable=False)  # Language code (e.g., "es")
    source_language_label = db.Column(db.String(100), nullable=False)  # Human-readable (e.g., "English")
    target_language_label = db.Column(db.String(100), nullable=False)  # Human-readable (e.g., "Spanish")
    timestamp = db.Column(db.DateTime, nullable=False)  # When translation was created
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # When record was saved
    
    def __repr__(self):
        return f'<TranslationHistory {self.id} for user {self.user_id}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'sourceText': self.source_text,
            'translatedText': self.translated_text,
            'sourceLanguage': self.source_language,
            'targetLanguage': self.target_language,
            'sourceLanguageLabel': self.source_language_label,
            'targetLanguageLabel': self.target_language_label,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'userId': self.user_id
        } 
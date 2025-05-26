from app.models import db
from datetime import datetime

class TripHistory(db.Model):
    __tablename__ = 'trip_history'
    
    id = db.Column(db.String(50), primary_key=True)  # Will be generated as UUID
    user_id = db.Column(db.String(100), nullable=False)  # Firebase UID
    request_data = db.Column(db.JSON, nullable=False)  # Trip planning request object
    response_data = db.Column(db.JSON, nullable=False)  # Generated trip itinerary response
    timestamp = db.Column(db.DateTime, nullable=False)  # When trip was planned
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # When record was saved
    
    def __repr__(self):
        return f'<TripHistory {self.id} for user {self.user_id}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'request': self.request_data,
            'response': self.response_data,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'userId': self.user_id
        } 
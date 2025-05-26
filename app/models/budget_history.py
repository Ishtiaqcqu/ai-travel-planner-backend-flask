from app.models import db
import json
from datetime import datetime

class BudgetHistory(db.Model):
    __tablename__ = 'budget_history'
    
    id = db.Column(db.String(50), primary_key=True)  # Will be generated as UUID
    user_id = db.Column(db.String(100), nullable=False)  # Firebase UID
    request_data = db.Column(db.JSON, nullable=False)  # BudgetRequest object
    response_data = db.Column(db.JSON, nullable=False)  # BudgetResponse object
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BudgetHistory {self.id} for user {self.user_id}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'request': self.request_data,
            'response': self.response_data
        } 
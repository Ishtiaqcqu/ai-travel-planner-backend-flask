from app.models import db
from datetime import datetime

class ApiHit(db.Model):
    __tablename__ = 'api_hits'
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    status_code = db.Column(db.Integer, nullable=True)
    response_time = db.Column(db.Float, nullable=True)  # in milliseconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with User
    user = db.relationship('User', backref='api_hits')
    
    def __repr__(self):
        return f'<ApiHit {self.method} {self.endpoint}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'method': self.method,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user': self.user.to_dict() if self.user else None
        } 
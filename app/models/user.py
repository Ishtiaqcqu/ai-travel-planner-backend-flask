from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False, default='Member')
    passport_number = db.Column(db.String(50), nullable=True)
    travel_preferences = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<User {self.email}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'fullName': self.fullName,
            'email': self.email,
            'role': self.role,
            'passport_number': self.passport_number,
            'travel_preferences': self.travel_preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 
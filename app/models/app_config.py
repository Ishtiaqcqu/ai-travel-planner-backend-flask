from app.models import db
from datetime import datetime

class AppConfig(db.Model):
    __tablename__ = 'app_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    
    # Relationship with Admin
    admin = db.relationship('Admin', backref='config_updates')
    
    def __repr__(self):
        return f'<AppConfig {self.key}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    @staticmethod
    def get_config(key, default=None):
        """Get a configuration value by key"""
        config = AppConfig.query.filter_by(key=key).first()
        return config.value if config else default
    
    @staticmethod
    def set_config(key, value, description=None, admin_id=None):
        """Set a configuration value"""
        config = AppConfig.query.filter_by(key=key).first()
        if config:
            config.value = value
            config.updated_by = admin_id
            if description:
                config.description = description
        else:
            config = AppConfig(
                key=key,
                value=value,
                description=description,
                updated_by=admin_id
            )
            db.session.add(config)
        db.session.commit()
        return config 
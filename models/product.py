from datetime import datetime
from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def update_stock(self, quantity):
        """Update product stock"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

    @classmethod
    def get_by_category(cls, category):
        return cls.query.filter_by(category=category).all()
    
    def check_stock_availability(self, requested_quantity):
        return self.stock >= requested_quantity

from . import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        }

    def update_quantity(self, new_quantity):
        """Update cart item quantity"""
        if new_quantity > 0 and new_quantity <= self.product.stock:
            self.quantity = new_quantity
            return True
        return False

    @classmethod
    def get_user_cart(cls, user_id):
        """Get all cart items for a user"""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_cart_total(cls, user_id):
        """Calculate total price of all items in user's cart"""
        cart_items = cls.get_user_cart(user_id)
        return sum(item.product.price * item.quantity for item in cart_items)

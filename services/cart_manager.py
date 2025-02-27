from models import Cart, Product
from flask_login import current_user

class CartManager:
    @staticmethod
    def add_item(product_id, quantity=1):
        cart_item = Cart.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        product = Product.get_by_id(product_id)
        if not product.check_stock_availability(quantity):
            raise ValueError("Not enough stock available")
            
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
        
        cart_item.save()
        return cart_item
    
    @staticmethod
    def remove_item(product_id):
        cart_item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.delete()
            
    @staticmethod
    def get_user_cart():
        return Cart.query.filter_by(user_id=current_user.id).all()
    
    @staticmethod
    def calculate_total():
        cart_items = CartManager.get_user_cart()
        return sum(item.product.price * item.quantity for item in cart_items) 
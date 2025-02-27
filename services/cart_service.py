from models.cart import Cart
from models.product import Product
from models import db

class CartService:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        product = Product.query.get(product_id)
        if not product or product.stock < quantity:
            return False, "Not enough stock available"

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        return True, "Product added to cart"

    @staticmethod
    def update_cart_item(cart_item_id, action):
        cart_item = Cart.query.get(cart_item_id)
        if not cart_item:
            return False, "Cart item not found"

        if action == 'increase':
            if cart_item.quantity >= cart_item.product.stock:
                return False, "Not enough stock available"
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                db.session.delete(cart_item)

        db.session.commit()
        return True, "Cart updated successfully"

    @staticmethod
    def remove_from_cart(cart_item_id):
        cart_item = Cart.query.get(cart_item_id)
        if not cart_item:
            return False, "Cart item not found"

        db.session.delete(cart_item)
        db.session.commit()
        return True, "Item removed from cart"

    @staticmethod
    def get_cart_items(user_id):
        return Cart.get_user_cart(user_id)

    @staticmethod
    def get_cart_total(user_id):
        return Cart.get_cart_total(user_id)

    @staticmethod
    def clear_cart(user_id):
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit() 
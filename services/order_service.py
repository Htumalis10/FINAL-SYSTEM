from models.order import Order, OrderItem
from models.cart import Cart
from models.product import Product
from models import db

class OrderService:
    @staticmethod
    def create_order(user_id, payment_method):
        cart_items = Cart.get_user_cart(user_id)
        if not cart_items:
            return False, "Cart is empty"

        total = Cart.get_cart_total(user_id)
        
        # Verify stock availability
        for item in cart_items:
            if item.quantity > item.product.stock:
                return False, f"Not enough stock for {item.product.name}"

        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(order)

        # Create order items and update stock
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.update_stock(cart_item.quantity)

        # Clear cart
        Cart.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        return True, order.id

    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_order(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def update_order_status(order_id, new_status):
        order = Order.query.get(order_id)
        if not order:
            return False, "Order not found"

        success = order.update_status(new_status)
        if success:
            db.session.commit()
            return True, "Order status updated"
        return False, "Invalid status" 
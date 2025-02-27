from models import db, Order, OrderItem, Cart
from flask_login import current_user
import logging

logger = logging.getLogger(__name__)

class OrderManager:
    @staticmethod
    def create_order(payment_method, address, phone):
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        try:
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                payment_method=payment_method,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()
            
            for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                db.session.add(order_item)
                cart_item.product.stock -= cart_item.quantity
            
            # Clear cart
            for item in cart_items:
                db.session.delete(item)
                
            db.session.commit()
            return order
            
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_user_orders():
        return Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def update_order_status(order_id, status):
        order = Order.query.get_or_404(order_id)
        order.status = status
        db.session.commit()
        return order 
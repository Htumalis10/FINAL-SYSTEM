from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Order, OrderItem, Cart
from werkzeug.utils import secure_filename
import os
import logging
from services.order_manager import OrderManager
from services.cart_manager import CartManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders')
@login_required
def orders():
    logger.debug(f"Fetching orders for user_id: {current_user.id}")
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    logger.debug(f"Found {len(user_orders)} orders")
    return render_template('orders.html', orders=user_orders)

@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartManager.get_user_cart()
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.view_cart'))

    total = CartManager.calculate_total()
    
    if request.method == 'POST':
        try:
            payment_method = request.form.get('payment_method')
            address = request.form.get('address')
            phone = request.form.get('phone')
            
            order = OrderManager.create_order(payment_method, address, phone)
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.orders'))
            
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('orders.checkout'))
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@orders_bp.route('/gcash_payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def gcash_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        payment_screenshot = request.files.get('payment_screenshot')
        if payment_screenshot:
            filename = secure_filename(f'gcash_payment_{order_id}_{payment_screenshot.filename}')
            payment_screenshot.save(os.path.join('static/uploads', filename))
            
            order.status = 'processing'
            db.session.commit()
            
            logger.debug(f"Updated order status to 'processing' for order_id: {order_id}")
            flash('Payment proof uploaded successfully! Our team will verify your payment.', 'success')
            return redirect(url_for('orders.orders'))
        else:
            flash('Please upload your GCash payment screenshot', 'danger')
    
    return render_template('gcash_payment.html', order=order)

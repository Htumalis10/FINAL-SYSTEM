from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Order, OrderItem, Cart
from werkzeug.utils import secure_filename
import os
import logging

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
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.view_cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        logger.debug("Processing checkout POST request")
        payment_method = request.form.get('payment_method')
        address = request.form.get('address')
        phone = request.form.get('phone')

        logger.debug(f"Payment Method: {payment_method}, Address: {address}, Phone: {phone}")

        if not address or not phone:
            flash('Please provide delivery address and contact number', 'danger')
            return redirect(url_for('orders.checkout'))

        if payment_method not in ['gcash', 'cod']:
            flash('Invalid payment method', 'danger')
            return redirect(url_for('orders.checkout'))

        # Check stock availability
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                flash(f'Not enough stock for {cart_item.product.name}', 'danger')
                return redirect(url_for('cart.view_cart'))

        try:
            # Create the order
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                payment_method=payment_method,
                status='pending'
            )
            logger.debug(f"Created order object: {order.user_id}, {order.total_amount}, {order.payment_method}")
            db.session.add(order)
            db.session.flush()  # This gets us the order ID

            # Add order items and update stock
            for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                db.session.add(order_item)
                cart_item.product.stock -= cart_item.quantity
                logger.debug(f"Added order item: product_id={cart_item.product_id}, quantity={cart_item.quantity}")

            # Clear the cart
            for item in cart_items:
                db.session.delete(item)

            db.session.commit()
            logger.debug("Successfully committed order to database")

            if payment_method == 'gcash':
                return redirect(url_for('orders.gcash_payment', order_id=order.id))
            else:
                flash('Order placed successfully! Our team will contact you for delivery.', 'success')
                return redirect(url_for('orders.orders'))

        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            db.session.rollback()
            flash('An error occurred while processing your order. Please try again.', 'danger')
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

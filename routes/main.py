from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Product
from services.product_service import ProductService
from services.cart_service import CartService
from services.order_service import OrderService
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    category = request.args.get('category')
    products = ProductService.get_all_products(category)
    categories = ['Clothing', 'Accessories', 'Shoes', 'Bags']
    return render_template('home.html', products=products, categories=categories, selected_category=category)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = ProductService.get_product(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('main.home'))
    return render_template('product_detail.html', product=product)

@main_bp.route('/cart')
@login_required
def cart():
    cart_items = CartService.get_cart_items(current_user.id)
    total = CartService.get_cart_total(current_user.id)
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    success, message = CartService.add_to_cart(current_user.id, product_id, quantity)
    if success:
        flash('Product added to cart!', 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('main.cart'))

@main_bp.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    action = request.form.get('action')
    success, message = CartService.update_cart_item(item_id, action)
    if not success:
        flash(message, 'danger')
    return redirect(url_for('main.cart'))

@main_bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    success, message = CartService.remove_from_cart(item_id)
    if not success:
        flash(message, 'danger')
    return redirect(url_for('main.cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        success, result = OrderService.create_order(current_user.id, payment_method)
        
        if success:
            flash('Order placed successfully!', 'success')
            if payment_method == 'gcash':
                return redirect(url_for('main.gcash_payment', order_id=result))
            return redirect(url_for('main.orders'))
        else:
            flash(result, 'danger')
            return redirect(url_for('main.cart'))

    cart_items = CartService.get_cart_items(current_user.id)
    total = CartService.get_cart_total(current_user.id)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@main_bp.route('/orders')
@login_required
def orders():
    user_orders = OrderService.get_user_orders(current_user.id)
    return render_template('orders.html', orders=user_orders)

@main_bp.route('/gcash_payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def gcash_payment(order_id):
    order = OrderService.get_order(order_id)
    if not order or order.user_id != current_user.id:
        flash('Order not found or unauthorized access', 'danger')
        return redirect(url_for('main.orders'))

    if request.method == 'POST':
        payment_screenshot = request.files.get('payment_screenshot')
        if payment_screenshot:
            filename = f'gcash_payment_{order_id}_{payment_screenshot.filename}'
            payment_screenshot.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            success, message = OrderService.update_order_status(order_id, 'processing')
            if success:
                flash('Payment proof uploaded successfully!', 'success')
            else:
                flash(message, 'danger')
            return redirect(url_for('main.orders'))
        flash('Please upload your GCash payment screenshot', 'danger')

    return render_template('gcash_payment.html', order=order)

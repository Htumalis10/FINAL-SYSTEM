from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Cart, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('Not enough stock available', 'danger')
        return redirect(url_for('main.product_detail', id=product_id))
    
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first_or_404()
    quantity = int(request.form.get('quantity'))
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        if quantity > cart_item.product.stock:
            return jsonify({'error': 'Not enough stock available'}), 400
        cart_item.quantity = quantity
    
    db.session.commit()
    return jsonify({'success': True})

@cart_bp.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart.view_cart'))

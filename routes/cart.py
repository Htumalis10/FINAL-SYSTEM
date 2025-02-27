from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from services.cart_manager import CartManager

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartManager.get_user_cart()
    total = CartManager.calculate_total()
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        quantity = int(request.form.get('quantity', 1))
        CartManager.add_item(product_id, quantity)
        flash('Product added to cart!', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
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

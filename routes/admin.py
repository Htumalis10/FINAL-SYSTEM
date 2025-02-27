from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from models import db, Product
from utils.decorators import admin_required
from services.product_manager import ProductManager

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

@admin_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        try:
            ProductManager.create_product(
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=float(request.form.get('price')),
                category=request.form.get('category'),
                stock=int(request.form.get('stock')),
                image=request.files.get('image')
            )
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'danger')
    
    return render_template('admin/add_product.html')

@admin_bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.get_by_id(id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        try:
            ProductManager.update_product(
                product_id=id,
                data=request.form,
                image=request.files.get('image')
            )
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'danger')
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/delete_product/<int:id>')
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

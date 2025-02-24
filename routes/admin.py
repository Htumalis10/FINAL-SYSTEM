from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from models import db, Product
from utils.decorators import admin_required

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
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))
        image = request.files.get('image')
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', filename))
            image_url = f'/static/uploads/{filename}'
        else:
            image_url = None
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
            image_url=image_url
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_product.html')

@admin_bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        
        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', filename))
            product.image_url = f'/static/uploads/{filename}'
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
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

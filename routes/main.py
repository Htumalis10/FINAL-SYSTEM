from flask import Blueprint, render_template
from models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    products = Product.query.all()
    categories = set(p.category for p in products if p.category)
    category = request.args.get('category')
    
    if category:
        products = Product.query.filter_by(category=category).all()
    
    return render_template('index.html', products=products, categories=categories)

@main_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

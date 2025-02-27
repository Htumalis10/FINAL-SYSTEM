from models import db, Product
from werkzeug.utils import secure_filename
import os

class ProductManager:
    UPLOAD_FOLDER = 'static/uploads'
    
    @classmethod
    def create_product(cls, name, description, price, category, stock, image):
        image_url = cls._save_image(image) if image else None
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
            image_url=image_url
        )
        product.save()
        return product
    
    @classmethod
    def update_product(cls, product_id, data, image=None):
        product = Product.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
            
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.category = data.get('category', product.category)
        product.stock = int(data.get('stock', product.stock))
        
        if image:
            product.image_url = cls._save_image(image)
            
        product.save()
        return product
    
    @staticmethod
    def _save_image(image):
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(ProductManager.UPLOAD_FOLDER, filename))
            return f'/uploads/{filename}'
        return None
    
    @staticmethod
    def get_by_category(category):
        return Product.query.filter_by(category=category).all() 
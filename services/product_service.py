from models.product import Product
from models import db
import os
from werkzeug.utils import secure_filename

class ProductService:
    @staticmethod
    def get_all_products(category=None):
        if category:
            return Product.query.filter_by(category=category).all()
        return Product.query.all()

    @staticmethod
    def get_product(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create_product(data, image=None, upload_folder=None):
        try:
            image_url = None
            if image and upload_folder:
                filename = secure_filename(image.filename)
                image_path = os.path.join(upload_folder, filename)
                image.save(image_path)
                image_url = f'/static/uploads/{filename}'
            
            product = Product(
                name=data['name'],
                description=data['description'],
                price=float(data['price']),
                category=data['category'],
                stock=int(data['stock']),
                image_url=image_url or '/static/uploads/default.jpg'
            )
            
            db.session.add(product)
            db.session.commit()
            return True, product.id
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def update_product(product_id, data, image=None, upload_folder=None):
        try:
            product = Product.query.get(product_id)
            if not product:
                return False, "Product not found"

            product.name = data['name']
            product.description = data['description']
            product.price = float(data['price'])
            product.category = data['category']
            product.stock = int(data['stock'])

            if image and upload_folder:
                filename = secure_filename(image.filename)
                image_path = os.path.join(upload_folder, filename)
                image.save(image_path)
                product.image_url = f'/static/uploads/{filename}'

            db.session.commit()
            return True, "Product updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return False, "Product not found"

            db.session.delete(product)
            db.session.commit()
            return True, "Product deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e) 
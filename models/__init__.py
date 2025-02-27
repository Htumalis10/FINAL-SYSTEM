from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Import after db initialization to avoid circular imports
from .base_model import BaseModel
from .user import User
from .product import Product
from .cart import Cart
from .order import Order, OrderItem

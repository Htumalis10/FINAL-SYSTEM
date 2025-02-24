from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@thriftstore.com').first()
        if admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin = User(
            email='admin@thriftstore.com',
            password_hash=generate_password_hash('admin123'),  # Use password_hash field instead of password
            name='Admin',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Email: admin@thriftstore.com")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin()

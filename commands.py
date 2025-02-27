import click
from flask.cli import with_appcontext
from models import db, User
from werkzeug.security import generate_password_hash

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@click.argument('name')
@with_appcontext
def create_admin(email, password, name):
    """Create a new admin user"""
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_admin = True
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            click.echo(f'Existing user {email} has been promoted to admin')
        else:
            admin = User(
                email=email,
                password_hash=generate_password_hash(password),
                name=name,
                is_admin=True,
                address="Admin Address",
                phone="Admin Phone"
            )
            db.session.add(admin)
            db.session.commit()
            click.echo(f'Created new admin user: {email}')
    except Exception as e:
        click.echo(f'Error creating admin user: {str(e)}')

def init_app(app):
    app.cli.add_command(create_admin) 
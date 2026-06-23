from app import create_app, db
from models.user import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    existing = User.query.filter_by(email="admin@buspass.com").first()
    if existing:
        print("⚠️ Admin existe déjà !")
    else:
        hashed = bcrypt.generate_password_hash("Admin1234").decode('utf-8')
        admin = User(
            full_name="Admin",
            email="admin@buspass.com",
            phone="0600000000",
            password_hash=hashed,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin créé avec succès !")
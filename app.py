# ============================================================
#   CodeAlpha — Cloud-Based Bus Pass System
#   app.py : Point d'entrée principal
# ============================================================

from flask import Flask
from database import db, bcrypt, login_manager
import os

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'codealpha-buspass-secret-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'qrcodes')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Modèles
    from models.user import User
    from models.bus_pass import BusPass

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Créer les tables
    with app.app_context():
        db.create_all()

    # Blueprints
    from routes.auth import auth
    from routes.main import main
    from routes.passes import passes
    from routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(passes)
    app.register_blueprint(admin)

    # ✅ Expiration automatique toutes les 24h
    from apscheduler.schedulers.background import BackgroundScheduler
    from datetime import date

    def expire_passes():
        with app.app_context():
            passes_list = BusPass.query.filter_by(status='active').all()
            for p in passes_list:
                if p.end_date and p.end_date < date.today():
                    p.status = 'expired'
            db.session.commit()

    scheduler = BackgroundScheduler()
    scheduler.add_job(expire_passes, 'interval', hours=24)
    scheduler.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
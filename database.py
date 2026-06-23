# ============================================================
#   database.py — Configuration centralisée de la base de données
# ============================================================

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Créer UNE SEULE instance pour toute l'application
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Veuillez vous connecter.'
login_manager.login_message_category = 'warning'
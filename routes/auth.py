from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required
from app import db
from models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name        = request.form.get('full_name', '').strip()
        email            = request.form.get('email', '').strip().lower()
        phone            = request.form.get('phone', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([full_name, email, phone, password]):
            flash('Tous les champs sont obligatoires.', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Le mot de passe doit faire au moins 6 caractères.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(full_name=full_name, email=email, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('✅ Compte créé avec succès ! Connectez-vous maintenant.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user     = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'✅ Bienvenue {user.full_name} !', 'success')

            # ✅ Redirection directe par URL (évite les problèmes de préfixe)
            if user.role == 'admin':
                return redirect('/admin/dashboard')
            return redirect('/dashboard')
        else:
            flash('❌ Email ou mot de passe incorrect.', 'danger')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))
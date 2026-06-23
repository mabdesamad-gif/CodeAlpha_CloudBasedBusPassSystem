# ============================================================
#   routes/admin.py — Routes d'administration
# ============================================================

from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.bus_pass import BusPass
from functools import wraps
from datetime import datetime, timedelta
import qrcode
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Accès refusé. Admin requis.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_passes = BusPass.query.count()
    pending_passes = BusPass.query.filter_by(status='pending').count()
    active_passes = BusPass.query.filter_by(status='active').count()

    stats = {
        'total_users': total_users,
        'total_passes': total_passes,
        'pending_passes': pending_passes,
        'active_passes': active_passes,
    }

    recent_passes = BusPass.query.order_by(BusPass.created_at.desc()).limit(10).all()
    return render_template('admin_dashboard.html', stats=stats, passes=recent_passes)


@admin.route('/passes/approve/<int:pass_id>', methods=['POST'])
@login_required
@admin_required
def approve_pass(pass_id):
    bus_pass = BusPass.query.get_or_404(pass_id)
    bus_pass.status = 'active'

    # Dates
    bus_pass.start_date = datetime.now().date()
    if bus_pass.pass_type == 'monthly':
        bus_pass.end_date = (datetime.now() + timedelta(days=30)).date()
    elif bus_pass.pass_type == 'quarterly':
        bus_pass.end_date = (datetime.now() + timedelta(days=90)).date()
    else:
        bus_pass.end_date = (datetime.now() + timedelta(days=365)).date()

    # ✅ Générer le QR code
    qr_data = (
        f"PASS:{bus_pass.pass_number}\n"
        f"TRAJET:{bus_pass.route_from} → {bus_pass.route_to}\n"
        f"TYPE:{bus_pass.pass_type}\n"
        f"VALIDITE:{bus_pass.end_date}\n"
        f"USER:{bus_pass.owner.full_name}"
    )

    qr = qrcode.make(qr_data)

    # Dossier de sauvegarde
    qr_folder = os.path.join('static', 'qrcodes')
    os.makedirs(qr_folder, exist_ok=True)

    qr_filename = f"{bus_pass.pass_number}.png"
    qr_path = os.path.join(qr_folder, qr_filename)
    qr.save(qr_path)

    bus_pass.qr_code_path = f"qrcodes/{qr_filename}"

    db.session.commit()
    flash(f'✅ Pass {bus_pass.pass_number} approuvé avec QR code !', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/passes/reject/<int:pass_id>', methods=['POST'])
@login_required
@admin_required
def reject_pass(pass_id):
    bus_pass = BusPass.query.get_or_404(pass_id)
    bus_pass.status = 'rejected'
    db.session.commit()
    flash(f'❌ Pass {bus_pass.pass_number} rejeté.', 'warning')
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)
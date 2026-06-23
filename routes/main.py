# ============================================================
#   routes/main.py — Routes principales
# ============================================================

from flask import render_template, Blueprint
from flask_login import login_required, current_user
from models.bus_pass import BusPass

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    user_passes = BusPass.query.filter_by(user_id=current_user.id).all()
    stats = {
        'total': len(user_passes),
        'active': len([p for p in user_passes if p.status == 'active']),
        'pending': len([p for p in user_passes if p.status == 'pending']),
        'total_spent': sum(p.price for p in user_passes),
    }
    return render_template('dashboard.html', passes=user_passes, stats=stats)
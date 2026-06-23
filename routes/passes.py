# ============================================================
#   routes/passes.py — Gestion des Bus Pass
# ============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db
from models.bus_pass import BusPass
from models.user import User
import uuid
from datetime import datetime, timedelta

passes = Blueprint('passes', __name__, url_prefix='/passes')


@passes.route('/new', methods=['GET', 'POST'])
@login_required
def new_pass():
    """Créer un nouveau pass"""
    if request.method == 'POST':
        try:
            route_from = request.form.get('route_from')
            route_to = request.form.get('route_to')
            pass_type = request.form.get('pass_type')
            price_map = {'monthly': 450, 'quarterly': 1200, 'yearly': 4000}
            price = price_map.get(pass_type, 450)

            # Créer le pass
            bus_pass = BusPass(
                pass_number=f"PASS-{uuid.uuid4().hex[:8].upper()}",
                user_id=current_user.id,
                route_from=route_from,
                route_to=route_to,
                pass_type=pass_type,
                price=price,
                status='active'
            )
            
            bus_pass.calculate_valid_until()
            db.session.add(bus_pass)
            db.session.commit()

            flash('✅ Pass créé avec succès !', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur : {str(e)}', 'danger')
            return redirect(url_for('passes.new_pass'))

    return render_template('new_pass.html')


@passes.route('/list')
@login_required
def list_passes():
    """Lister tous les passes de l'utilisateur"""
    user_passes = BusPass.query.filter_by(user_id=current_user.id).all()
    return render_template('passes/list_passes.html', passes=user_passes)


@passes.route('/<int:pass_id>/details')
@login_required
def pass_details(pass_id):
    """Détails d'un pass"""
    bus_pass = BusPass.query.get_or_404(pass_id)
    
    if bus_pass.user_id != current_user.id:
        flash('❌ Accès refusé', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('passes/pass_details.html', pass_obj=bus_pass)


@passes.route('/<int:pass_id>/cancel', methods=['POST'])
@login_required
def cancel_pass(pass_id):
    """Annuler un pass"""
    bus_pass = BusPass.query.get_or_404(pass_id)
    
    if bus_pass.user_id != current_user.id:
        flash('❌ Accès refusé', 'danger')
        return redirect(url_for('main.dashboard'))
    
    bus_pass.status = 'cancelled'
    db.session.commit()
    
    flash('✅ Pass annulé avec succès !', 'success')
    return redirect(url_for('main.dashboard'))
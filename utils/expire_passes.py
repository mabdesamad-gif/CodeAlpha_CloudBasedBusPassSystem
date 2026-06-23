import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models.bus_pass import BusPass
from datetime import date

app = create_app()

with app.app_context():
    passes = BusPass.query.filter_by(status='active').all()
    expired_count = 0

    for p in passes:
        if p.end_date and p.end_date < date.today():
            p.status = 'expired'
            expired_count += 1

    db.session.commit()
    print(f"✅ {expired_count} pass(es) expiré(s) mis à jour.")
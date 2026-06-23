from app import db
from datetime import datetime, timedelta


class BusPass(db.Model):
    __tablename__ = 'bus_passes'

    id           = db.Column(db.Integer, primary_key=True)
    pass_number  = db.Column(db.String(20), unique=True, nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    route_from   = db.Column(db.String(100), nullable=False)
    route_to     = db.Column(db.String(100), nullable=False)
    pass_type    = db.Column(db.String(20), nullable=False)
    price        = db.Column(db.Float, nullable=False)
    status       = db.Column(db.String(20), default='pending')
    qr_code_path = db.Column(db.String(200), nullable=True)
    start_date   = db.Column(db.Date, nullable=True)
    end_date     = db.Column(db.Date, nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('User', backref='bus_passes', lazy=True)

    def __repr__(self):
        return f'<BusPass {self.pass_number}>'

    def calculate_valid_until(self):
        if self.start_date is None:
            return None
        if self.pass_type == 'monthly':
            month = self.start_date.month + 1
            year = self.start_date.year
            if month > 12:
                month = 1
                year += 1
            return self.start_date.replace(year=year, month=month)
        elif self.pass_type == 'weekly':
            return self.start_date + timedelta(weeks=1)
        elif self.pass_type == 'daily':
            return self.start_date + timedelta(days=1)
        else:
            return self.end_date

    @property
    def valid_until(self):
        return self.calculate_valid_until()
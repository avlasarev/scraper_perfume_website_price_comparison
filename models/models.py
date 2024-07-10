# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
#
# db = SQLAlchemy()
#
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     current_price = db.Column(db.Float, nullable=True)
#     url = db.Column(db.String(200), unique=True, nullable=False)
#     image = db.Column(db.String(200), nullable=True)
#     source = db.Column(db.String(50), nullable=False)
#
# class PriceHistory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#
#     product = db.relationship('Product', backref=db.backref('price_history', lazy=True))
#
# def flag_suspicious_prices(product_id):
#     # Implement logic to check for suspiciously low prices
#     price_threshold = 50.0
#     price_history = PriceHistory.query.filter_by(product_id=product_id).all()
#     suspicious_prices = [ph.price for ph in price_history if ph.price < price_threshold]
#     return suspicious_prices


# not using models for the suspicious prices used a comparer instead
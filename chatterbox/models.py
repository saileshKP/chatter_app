from chatterbox import db

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False)
	messages = db.relationship('Messages', backref='User')
	
class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String(500), nullable=False)
	datetime = db.Column(db.DateTime, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
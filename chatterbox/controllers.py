from flask import Flask, request, jsonify
from functools import wraps
from chatterbox import app, db
from chatterbox.models import Users, Messages
import datetime


def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	try:
		user_record = Users.query.filter_by(user_id=username).first()
		user_password = user_record.password
		
	except:
		return False
		
	if password == user_password:
		return True
	else:
		return False
		

def requires_auth(f):
	"""Decorator to check if user is authorized."""
	
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return jsonify({'message' : 'Invalid Credentials'}), 401
		return f(*args, **kwargs)
	return decorated


@app.route('/newuser', methods=['POST'])
def create_user():
	"""This function is called to create a new user"""
	
	user_data = request.get_json()
	
	try:
		new_user = Users(name=user_data['name'], user_id=user_data['user_id'], password=user_data['password'])
		db.session.add(new_user)
		db.session.commit()
	
	except:
		return jsonify({'message' : 'user creation failed - user_id already used or field empty'}), 400
	
	return jsonify({'msg' : 'New User created'}), 201

@app.route('/newmessage', methods=['POST'])
@requires_auth	
def create_message():
	"""This function is called to post a new message"""
	
	auth = request.authorization
	user = Users.query.filter_by(user_id=auth.username).first()
		
	
	try:
		message_data = request.get_json()		
		new_message = Messages(message=message_data['message'], datetime=datetime.datetime.now(), User=user)
		db.session.add(new_message)
		db.session.commit()
	
	except: 
		return jsonify({'message' : 'message posting failed - field empty'}), 400
	
	return jsonify({'msg' : 'New message posted'}), 201
	
@app.route('/messages', methods=['GET'])
@requires_auth
def list_messages():
	"""This function is called to list all messages"""
	
	messages_all = Messages.query.all()
	message_list = []
	for message_record in messages_all:
		user = message_record.User
		user_id = user.user_id
		message_data ={}
		message_data['user_id'] = user_id
		message_data['message'] = message_record.message
		message_list.append(message_data)
		
	return jsonify({'message_list' : message_list})
	

@app.route('/message/<int:message_id>', methods = ['GET'])
@requires_auth
def retrieve_message(message_id):
	"""This function is called to get a specific message /
	and check if it's pallindrome.
	"""
	try:
		message_record = Messages.query.filter_by(id=message_id).first()
		message_text = message_record.message
		
	except:
		return jsonify({'message' : 'Message not found'}), 404	
	
	def check_pallindrome(message):
		for i in range(0, int(len(message)/2)):
			if message[i] != message[len(message)-i-1]:
				return 'false'
		
		return 'true'
		
	return jsonify({'message' : message_text, 'Pallindrome' : check_pallindrome(message_text)})
	
	
@app.route('/message/<int:message_id>', methods=['DELETE'])
@requires_auth
def delete_message(message_id):
	"""This function is called to delete a message"""
	
	try:
		message_record = Messages.query.filter_by(id=message_id).first()
		db.session.delete(message_record)
		db.session.commit()		
	
	except:
		return jsonify({'message' : 'Message not found'}), 404		
	
		
	return jsonify({'message' : 'Message deleted'}), 204		
	
	
	
if __name__== '__main__':
	app.run(debug=True)
	

	
	
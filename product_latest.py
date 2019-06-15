from flask import Flask, request, flash, url_for, redirect
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from flask_bcrypt import Bcrypt

#####################
# Define App
#####################

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_latest.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
bc = Bcrypt()

#####################
# Define Data Models
#####################

class categories(db.Model):
	id = db.Column( db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(100))
	products = db.relationship('products', backref='catg', lazy=True)

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return 'Category('+ self.name + ' , ' + self.description + ')'

class products(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(50))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

	def __init__(self, name, description, category_id):
		self.name = name
		self.description = description
		self.category_id = category_id

	def __repr__(self):
		return 'Products('+ self.name + ' , ' + self.description + ' , ' + str(self.category_id) + ')'

class loginuser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	fname = db.Column(db.String(100), unique=False, nullable=False)
	lname = db.Column(db.String(100), unique=False, nullable=True)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	items = db.relationship('selleritem', backref='seller', lazy=True)

	def __init__(self, email, fname, lname, image_file, password):
		self.email = email
		self.fname = fname
		self.lname = lname
		self.image_file = image_file
		self.password = password

	def __repr__(self):
		return 'User(' + self.fname + self.lname + ', ' + self.email +')'

class selleritem(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	quantity = db.Column(db.Integer, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('loginuser.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

	def __init__(self, user_id, product_id, category_id, quantity, price):
		self.quantity = quantity
		self.price = price
		self.category_id = category_id
		self.product_id = product_id
		self.user_id = user_id

	def __repr__(self):
		return 'Items( prod_id:'+ str(self.product_id) + ' , catg_id:' + str(self.category_id) + ' , price:' + str(self.price) + ' , quantity:' + str(self.quantity) + ')'

#####################
# Define Endpoints
#####################

@app.route('/')
def show_all():
   return 'NinjaKart'

# PRODUCT LISTING
@app.route('/product', methods = ['GET', 'POST'])
def addProd():
	if request.method == 'POST':
		if not request.get_json().get('name'):
			return jsonify({'status': 'failed', 'message': 'Required field missing'})
		else:
			product = products(request.get_json().get('name'), request.get_json().get('description'), request.get_json().get('category_id'))
			db.session.add(product)
			db.session.commit()
			response = jsonify({'status': 'success'})
			return response
	row = []
	for i in range(len(products.query.all())):
		obj = {}
		obj['name'] = products.query.all()[i].name
		obj['id'] = products.query.all()[i].id
		obj['description'] = products.query.all()[i].description
		obj['category'] = products.query.all()[i].catg.name
		row.append(obj)
	response = jsonify(row)
	return response

@app.route('/product/<prodId>', methods = ['GET', 'DELETE'])
def deleteProd(prodId):
	if request.method == 'DELETE':
		data = products.query.filter_by(id=prodId).delete()
		db.session.commit()
		return jsonify({'status': 'success'})
	else:
		row = products.query.get(prodId)
		obj = {}
		obj['name'] = row.name
		obj['id'] = row.id
		obj['description'] = row.description
		obj['category'] = row.catg.name
		return jsonify(obj)

# CATEGORIES LISTING
@app.route('/categories', methods = ['GET', 'POST'])
def addCategories():
	if request.method == 'POST':
		if not request.get_json().get('name'):
			return jsonify({'status': 'failed', 'message': 'Required field missing'})
		else:
			catg = categories(request.get_json().get('name'), request.get_json().get('description'))
			db.session.add(catg)
			db.session.commit()
			return jsonify({'status': 'success'})
	row = []
	for i in range(len(categories.query.all())):
		obj = {}
		obj['name'] = categories.query.all()[i].name
		obj['id'] = categories.query.all()[i].id
		obj['description'] = categories.query.all()[i].description
		row.append(obj)
	response = jsonify(row)
	return response

@app.route('/categories/<catgId>', methods = ['GET', 'DELETE'])
def deleteCatg(catgId):
	if request.method == 'DELETE':
		data = categories.query.filter_by(id=catgId).delete()
		db.session.commit()
		return jsonify({'status': 'success'})
	else:
		row = []
		for u in categories.query.get(catgId):
			del u.__dict__['_sa_instance_state']
			row.append(u.__dict__)
		return jsonify(row)

# VENDOR ITEM LISTING

@app.route('/items', methods = ['GET', 'POST'])
def addGetItem():
	if request.method == 'POST':
		if not request.get_json().get('product_id') or not request.get_json().get('category_id') or not request.get_json().get('user_id'):
			return jsonify({'status': 'failed', 'message': 'Required field missing'})
		else:
			catg = selleritem(request.get_json().get('user_id'), request.get_json().get('product_id'), request.get_json().get('category_id'), request.get_json().get('quantity'), request.get_json().get('price'))
			db.session.add(catg)
			db.session.commit()
			return jsonify({'status': 'success'})
	data = []
	query = selleritem.query.join(products, selleritem.product_id==products.id).add_columns(products.name).join(categories, selleritem.category_id==categories.id).add_columns(categories.name)
	for row in query:
		obj = {}
		obj['id'] = row[0].id
		obj['quantity'] = row[0].quantity
		obj['price'] = row[0].price
		obj['user_id'] = row[0].user_id
		obj['category_id'] = row[0].category_id
		obj['product_id'] = row[0].product_id
		obj['product'] = row[1]
		obj['category'] = row[2]
		data.append(obj)
	return jsonify(data)

@app.route('/items/<itemId>', methods = ['GET', 'DELETE'])
def getNdDeleteItem(itemId):
	if request.method == 'DELETE':
		data = selleritem.query.filter_by(id=itemId).delete()
		db.session.commit()
		return jsonify({'status': 'success'})
	else:
		# row = selleritem.query.get(itemId)
		row = selleritem.query.join(products, selleritem.product_id==products.id).add_columns(products.name).join(categories, selleritem.category_id==categories.id).add_columns(categories.name).one()
		obj = {}
		obj['id'] = row[0].id
		obj['quantity'] = row[0].quantity
		obj['price'] = row[0].price
		obj['user_id'] = row[0].user_id
		obj['category_id'] = row[0].category_id
		obj['product_id'] = row[0].product_id
		obj['product'] = row[1]
		obj['category'] = row[2]
		return jsonify(obj)

@app.route('/register', methods = ['POST'])
def createUser():
	if request.method == 'POST':
		if not request.get_json().get('email') or not request.get_json().get('password'):
			return jsonify({'status': 'failed', 'message': 'Required field username/password missing!'})
		else:
			encrypted_password = bc.generate_password_hash(request.get_json().get('password')).decode('utf-8')
			u = loginuser(request.get_json().get('email'), request.get_json().get('fname'),request.get_json().get('lname'),
				request.get_json().get('image_file'),encrypted_password)
			db.session.add(u)
			db.session.commit()
			return jsonify({'status': 'success'})

@app.route('/login', methods = ['POST'])
def loginUser():
			print(request.get_json().get('email'))
			user_obj = loginuser.query.filter(loginuser.email == request.get_json().get('email')).one()
			print(user_obj)
			auth = bc.check_password_hash(user_obj.password,request.get_json().get('password'))
			if auth == True:
				obj = {}
				obj['email'] = user_obj.email
				obj['fname'] = user_obj.fname
				obj['lname'] = user_obj.lname
				return jsonify({'status': 'success', 'data': obj})
			return jsonify({'status': 'failed'})

#####################
# Entrypoint
#####################

if __name__ == '__main__':
	db.create_all()
	app.run()


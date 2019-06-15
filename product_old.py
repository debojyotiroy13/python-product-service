from flask import Flask, request, flash, url_for, redirect, render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.sqlite3'
app.config['SECRET_KEY'] = "asdjkbakjsbdjkbakds"

db = SQLAlchemy(app)
class users(db.Model):
	__tablename__ = "USERS"
	id = db.Column('user_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	city = db.Column(db.String(50))  
	email = db.Column(db.String(200))
	password = db.Column(db.String(10))

	def __init__(self, name, city, email,passowrd):
		self.name = name
		self.city = city
		self.email = email
		self.passowrd = passowrd

class products(db.Model):
	__tablename__ = "PRODUCTS"
	id = db.Column('product_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(50))  
	price = db.Column(db.Integer)
	category = db.Column(db.String(50))
	#category_id = db.Column(db.Integer, db.ForeignKey("CATEGORIES.catg_id"))
	#category = db.relationship("categories")

	def __init__(self, name, description, price, category):
		self.name = name
		self.description = description
		self.price = price
		self.category = category

class categories(db.Model):
	__tablename__ = "CATEGORIES"
	id = db.Column('catg_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(100))

	def __init__(self, name, description):
		self.name = name
		self.description = description

@app.route('/')
def show_all():
   return render_template('<H1>PRODUCT CATALOG SERVICE/H1>')

@app.route('/product', methods = ['GET', 'POST'])
def addProd():
	if request.method == 'POST':
		if not request.get_json().get('name'):
			return jsonify({'status': 'failed', 'message': 'Required field missing'})
		else:
			product = products(request.get_json().get('name'), request.get_json().get('description'),request.get_json().get('price'), request.get_json().get('category'))
			db.session.add(product)
			db.session.commit()
			return jsonify({'status': 'success'})
	row = []
	for u in products.query.all():
		del u.__dict__['_sa_instance_state']
		row.append(u.__dict__)
	return jsonify(row)

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
	for u in categories.query.all():
		print(u.__dict__)
		del u.__dict__['_sa_instance_state']
		row.append(u.__dict__)
	return jsonify(row)

@app.route('/product/<prodId>', methods = ['GET', 'DELETE'])
def deleteProd(prodId):
	if request.method == 'DELETE':
		data = products.query.filter_by(id=prodId).delete()
		db.session.commit()
		return jsonify({'status': 'success'})
	else:
		row = []
		for u in products.query.get(prodId):
			print(u.__dict__)
			del u.__dict__['_sa_instance_state']
			row.append(u.__dict__)
		return jsonify(row)

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)
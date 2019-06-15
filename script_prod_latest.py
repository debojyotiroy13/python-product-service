from tutorial_app import db
db.create_all()
from tutorial_app import User, Post
user_1 = User(username="debo", email="debo@gmail.com",password="password")
user_2 = User(username="nikhil", email="nikhil@gmail.com",password="password")
db.session.add(user_1)
db.session.add(user_2)
db.session.commit()
User.query.all()
user = User.query.get(1)

post_1 = Post(title='Blog 1', content='Story of life', user_id=1)
post_2 = Post(title='Blog 2', content='Story of life 2', user_id=2)
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()



from product_latest import db
db.create_all()
from product_latest import user, selleritem
user1 = user( 'debo@gmail.com', 'Debo', 'Roy', 'default.jpg' , 'password')
user2 = user( 'bhavya@gmail.com', 'Bhavya', 'Sankala', 'default.jpg' , 'password')
db.session.add(user1)
db.session.add(user2)
db.session.commit()
user.query.all()

from product_latest import db
db.create_all()
from product_latest import user, selleritem
item1 = selleritem(1, 50000, 1, 1, 1)
db.session.add(item1)
db.session.commit()

from product_latest import db
from product_latest import user, selleritem, products
selleritem.query.all()
selleritem.query.join(products, selleritem.product_id==products.id).add_columns(products.name).join(categories, selleritem.category_id==categories.id).add_columns(categories.name).all()
selleritem.query.join(products, selleritem.product_id==products.id).add_columns(products.name).all()

from flask_bcrypt import Bcrypt
bc = Bcrypt()
bc.generate_password_hash('password')
bc.generate_password_hash('password').decode('utf-8')
h = bc.generate_password_hash('password').decode('utf-8')
bc.check_password_hash(h,'password')





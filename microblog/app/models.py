from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), index=True, unique=True, nullable=False)
	email = db.Column(db.String(120), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	level = db.Column(db.Integer, default=1)
	points = db.Column( db.Integer, default=0 )

	def set_password( self, password ):
		self.password_hash = generate_password_hash( password )
	
	def check_password( self, password ):
		return check_password_hash( self.password_hash, password )
	
class BlogPost( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	title = db.Column( db.String(140), nullable=False )
	content = db.Column( db.Text, nullable=False )
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
	user_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False )

	user = db.relationship( 'User', backref='posts' )

class Comment( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	content = db.Column( db.Text, nullable=False )
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
	user_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False )
	post_id = db.Column( db.Integer, db.ForeignKey('blog_post.id'), nullable=False )
	parent_id = db.Column( db.Integer, db.ForeignKey('comment.id'), nullable=True )

	user = db.relationship( 'User', backref='comments' )
	post = db.relationship( 'BlogPost', backref='comments' )
	parent = db.relationship( 'Comment', remote_side=[id], backref='replies' )


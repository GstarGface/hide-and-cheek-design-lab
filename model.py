"""Models and database functions for DesignLab"""

from flask_sqlalchemy import SQLAlchemy 

from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

######################################
#Model Definitions: Style/Size/Cut/Waist/Fabric/Color/Stitch/Thread/Design/Order/Admins

class Style(db.Model):
	"""Style options"""

	__tablename__ = "styles"

	style_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	style_name = db.Column(db.String(50), nullable=False)
	style_description = db.Column(db.String(200), nullable=False)
	style_svg = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Style: style_id = %s style_name = %s>" % (self.style_id, self.style_name)


class StyleAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['style_id', 'style_name', 'style_description', 'style_svg', 'discontinued']


class Size(db.Model):
	"""Size options"""

	__tablename__ = "sizes"

	size_code = db.Column(db.String(2), autoincrement=True, primary_key=True)
	size = db.Column(db.String(20), nullable=False)
	size_description = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Size: size_code = %s>" % self.size_code

class SizeAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['size_code', 'size', 'size_description', 'discontinued']



class Waist(db.Model):
	"""Waist height options"""

	__tablename__ = "waists"

	waist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	waist_name = db.Column(db.String(50), nullable=False)
	waist_description = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Waist: waist_id = %s waist_name = %s>" % (self.waist_id, self.waist_name)

class WaistAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['waist_id', 'waist_name', 'waist_description', 'discontinued']


class Fabric(db.Model):
	"""Fabric options"""

	__tablename__ = "fabrics"

	fabric_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	fabric_name = db.Column(db.String(50), nullable=False)
	fabric_description = db.Column(db.String(800), nullable=False)
	fabric_thumbnail = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Fabric: fabric_id = %s fabric_name = %s >" % (self.fabric_id, self.fabric_name)

class FabricAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['fabric_id', 'fabric_name', 'fabric_description', 'fabric_thumbnail', 'discontinued']


class Color(db.Model):
	"""Color options for each fabric"""
	__tablename__ = "colors"

	color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	color_name = db.Column(db.String(50), nullable=False)
	fabric_id = db.Column(db.Integer, db.ForeignKey('fabrics.fabric_id'), nullable=False)
	color_hex = db.Column(db.String(20), nullable=False)
	color_thumbnail = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	#Defines relationship to the Fabric class
	fabric = db.relationship("Fabric", backref=db.backref("colors"))

	def __repr__(self):
		"""Quick reference when printed"""
		return "<Color: color_id = %s color_name = %s fabric_id = %s>" % (self.color_id, self.color_name, self.fabric_id)

class ColorAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['color_id', 'color_name', 'color_hex', 'color_thumbnail', 'discontinued']


class Embroidery(db.Model):
	"""Embroidery options"""

	__tablename__ = "embroidery"

	embroidery_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	embroidery_location = db.Column(db.String(50), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Embroidery: embroidery_id = %s embroidery_location = %s >" % (self.embroidery_id, self.embroidery_location)

class EmbroideryAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['embroidery_id', 'embroidery_location', 'discontinued']

class Stitching(db.Model):
	"""Stitching options"""

	__tablename__ = "stitching"

	stitching_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	stitching_style = db.Column(db.String(50), nullable=False)
	thumbnail = db.Column(db.String(200), nullable=True)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Stitching: stitching_id = %s stitching_style = %s >" % (self.stitching_id, self.stitching_style)

class StitchingAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['stitching_id', 'stitching_style', 'thumbnail', 'discontinued']



class Thread(db.Model):
	"""Thread color options"""

	__tablename__ = "threads"

	thread_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	thread_color = db.Column(db.String(50), nullable=False)
	thread_hex = db.Column(db.String(10), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Thread Color: thread_id = %s thread_color = %s >" % (self.thread_id, self.thread_color)

class ThreadsAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['thread_id', 'thread_color', 'thread_hex', 'discontinued']



class Design(db.Model):
	"""User generated designs"""
	__tablename__ = "designs"

	design_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	style_id = db.Column(db.Integer, db.ForeignKey('styles.style_id'), nullable=False)
	size_code = db.Column(db.String(2), db.ForeignKey('sizes.size_code'), nullable=False)
	waist_id = db.Column(db.Integer, db.ForeignKey('waists.waist_id'), nullable=False)
	fabric_id = db.Column(db.Integer, db.ForeignKey('fabrics.fabric_id'), nullable=False)
	color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), nullable=False)
	embroidery_id = db.Column(db.Integer, db.ForeignKey('embroidery.embroidery_id'), nullable=True)
	stitching_id = db.Column(db.Integer, db.ForeignKey('stitching.stitching_id'), nullable=True)

	#Defines class relationships
	style = db.relationship("Style", backref=db.backref("designs"))
	size = db.relationship("Size", backref=db.backref("designs"))
	waist = db.relationship("Waist", backref=db.backref("designs"))
	fabric = db.relationship("Fabric", backref=db.backref("designs"))
	color = db.relationship("Color", backref=db.backref("designs"))
	embroidery = db.relationship("Embroidery", backref=db.backref("designs"))
	stitching = db.relationship("Stitching", backref=db.backref("designs"))

class Order(db.Model):
	"""Order information for fulfillment portal"""
	__tablename__ = "orders"

	order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	design_id = db.Column(db.Integer, db.ForeignKey('designs.design_id'), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(800), nullable=False)
	state = db.Column(db.String(10), nullable=False)
	zipcode = db.Column(db.Integer, nullable=False)

	design = db.relationship("Design", backref=db.backref("orders"))


#######################################
#Helper functions

def connect_to_db(app):
	"""Connects db to flask app."""

	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://georgia@localhost/designlab')
	db.app = app
	db.init_app(app)

if __name__ == '__main__':
	#Enables running this module interactively to interact directly w/ the database.

	from design_lab import app
	connect_to_db(app)
	print "Connected to DesignLab DB."

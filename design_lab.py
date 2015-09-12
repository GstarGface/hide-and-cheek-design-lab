"""The Design Lab server!"""
import os
import json

from time import time

from jinja2 import StrictUndefined 

from flask import Flask, render_template, redirect, request, flash, session, jsonify

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_debugtoolbar import DebugToolbarExtension
from instagram import client

from model import Style, Size, Waist, Fabric, Color, Embroidery, Stitching, Thread, connect_to_db, db, StyleAdmin, SizeAdmin, WaistAdmin, FabricAdmin, ColorAdmin, EmbroideryAdmin, StitchingAdmin, ThreadsAdmin
import shopify

app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
# app.secret_key = "ommmnamasteshantishantishanti" 
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev")


app.jinja_env.globals.update(time=time)

#configure the Instagram API
instaConfig = {
	'client_id':os.environ.get('INSTAGRAM_CLIENT_ID'),
	'client_secret':os.environ.get('INSTAGRAM_CLIENT_SECRET'),
	'redirect_uri':os.environ.get('REDIRECT_URI')	
}

api = client.InstagramAPI(**instaConfig)

API_KEY = os.environ.get('SHOPIFY_API_KEY')
PASSWORD = os.environ.get('SHOPIFY_PASSWORD')
shop_url = "https://%s:%s@hide-cheek.myshopify.com/admin" % (API_KEY, PASSWORD)
shopify.ShopifyResource.set_site(shop_url)


@app.route('/')
def index():
	"""Landing page"""

	session['current_design'] = {
		"style_id": None,
		"style_svg": "newnaked.svg",
		"size_code": None,
		"waist_id": "2",
		"fabric_id": None,
		"color_id": None,
		"color_hex": None,
		"embroidery_text": None,
		"embroidery_place":None,
		"stitching_style": None,
		"thread_color": None,
		"suggestions": None
		}
	return render_template("landing_page.html")


@app.route('/step1', methods=["GET", "POST"])
def step_one():
	"""Form to choose style, size, cut, waist"""

	styles = Style.query.filter(Style.discontinued == False).order_by(Style.style_id).all()
	sizes = Size.query.filter(Size.discontinued == False).order_by(Size.size_description).all()
	waists = Waist.query.filter(Waist.discontinued == False).order_by(Waist.waist_id).all()
	
	
	return render_template("step1.html", styles=styles, sizes=sizes, waists=waists)


@app.route('/current-design.json')
def current_design():
	"""JSON information about the current user's design"""

	return jsonify(session['current_design'])


@app.route('/styles.json')
def styles():
	"""Returns style options from db via JSON"""

	styles = db.session.query(Style.style_svg, Style.style_id).order_by(Style.style_id).all()

	return jsonify({"styles": styles})


@app.route('/suggestions', methods=["POST"])
def suggestions():
	"""Adds custom sizing suggestions to session"""

	session['current_design']['suggestions']= request.form.get('suggestions')

	print "\n\n\n"
	print session['current_design']['suggestions'] 
	print "\n\n\n"

	return jsonify(session['current_design'])


@app.route('/step2', methods=["GET", "POST"])
def step_two():
	"""Form to choose fabric"""


	session['current_design']['style_id'] = request.form.get('style')
	session['current_design']['size_code'] = request.form.get('size')
	session['current_design']['style_svg'] = request.form.get('style-svg')
	session['current_design']['waist_id'] = request.form.get('waist')

	print "\n\n\n"
	print session['current_design']['waist_id'] 
	print "\n\n\n"
	

	fabrics = Fabric.query.filter(Fabric.discontinued == False).all()
	return render_template("step2.html", fabrics=fabrics)


@app.route('/step3', methods=["GET", "POST"])
def step_three():
	"""Last form: choose fabric color and custom embroidery"""

	session['current_design']['fabric_id'] = request.form.get('fabric')
	fab_id = session['current_design']['fabric_id']

	colors = Color.query.filter(Color.fabric_id==fab_id, Color.discontinued == False).all()
	embroidery = Embroidery.query.filter(Embroidery.discontinued == False).all()
	stitch = Stitching.query.filter(Stitching.discontinued == False).order_by(Stitching.stitching_id).all()
	thread = Thread.query.filter(Thread.discontinued == False).order_by(Thread.thread_id).all()

	return render_template("step3.html", colors=colors, embroidery=embroidery, stitch=stitch, thread=thread)



@app.route('/myDesignLab', methods=["GET", "POST"])
def my_design():
	"""Display the finished design with options to save or purchase"""

	session['current_design']['color_id'] = request.form.get('color')
	session['current_design']['color_hex'] = request.form.get('hex')
	session['current_design']['embroidery_text'] = request.form.get('embroidery')
	session['current_design']['embroidery_place'] = request.form.get('emb-place')
	session['current_design']['stitching_style'] = request.form.get('stitch')
	session['current_design']['thread_color'] = request.form.get('thread')

	print "\n\n\n"
	print session['current_design']  
	print "\n\n\n"

	return render_template("myDesignLab.html")


@app.route('/added', methods=['GET', 'POST'])
def added():
	"""Adds the current session to the shopping cart."""

	status = "design added to cart!"
	return json.dumps({'status': status})


@app.route('/newDesign')
def new():

	session['current_design'] = {
		"style_id": None,
		"style_svg": "newnaked.svg",
		"size_code": None,
		"waist_id": "2",
		"fabric_id": None,
		"color_id": None,
		"color_hex": None,
		"embroidery_text": None,
		"embroidery_place": None,
		"stitching_style": None,
		"thread_color": None,
		"suggestions": None
		}

	return redirect('/step1')

@app.route('/selections.json')
def selections():
	"""Returns design details from db via JSON"""

	style_sesh = session['current_design']['style_id']
	style = db.session.query(Style.style_name).filter(Style.style_id==style_sesh).one()
	
	size_sesh = session['current_design']['size_code']
	size = db.session.query(Size.size).filter(Size.size_code==size_sesh).one()

	waist_sesh = session['current_design']['waist_id']
	waist = db.session.query(Waist.waist_name).filter(Waist.waist_id==waist_sesh).one()

	fab_sesh = session['current_design']['fabric_id']
	fabric = db.session.query(Fabric.fabric_name).filter(Fabric.fabric_id==fab_sesh).one()

	color_sesh = session['current_design']['color_id']
	color = db.session.query(Color.color_name).filter(Color.color_id==color_sesh).one()

	place_sesh = session['current_design']['embroidery_place']

	stitch_sesh = session['current_design']['stitching_style']

	thread_sesh = session['current_design']['thread_color']

	text_sesh = session['current_design']['embroidery_text']

	return jsonify({"selections": {"style": style[0], 
								   "size": size[0],
								   "waist":waist[0],
								   "fabric":fabric[0],
								   "color":color[0],
								   "placement": place_sesh,
								   "stitch": stitch_sesh,
								   "thread":thread_sesh,
								   "text": text_sesh,
								   "suggestions": session['current_design']['suggestions']
								   }
					})


@app.route('/Lookbook', methods=["GET", "POST"])
def lookbook():
	"""Display most-recent Instagram images with the hideandcheek hashtag""" #FIXME : make this the *most-liked* insta images, not just the most recent



	our_recent_media, next = api.user_recent_media(user_id="1558910306", count=60)
	for media in our_recent_media:
		print media

	print "\n\n\n\n"

	tagged_media, next = api.tag_recent_media(count=60, tag_name='superfoodoffashion')
	print tagged_media
	for n in tagged_media:
		print n


	lookbookData = {
			'our_media' : our_recent_media,
			'tagged' : tagged_media
	}

	print lookbookData

	return render_template('lookbook.html', **lookbookData )
	


##################################################

if __name__ == "__main__":
    
    app.debug = False #Switch to False when demo/deploying!!!!

    connect_to_db(app)

    #Create admin
	#Add more administrative views here
    admin = Admin(app, name='designlab', template_mode='bootstrap3')
    admin.add_view(StyleAdmin(Style, db.session))
    admin.add_view(SizeAdmin(Size, db.session))
    admin.add_view(WaistAdmin(Waist, db.session))
    admin.add_view(FabricAdmin(Fabric, db.session))
    admin.add_view(ColorAdmin(Color, db.session))
    admin.add_view(EmbroideryAdmin(Embroidery, db.session))
    admin.add_view(StitchingAdmin(Stitching, db.session))
    admin.add_view(ThreadsAdmin(Thread, db.session))


    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
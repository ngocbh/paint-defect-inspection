import os
import mongoengine as mge

from flask import Flask, abort, session, request, redirect
from flask.json import jsonify
UPLOAD_FOLDER = 'upload'

app = Flask(__name__, template_folder="../templates/BS3", static_folder="../templates/BS3", static_url_path="")
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.secret_key = "secret key"

# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# mge.connect('doulingo_demo', host='localhost', port=27017)

from server.routes import *
from server.services import *

init_services(app)

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	print("Start..")
	app.debug = True
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])

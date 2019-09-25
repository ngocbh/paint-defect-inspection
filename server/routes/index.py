from server import app
from flask import render_template
from flask import Flask, abort, session, request, redirect
from server.utils.parameters import *
from server.utils.utils import get_listdir
import xml.etree.ElementTree as ET
import time


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
	return render_template('dashboard.html')

@app.route('/prototype', methods = ['GET', 'POST'])
def render_prototype():
	return render_template('prototype.html', notification='Welcome to prototype')

@app.route('/car', methods = ['GET', 'POST'])
def show_result():
	dirbase=request.args.get('name')
	overviews = []
	defects = []

	absworkingdir=os.path.join(STATIC_DIR,STATIC_USER_DIR)

	listcar = get_listdir(absworkingdir)

	if dirbase == None:
		return render_template('car.html', showcar='none', showlist='block', lenlistcar=len(listcar), listcar=listcar, 
			len_df=len(defects), defects=defects, 
			len_ov=len(overviews), overviews=overviews, notification='Render Failed: No car to show')

	workingdir=os.path.join(STATIC_USER_DIR,dirbase)
	absworkingdir=os.path.join(absworkingdir,dirbase)
	tree = ET.parse(os.path.join(absworkingdir, 'metadata-results.xml'))
	root = tree.getroot()

	
	overviews_et = next(root.iter('overview'))
	for overview_et in overviews_et:
		filename = overview_et.find('name').text
		filebase = os.path.splitext(overview_et.find('name').text)[0]
		filepath = os.path.join(workingdir,'{}_inferred.jpg'.format(filebase))
		overviews.append(filepath)

	
	for image in root.iter('image'):
		filename = image.find('name').text
		filebase = os.path.splitext(image.find('name').text)[0]
		filepath = os.path.join(workingdir,'{}_inferred.jpg'.format(filebase))
		defects.append(filepath)

	print(overviews, defects)
	print('carroute')
	return render_template('car.html', showcar='block', showlist='none',  lenlistcar=len(listcar), listcar=listcar,
	    len_df=len(defects), defects=defects, 
		len_ov=len(overviews), overviews=overviews, notification='Render Sucessfully')

@app.route('/dashboard', methods = ['GET', 'POST'])
def render_dashboard():
	return render_template('dashboard.html')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return app.send_static_file('500.html')

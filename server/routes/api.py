from server import app
from flask import render_template
from flask import Flask, abort, session, request, redirect
from werkzeug import secure_filename
from server.utils.parameters import *
from server.services import projector

import os
import time 

@app.route('/api/upload', methods = ['GET', 'POST'])
def upload_file_1():
	print(request.method)
	if request.method == 'POST':
		f = request.files['file']
		print(USER_DIR)
		print(f.filename)
		print(os.path.join(USER_DIR,f.filename))
		try:
			os.mkdir(USER_DIR)
		except OSError:
			pass
		# time.sleep(4)
		filename = secure_filename(f.filename)
		filebase = os.path.splitext(filename)[0]
		filepath = os.path.join(USER_DIR,filename)
		f.save(filepath)
		projector.process(filepath, filebase)
		# overviews =[]
		# defects=[]
		return redirect('/car?name={}'.format(filebase))
	else:
		return 'nothing to upload'


# from __future__ import absolute_import
import sys
sys.path.append('/Users/ngocjr/Workspace/Project/computervision/paint-defect-inspection/')

from server.utils.parameters import *

from zipfile import ZipFile

import xml.etree.ElementTree as ET
import os
import requests
import json
import shutil 
import cv2

def mark_car(filepath, filebase):
	workingdir = os.path.join(USER_DIR,filebase)

	tree = ET.parse(os.path.join(workingdir, 'metadata-results.xml'))
	root = tree.getroot()

	overview = next(root.iter('overview'))
	for view in overview:
		filename = view.find('name').text
		filebase = os.path.splitext(view.find('name').text)[0]
		view_img = cv2.imread(os.path.join(workingdir,filename))
		vsz = view_img.shape[0]
		x = float(view.find('x').text)
		y = float(view.find('y').text)
		z = float(view.find('z').text)
		normal = view.find('normal')
		nx = float(normal.find('x').text)
		ny = float(normal.find('y').text)
		nz = float(normal.find('z').text)
		coor = (x,y,z,(nx,ny,nz))

		for image in root.iter('image'):
			im_filename = image.find('name').text
			im_img = cv2.imread(os.path.join(workingdir,im_filename))
			isz = im_img.shape[0]
			ix = float(image.find('x').text)
			iy = float(image.find('y').text)
			iz = float(image.find('z').text)
			inormal = image.find('normal')
			inx = float(inormal.find('x').text)
			iny = float(inormal.find('y').text)
			inz = float(inormal.find('z').text)

			if nx == inx and ny == iny and nz == inz:
				# print(filebase, nx, ny, nz, inx, iny, inz, im_filename)
				for defect in image.findall('defect'):
					conf = float(defect.find('confidence').text)
					xmin = int(defect.find('xmin').text)
					ymin = int(defect.find('ymin').text)
					xmax = int(defect.find('xmax').text)
					ymax = int(defect.find('ymax').text)
					# print(xmin, ymin, xmax, ymax, isz)

					mo1 = ((isz/2 - xmin) * 10/float(isz))
					mo2 = ((isz/2 - ymin) * 10/float(isz))
					# print(mo1, mo2)
					# print(xmin, ymin, isz/2)

					m1 = (0,0,0)

					if view.tag == 'front':
						m1 = (ix - mo1, iy, iz + mo2)
					elif view.tag == 'left':
						m1 = (ix, iy + mo1, iz + mo2)
					elif view.tag == 'back':
						m1 = (ix + mo1, iy, iz + mo2)
					elif view.tag == 'right':
						m1 = (ix, iy - mo1, iz + mo2)

					# print("i=",(ix,iy,iz))
					# print("m1=",m1)

					# print("vx=", (x,y,z))
					dx = (x - m1[0])/(245/float(vsz))
					dy = (y - m1[1])/(245/float(vsz))
					dz = (z - m1[2])/(245/float(vsz))
					ret = (0,0)
					# print("d=", (dx,dy,dz))

					if view.tag == 'front':
						ret = (vsz/2 - dx, vsz/2 + dz)
					elif view.tag == 'left':
						ret = (vsz/2 + dy, vsz/2 + dz)
					elif view.tag == 'back':
						ret = (vsz/2 + dx,vsz/2 + dz)
					elif view.tag == 'right':
						ret = (vsz/2 - dy, vsz/2 + dz)

					ret = (int(ret[0]), int(ret[1]))

					# print('tam=', (vsz/2, vsz/2))
					# print("ret=", ret)

					cv2.rectangle(view_img, ret, (ret[0] + 100, ret[1] + 100), (92, 0, 255), 8)
					font = cv2.FONT_HERSHEY_SIMPLEX
					# cv2.putText(view_img,str(round(conf,4)), (ret[0], ret[1]-20), font, 2 ,(92, 0, 255), 4)

		cv2.imwrite(os.path.join(workingdir, '{}_inferred.jpg'.format(filebase)), view_img)
		# print('_________________')



def process(filepath, filebase):	
	try:
		os.mkdir(os.path.join(USER_DIR,filebase))
	except OSError:
		pass
	with ZipFile(filepath, 'r') as zipObj:
		# Extract all the contents of zip file in current directory
		zipObj.extractall(os.path.join(USER_DIR,filebase))

	workingdir = os.path.join(USER_DIR,filebase)
	tree = ET.parse(os.path.join(workingdir, 'metadata.xml'))
	root = tree.getroot()

	for image in root.iter('image'):
		image_path = os.path.join(workingdir, image.find('name').text)
		image_base = os.path.splitext(image.find('name').text)[0]
		files = {'files': open(image_path, 'rb')}
		response = requests.post(POWERAI_VISION_API, files=files, verify=False)
		d = json.loads(response.text)
		img = cv2.imread(image_path)

		font = cv2.FONT_HERSHEY_SIMPLEX
		for defect in d['classified']:
			print(defect)
			d_e = ET.SubElement(image, 'defect')
			conf_e = ET.SubElement(d_e, 'confidence')
			conf_e.text = str(defect['confidence'])
			label_e = ET.SubElement(d_e, 'label')
			label_e.text = str(defect['label'])
			xmin_e = ET.SubElement(d_e, 'xmin')
			xmin_e.text = str(defect['xmin'])
			xmax_e = ET.SubElement(d_e, 'xmax')
			xmax_e.text = str(defect['xmax'])
			ymin_e = ET.SubElement(d_e, 'ymin')
			ymin_e.text = str(defect['ymin'])
			ymax_e = ET.SubElement(d_e, 'ymax')
			ymax_e.text = str(defect['ymax'])
			# d_e.extend([conf_e,label_e,xmin_e,xmax_e,ymin_e,ymax_e])
			cv2.rectangle(img, (defect['xmin'], defect['ymin']), (defect['xmax'], defect['ymax']), (92, 0, 255), 8)
			cv2.putText(img,str(round(defect['confidence'],4)), (defect['xmin'], defect['ymin']-20), font, 2 ,(92, 0, 255), 4)
		cv2.imwrite(os.path.join(workingdir, '{}_inferred.jpg'.format(image_base)), img)

	tree.write(os.path.join(workingdir,'metadata-results.xml'))

	mark_car(filepath, filebase)
	static_dir=os.path.join(STATIC_DIR,STATIC_USER_DIR)
	static_path=os.path.join(static_dir,filebase)

	if os.path.isdir(static_path):
		shutil.rmtree(static_path)

	shutil.copytree(workingdir, static_path)


if __name__ == '__main__':
	process("/Users/ngocjr/Workspace/Project/computervision/paint-defect-inspection/server/utils/../assets/users/car1.zip",
		"car1")
	mark_car("/Users/ngocjr/Workspace/Project/computervision/paint-defect-inspection/server/utils/../assets/users/car1.zip",
		"car1")
	


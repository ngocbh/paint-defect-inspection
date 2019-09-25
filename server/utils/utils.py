from __future__ import absolute_import 

from os import listdir
from os.path import isfile, join, isdir

def get_listdir(path):
	ret = []
	for filename in listdir(path):
		filepath = join(path,filename)
		if isdir(filepath): 
			ret.append(filename)
	return ret

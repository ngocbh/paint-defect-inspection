import requests
import os
import glob
import pprint
import urllib
import io
import json
import cv2
import numpy
import xml.etree.ElementTree as ET

XMLAnnotationFiles = glob.glob("..\\labels\\*.xml")
PICTURE_PATH = glob.glob("..\\Defects\\**")

def draw_img(picture_path : str, root, picture_name : str):

    image = cv2.imread(picture_path)
    copy = numpy.copy(image)
    for type_tag in root.findall("object"):
        boundingbox = type_tag.find("bndbox")
        cv2.putText(copy, type_tag.find("name").text, 
            (int(boundingbox.find("xmin").text), int(boundingbox.find("ymin").text) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        cv2.rectangle(copy, 
                        (int(boundingbox.find("xmin").text), int(boundingbox.find("ymin").text)),
                        (int(boundingbox.find("xmax").text), int(boundingbox.find("ymax").text)),
                        [0, 255, 0], 2)
    
    cv2.imwrite("{}.png".format(picture_name), copy)

if __name__ == "__main__":
    assert len(PICTURE_PATH) == len(XMLAnnotationFiles)
    for (file_path, picture_file) in zip(XMLAnnotationFiles, PICTURE_PATH):
        root = ET.parse(file_path).getroot()
        print(os.path.abspath(picture_file))
        draw_img(os.path.abspath(picture_file), root, os.path.splitext(os.path.basename(picture_file))[0])

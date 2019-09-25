import xml.etree.ElementTree as ET
import glob
import os

XMLAnnotationFiles = glob.glob("..\\labels\\*.xml")
print(XMLAnnotationFiles)


for file_path in XMLAnnotationFiles:
    root = ET.parse(file_path).getroot()
    textFile = open(os.path.splitext(os.path.basename(file_path))[0] + ".txt", "w+")
    for type_tag in root.findall("object"):
        properties = []
        properties.append(type_tag.find("name").text.replace("-", "_"))
        boundingbox = type_tag.find("bndbox")
        properties.append(boundingbox.find("xmin").text)
        properties.append(boundingbox.find("ymin").text)
        properties.append(str(int(boundingbox.find("xmax").text) - int(boundingbox.find("xmin").text)))
        properties.append(str(int(boundingbox.find("ymax").text) - int(boundingbox.find("ymin").text)))
        textFile.write(" ".join(properties) + "\n")
    textFile.flush()


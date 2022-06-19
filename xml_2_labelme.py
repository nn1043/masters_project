import xml.etree.ElementTree as ET
import json
import base64
import os

filenames = []
widths = []
heights = []
shapes = []

path_anno = "/home/nicholas/Downloads/annotations/"
for annotation in os.listdir(path_anno):
    tree = ET.parse(path_anno + annotation)
    root = tree.getroot()

    filenames.append(root[1].text)
    widths.append(int(root[2][0].text))
    heights.append(int(root[2][1].text))

    xmin = float(root[4][5][0].text)
    ymin = float(root[4][5][1].text)
    xmax = float(root[4][5][2].text)
    ymax = float(root[4][5][3].text)
    bbox = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]
    shapes.append( [{ "label":"LICENSE_PLATE", "points":bbox, "group_id":None, "shape_type":"polygon", "flags":{} }] )

image_binary = []
path_images = "/home/nicholas/Downloads/images/"
for i in range(len(filenames)):
    with open(path_images + filenames[i], "rb") as image_file:
        image_binary.append( base64.b64encode(image_file.read()).decode("ascii") )


for i in range(len(filenames)):
    label = {
        "version": "5.0.1",
        "flags": {},
        "shapes": shapes[i],
        "imagePath": filenames[i],
        "imageData": image_binary[i],
        "imageHeight": heights[i],
        "imageWidth": widths[i],
    }

    path_output= "/home/nicholas/Downloads/labels"
    json_string = json.dumps(label)
    with open("{0}/{1}.json".format(path_output, filenames[i][:-4]), "w") as output:
        output.write(json_string)

"""                           
<annotation>
    <folder>images</folder>
    <filename>Cars1.png</filename>
    <size>
        <width>400</width>
        <height>248</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>licence</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <occluded>0</occluded>
        <difficult>0</difficult>
        <bndbox>
            <xmin>134</xmin>
            <ymin>128</ymin>
            <xmax>262</xmax>
            <ymax>160</ymax>
        </bndbox>
    </object>
</annotation>
"""
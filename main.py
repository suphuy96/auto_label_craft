import numpy as np  # linear algebra
import xml.etree.ElementTree as ET  # for parsing XML
import matplotlib.pyplot as plt  # to show images
from PIL import Image  # to read images
import os
import glob

root_images = r"F:\THANGNM\INvoice_ver1\INVOICE\an_viettel"
root_annots = r"F:\THANGNM\INvoice_ver1\INVOICE\an_viettel"

all_images = os.listdir(r"F:\THANGNM\INvoice_ver1\INVOICE\an_viettel/")
print(f"Total images : {len(all_images)}")

breeds = glob.glob(r"F:\THANGNM\INvoice_ver1\INVOICE\an_viettel/")
annotation = []
for b in breeds:
    annotation += glob.glob(b + "/*")
print(f"Total annotation : {len(annotation)}")

breed_map = {}
# for annot in annotation:
#     breed = annot.split("/")[-2]
#     index = breed.split("-")[0]
#     breed_map.setdefault(index, breed)
#
# print(f"Total Breeds : {len(breed_map)}")


# def bounding_box(image):
#     # bpath=root_annots+str(breed_map[image.split("_")[0]])+"/"+str(image.split(".")[0])
#     # print (bpath)
#     # print(root_annots)
#     # print (str(breed_map[image.split("_")[0]]))
#     # print (str(image.split(".")[0]))
#     bpath = root_annots + "/" + str(image.rstrip('.xml') )
#     print(bpath)
#     parser = ET.XMLParser(encoding="utf-8")
#     tree = ET.parse(bpath, parser=parser)
#     root = tree.getroot()
#     objects = root.findall('object')
#
#     for o in objects:
#         bndbox = o.find('Text')  # reading bound box
#         xmin = int(bndbox.find('xmin').text)
#         ymin = int(bndbox.find('ymin').text)
#         xmax = int(bndbox.find('xmax').text)
#         ymax = int(bndbox.find('ymax').text)
#
#     return (xmin, ymin, xmax, ymax)
#
#
# plt.figure(figsize=(10, 10))
# bbox = []
# for i, image in enumerate(all_images):
#     bbox = bounding_box(image)
#     print(bbox)
#     im = Image.open(os.path.join(root_images, image))
#     im = im.crop(bbox)
#     im.save('/content/results_imgs/{}.jpeg'.format(i, im))

def bounding_box(image):
    retval = []


    # bpath=root_annots+str(breed_map[image.split("_")[0]])+"/"+str(image.split(".")[0])
    # print (bpath)
    # print(root_annots)
    # print (str(breed_map[image.split("_")[0]]))
    # print (str(image.split(".")[0]))
    bpath = root_annots + "/" +image.rstrip('.xml')
    tree = ET.parse(bpath)
    root = tree.getroot()
    objects = root.findall('Text')

    for o in objects:
        bndbox = o.find('Text')  # reading bound box
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        retval.append(tuple((xmin, ymin, xmax, ymax)))

    return retval

plt.figure(figsize=(10, 10))
bbox = []
for i, image in enumerate(all_images):
    bboxarray = bounding_box(image)
    for x, bbox in enumerate(bboxarray):
        bbox = bounding_box(image)
        print(bbox)
        im = Image.open(os.path.join(root_images, image))
        im = im.crop(bbox)
        im.save(f'/content/results_imgs/{i}-{x}.jpeg')
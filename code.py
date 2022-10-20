from multiprocessing.sharedctypes import Value
import cv2
import os
import numpy as np
from collections import OrderedDict
orb = cv2.ORB_create(nfeatures=1000) # Find 1000 features to match from 
bf = cv2.BFMatcher()

# Image to match
findImg = 'img14.jpg'
imgCur = cv2.imread("D:\python project\Mini Project\A11-10-22\Superhero classification project\Superheroes\img16.jpg")
kp1,des1 = orb.detectAndCompute(imgCur,None)

# Loop through all superheroe images and find closest match
images = ["img1.jpg","img2.jpg","img3.jpg","img4.jpg","img5.jpg","img6.jpg","img7.jpg","img8.jpg","img9.jpg","img10.jpg","img11.jpg","img12.jpg"]

matchList = []
names = []
Superheroes="D:\python project\Mini Project\A11-10-22\Superhero classification project\Superheroes\\"
for img in images:
    imgCur = cv2.imread(f'{Superheroes}{img}',0)
    kp2,des2 = orb.detectAndCompute(imgCur,None)
 
    matches = bf.knnMatch(des1,des2,k=2)
    goodMatches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance: # Use 75 as a threshold defining a good match
            goodMatches.append([m])
    matchList.append(len(goodMatches))
    names.append(img)
print(matchList)
d={}
for i in range(len(images)):
    d[images[i]]=matchList[i]
print(d)
# sorted_value_index = np.argsort(dict.values())
# dictionary_keys = list(dict.keys())
# sorted_dict = {dictionary_keys[i]: sorted(
#     dict.values())[i] for i in range(len(dictionary_keys))}
d=dict(sorted(d.items(), key = lambda x: x[1], reverse = True))
l=list(d.keys())
 
print(d)
print(l)
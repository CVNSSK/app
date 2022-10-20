from pickle import GLOBAL
import sqlite3
from flask import Flask,redirect,render_template,request,url_for
import cv2

import os
import numpy as np
from collections import OrderedDict
from multiprocessing.sharedctypes import Value

db=sqlite3.connect("dbase\img.db",check_same_thread=False)


app=Flask(__name__)

picFolder = os.path.join('static', 'pics')

app.config['UPLOAD_FOLDER'] = picFolder

l=[]
d={}
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/register",methods=["POST"])
def register():
    image=request.form.get("image")
    print(image)
    if not image:
        return render_template("error.html",message="invalid image")
    orb = cv2.ORB_create(nfeatures=1000) # Find 1000 features to match from 
    bf = cv2.BFMatcher()


    # Image to match
    imgCur = cv2.imread(".\static\pics\\"+image) 
    kp1,des1 = orb.detectAndCompute(imgCur,None)

    # Loop through all superheroe images and find closest match
    images = ["img1.jpg","img2.jpg","img3.jpg","img4.jpg","img5.jpg","img6.jpg","img7.jpg","img8.jpg","img9.jpg","img10.jpg","img11.jpg","img12.jpg"]
    matchList = []
    names = []
    Superheroes=".\static\pics\\"
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
    global d
    d={}
    for i in range(len(images)):
        d[images[i]]=matchList[i]
    d=dict(sorted(d.items(), key = lambda x: x[1], reverse = True))
    global l
    l=list(d.keys())

    print(l)
    # 
    values_in_list = l[0:6]
    query = """
    SELECT img,address
    FROM imagesloc
    WHERE
    img IN ({})
    """.format(values_in_list).replace('[', '').replace(']', '')
    cur=db.cursor()
    x=cur.execute(query)
    x=x.fetchall()
    print(x)
    # query_df = pandas.read_gbq(query, project_id='some-project', dialect='standard')
    print("hello")
    print(d)
    for i in range(len(x)):
        d[x[i][0]]=x[i][1]
    print(d)
    return redirect("/registrants")

@app.route("/registrants")
def registrants()  :
    dic={}
    # imagelist={{('pics/' + image),d[l]} for image in l}
    # print(imagelist[0:6])
    # imagelist=imagelist[0:6]
    for i in range(0,6):
        dic['pics/' + l[i]]=d[l[i]]
    print(dic)
    return render_template("registrants.html",dic=dic)

if __name__ == '__main__':
   app.run()
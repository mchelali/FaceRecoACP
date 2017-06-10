# -*- coding: utf-8 -*-
from django.shortcuts import render
from forms import NewImage
from models import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import detection as dec
import reconnaissance as rec
import cv2
import os

def home(request):
    return render(request, 'home.html')

def step(request):
    return render(request, 'steps.html')


def experiance(request):
    #print "cook ----->", request.COOKIES
    request.session.save()
    #print "session ---->", request.session.session_key
    if not os.path.isdir("media/tmp/"+str(request.session.session_key)):
        os.mkdir("media/tmp/"+str(request.session.session_key), 0755)
        path= "media/tmp/"+str(request.session.session_key)
        print 'fichier cree --->', path
    else:
        path= "media/tmp/"+str(request.session.session_key)
        print 'le fichier existe ----->', path

    valid = False


    if request.POST:
        form = NewImage(request.POST, request.FILES)
        if form.is_valid():

            img = Image()
            img.image = request.FILES['image']
            img.save()

            visage = plt.imread("media/"+str(img.image.name))
            #return render(request, 'debug.html', locals())
            dim_false = False
            if visage.shape[0]!=124 or visage.shape[1]!=92 :
                dim_false = True
                dimention_invalid = "Velliez séléctionnez une image de dimention 124x92 pixel"
                return render(request, 'experementation.html', locals())

            database = rec.reconnaissance("media/Database", path)

            cv2.imwrite(path+"/moy.jpg", np.flipud(database.visage_moyen.reshape(124, -1)))

            #print img.image.url
            #print str(img.image.name)
            #print "media/"+str(img.image.name)

            #lecture de la photo uploader

            
            if visage.shape[2]>=3:
            	visage = cv2.cvtColor(visage, cv2.COLOR_BGR2GRAY)
            
            visage = cv2.equalizeHist(visage)
            cv2.imwrite(path+"/photo.jpg", np.flipud(visage))
            img.delete_()

            vis = False
            #detection des visage dans la photo uploader



            #print database.norm.shape
            diff = (visage.ravel() - database.visage_moyen.ravel())
            #print type(diff)
            #print diff.shape
            omega_new = np.array(np.dot(database.norm.transpose(), diff))

            #print 'omega_new\n', omega_new.shape
            #print 'omega', database.omega.shape

            database.__reconnaitre__(omega_new, path)
            if database.__recontruction__(omega_new, path):
                visage_trouve = True
            else:
                visage_trouve = False

            np.savetxt(path+"/faces.txt", database.faces, fmt='%i')
            np.savetxt(path+"/mean_face.txt", database.visage_moyen, fmt='%i')
            np.savetxt(path+"/ecart_face.txt", database.ecart_face, fmt='%i')	

	    valid = True
            #print 'Valid form'

    else:
        form = NewImage()

    return render(request, 'experementation.html', locals())

def propos(request):
    return render(request, 'a_propos.html', locals())

def elab(request):
    return render(request, 'elab.html')





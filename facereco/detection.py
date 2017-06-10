__author__ = 'mouhachelali'
import cv2

def detect(img):
    cascade = cv2.CascadeClassifier("static/haarcascades/haarcascade_frontalface_alt.xml")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(img,  scaleFactor=1.2, minNeighbors=4, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        #print 'pas de visage'
        return []
    #print rects
    rects[:, 2:] += rects[:, :2]
    #print rects
    return rects
#------------------------------------------------------------------------------------------
def box(img, rects, path_save):
    #rects= detect(img)
    if len(rects) != 0:
        mat = img.copy()
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(mat, (x1-5, y1-5), (x2+5, y2+5), (127, 255, 0), 3)
        #taille=92x124
        cv2.imwrite(path_save+"/detected.jpg", mat)
        face_extractor(img, rects, path_save)
        return True
    else:
        #print('pas de viasgeeeeeeeeeeeee')
        return False

#------------------------------------------------------------------------------------------
def face_extractor(img, rects, path_save):
    #rects=detect(img)
    #print rects

    i=1
    for x1, y1, x2, y2 in rects:
        face = img[y1:y2, x1:x2]
        face = cv2.resize(face, (124, 124))
        #print face.shape
        face = face[:, 16:108]
        #print face.shape
        #print len(face[:, :, 0].ravel())
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path_save+'/face'+str(i)+'.jpg', face)
        #print "face",i
        i = i+1

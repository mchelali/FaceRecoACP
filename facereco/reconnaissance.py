__author__ = 'mouhachelali'
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import cv2

class reconnaissance:
    def __init__(self, chemin, path_eigen):
        self.__faces_to_Matrix__(chemin)
        self.__moyenne__(float(self.nbr_visage))
        self.__ecart_visage__(self.nbr_visage)
        self.__covariance_matrix__()
        self.__valeur_vecteur_propre(path_eigen)
        self.__normalization__()
        self.__omega__()

    def __faces_to_Matrix__(self,chemin):
        mat=[]
        for dirname, dirnames, filenames in os.walk(chemin):
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    if (filename.endswith('jpg')):
                        #print os.path.join(subject_path, filename)
                        im = plt.imread(os.path.join(subject_path, filename))
                        #im = cv2.equalizeHist(im)
                        if im.ravel().shape[0]==11408:
                            mat.append(im.ravel())
        self.nbr_visage = len(mat)
        self.faces = np.array(mat).transpose()
        #print 'les visage\n\n', self.faces

    def __moyenne__(self, N):
        #calculer le visage moyen
        self.visage_moyen = np.zeros([len(self.faces), 1])
        for i in range(self.faces.shape[0]):
                self.visage_moyen[i] = np.round((sum(self.faces[i, :]) / N), 3)

        #print 'le visgae moyen\n\n', self.visage_moyen

    def __ecart_visage__(self, N):
        #print self.visage_moyen.shape
        self.ecart_face = np.zeros(self.faces.shape)
        for i in range(N):
            self.ecart_face[:, i] = ((self.faces[:, i]) - (self.visage_moyen[:, 0])).astype('float')
            #print '---------', self.ecart_face[:, i]
        #print 'l\'ecart visage \n\n', self.ecart_face

    def __covariance_matrix__(self):
        self.conMat = (np.dot(self.ecart_face.transpose(), self.ecart_face)).astype('float')
        #print 'At x A = \n\n', self.conMat
        #print self.conMat.shape
        #print trans_face

    def __valeur_vecteur_propre(self, path):
        self.eigenvalue, eigenvect = np.linalg.eig(self.conMat.astype(np.int))
        #print 'eigenvalue\n\n', self.eigenvalue
        #eigenvect = np.round(eigenvect, 3)
        #print 'eigenvector\n\n', eigenvect
        #print eigenvect.shape
        eigen_selected=[]
        for i in range(self.nbr_visage-20):
            face = (np.dot(self.ecart_face, eigenvect[:, i]))
            eigen_selected.append(face.ravel())
            cv2.imwrite(path+'/eigenface'+str(i)+'.jpg', np.flipud(face.reshape(124, -1)))
        self.eigen_vector = np.array(eigen_selected).transpose()
        #print 'eigen vector all (A x Ui)\n', self.eigen_vector

    def __normalization__(self):
        normalize = []
        self.eigen_vector = self.eigen_vector.astype('float')
        for i in range(self.eigen_vector.shape[1]):
            normalize.append(self.eigen_vector[:, i].ravel()/np.linalg.norm(self.eigen_vector[:, i].ravel()))
        self.norm = np.array(normalize).transpose()
        #print 'vecteur normalizer\n\n', self.norm
        print self.norm.shape

    def __omega__(self):
        self.omega = np.dot(self.norm.transpose(), self.ecart_face)
        #print 'omega\n\n', self.omega
        #print self.omega.shape

    def __reconnaitre__(self, omega_new, path):
        #  omega_new  : is a list who contain eigenface components
        #print '______________________________reconnaitre______________________________'
        #print 'omega\n', self.omega
        #print 'omega_new\n', omega_new
        # in this step we want to calculate the euclidiane distence betwene the omega and the omage_new
        self.min_euclid = []
        self.euc_dist = []
        for j in range(self.nbr_visage):
            x = (self.omega[:, j]).ravel()-(omega_new.ravel())
            self.euc_dist.append(round(np.linalg.norm(x)))
        self.min = [self.min_index(self.euc_dist), min(self.euc_dist)]
        matplotlib.use('Agg')
        plt.bar(range(self.nbr_visage), self.euc_dist, width=1)
        plt.ylim(0,max(self.euc_dist)+5)
        plt.xlim(-1,self.nbr_visage+1)
        plt.savefig(path+'/dist.png')


    def min_index(self, tab):
        m=0
        for i in range(1,len(tab)):
            if (tab[i] < tab[m]) :
                m = i
        return m

    def __recontruction__(self, omega_new, path):
        #print self.norm.transpose().shape
        #print self.omega[:, self.min[0]-1].reshape(-1, 1).shape
        print max(self.euc_dist)
        if self.euc_dist[self.min[0]] < max(self.euc_dist)/2.6:

            x = ((np.dot(self.norm, self.omega[:, self.min[0]])).ravel() + self.visage_moyen.ravel()).astype(np.uint8)
            #print x
            cv2.imwrite(path+'/reco.jpg', np.flipud(x.reshape(124, -1)))
            return True
        else:
            return False



#test = reconnaissance('test/Database','test/')

from PIL import Image
import cv2
import sys
import numpy as np
import random as rd

S = 255

def negativeImage(im, neg, cls, a):
    if cls == "HSV":
        img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2HSV)
    elif cls == "YCbCr":
        img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2YCrCb)
    else:
        img = np.asarray(im)
    
    R,G,B = cv2.split(img)
    if neg == "Negative":
        B[:] = [S-x for x in B]     #inverting blue
        G[:] = [S-x for x in G]     #inverting green    
        R[:] = [S-x for x in R]     #inverting red
    if a != "":
        a=int(a)%255
        B[:] = [x+a for x in B]     
        G[:] = [x+a for x in G]        
        R[:] = [x+a for x in R]
    #saving image
    my_img = cv2.merge((R, G, B))
    my_img = Image.fromarray(my_img)
    return my_img

'''
    for i in range(600000):
        rd1 = rd.randint(0, img.shape[1]-2)
        rdy1 = rd.randint(0, img.shape[0]-2)
        rd2 = rd.randint(0, img.shape[1]-2)
        rdy2 = rd.randint(0, img.shape[0]-2)
        tmp1, tmp2, tmp3 = B[rdy1][rd1], G[rdy1][rd1], R[rdy1][rd1]
        B[rdy1][rd1], G[rdy1][rd1], R[rdy1][rd1] = B[rdy2][rd2], G[rdy2][rd2], R[rdy2][rd2]
        B[rdy2][rd1], G[rdy2][rd1], R[rdy2][rd1] = tmp1, tmp2, tmp3
'''

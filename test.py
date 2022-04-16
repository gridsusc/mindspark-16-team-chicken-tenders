from traceback import format_exc
import numpy as np 
from preprocess import preprocess
from texton_color_utils import Textons
import cv2
import sys
import os

im = cv2.imread(sys.argv[1])
#im = cv2.blur(im,(5,5))
#im = cv2.medianBlur(im, 5)
#ob = preprocess(im)
#im, _ = ob.kmeans(3)

#im = cv2.medianBlur(im,3)

tex = Textons(im, int(sys.argv[2]), int(sys.argv[3]), 1)
im = tex.textons()
centers = np.unique(im)

for _ in range(int(sys.argv[2])):
    show = np.zeros_like(im)
    show[im==centers[_]] = 255
    #show = cv2.morphologyEx(show, cv2.MORPH_OPEN, np.ones((5, 5)))
    cv2.imwrite('/home/adkishor/projects/mindspark-16-team-chicken-tenders/foreground/foreground: '+str(_) + '.png', cv2.bitwise_not(show))

for _ in range(int(sys.argv[2])):
    show = np.zeros_like(im)
    show[im==centers[_]] = 255
    show = cv2.morphologyEx(show, cv2.MORPH_OPEN, np.ones((5, 5)))
    cv2.imwrite('/home/adkishor/projects/mindspark-16-team-chicken-tenders/edges/edges: '+str(_) + '.png', cv2.bitwise_not(show))


cv2.imshow("image", im)
cv2.waitKey(0)
cv2.destroyAllWindows()

f = os.listdir("/home/adkishor/projects/mindspark-16-team-chicken-tenders/foreground/")
e = os.listdir("/home/adkishor/projects/mindspark-16-team-chicken-tenders/edges/")

i = 0
for fimages in f:
    for eimages in e:

        image1 = cv2.imread("/home/adkishor/projects/mindspark-16-team-chicken-tenders/foreground/"+str(fimages),0)
        cv2.imshow("image1", image1)
        image1 = cv2.bitwise_not(image1)
        image1 = cv2.dilate(image1, kernel=np.ones((7,7)), iterations=1)
        image1 = cv2.bitwise_not(image1)
        image2 = cv2.imread("/home/adkishor/projects/mindspark-16-team-chicken-tenders/edges/"+str(eimages),0)
        cv2.imshow("image2", image2)
        show = np.zeros_like(image1)
        show[image1 == 0] = 255
        show[image2 == 0] = 127
        show = cv2.medianBlur(show,5)

        # cv2.imshow("check", show)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        cv2.imwrite("/home/adkishor/projects/mindspark-16-team-chicken-tenders/superimposed_imges/final_7"+str(i)+".png", show)
        i+=1


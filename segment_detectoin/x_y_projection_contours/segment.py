# zeinab Taghavi
#
# its better image be threshed once before usage
# 1 - correct rotation to more accurately find lines
# 2 - find the high compression vertical area
# 3 - in vertical high compression areas, make all horizontal high compression areas
#

import cv2
from scipy import ndimage
import pytesseract
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

def segment(img_file):

    img = cv2.imread(img_file)
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    env = cv2.bitwise_not(otsu)
    contour ,_ = cv2.findContours(env , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    len_cnt = []
    for cnt in contour:
        if cv2.contourArea(cnt)<(img.shape[0]*img.shape[1]/3):
            len_cnt.append(cv2.contourArea(cnt))


    clustering = []
    k_pre = min(len_cnt)
    for x in range(1,11):
        k = (max(len_cnt)-min(len_cnt)) * x / 10
        clustering.append(sum([k_pre <= i < k for i in len_cnt]))
        k_pre = k

    print(clustering)
    def_clustering = [clustering[i-1] - clustering[i] for i in range(1 , len(clustering))]
    thresh = (def_clustering.index(max(def_clustering))+1) * (max(len_cnt)-min(len_cnt))/10
    thresh_pre = (def_clustering.index(max(def_clustering))) * (max(len_cnt)-min(len_cnt))/10
    print (thresh , thresh_pre)
    print (len(contour),sum(clustering))

    if not os.path.exists('lines_images_for_' + img_file):
        os.mkdir('lines_images_for_' + img_file)

    count = 0
    os.chdir('Segment_images_for_' + img_file)

    for cnt in contour:
        if not thresh_pre< cv2.contourArea(cnt)< thresh:
            count += 1
            x , y, w, h = cv2.boundingRect(cnt)
            segment_img = otsu[: , x:x+w]
            cv2.imwrite(
                str(count) + '_segment_y1_{}_y2_{}_x1_{}_x2_{}_.jpg'.format(y - (int(h * 3 / 4)), y + (int(h * 7 / 4)), x,
                                                                         x + w), segment_img)
            # cv2.drawContours(otsu, [cnt], 0, 150, 3)

    # cv2.imwrite(img_file + '_1_contoured.jpg', otsu)

if __name__ == '__main__':
    
    n1 = 3
    n2 = 4
    
    avg_time = []
    
    for i in range(n1,n2):

        img_file = str(i) + '.jpg'
        segment(img_file)


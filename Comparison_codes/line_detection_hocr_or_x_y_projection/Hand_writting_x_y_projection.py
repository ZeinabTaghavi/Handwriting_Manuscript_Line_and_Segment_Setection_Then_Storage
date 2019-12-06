# zeinab Taghavi
#
# its better image be threshed once before usage
# 1 - correct rotation to more accurately find lines
# 2 - find the high compression vertical area
# 3 - in vertical high compression areas, make all horizontal high compression areas
#

import cv2
import numpy as np


def find_line_by_semi_histogram(img_file,vertical_percent , horizontal_percent):

    def correct_rotation(img):
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        num = 0
        sum = 0

        ## if there is no line, or OCR could not find
        try:
            for i in lines:
                for rho, theta in i:
                    if np.degrees(theta) > 60 and np.degrees(theta) < 120:
                        sum += np.degrees(theta)
                        num += 1

            rows, cols = img.shape[0], img.shape[1]
            if num != 0:
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), (sum / num) - 90, 1)
                img = cv2.warpAffine(img, M, (cols, rows))
                theta_radian = np.radians((sum / num) - 90)
                y = int(np.sin(theta_radian) / np.cos(theta_radian) * img.shape[0])
                img[0:abs(y), :] = 255
                img[img.shape[0] - abs(y):, :] = 255
                x = int(np.sin(theta_radian) / np.cos(theta_radian) * img.shape[1])
                img[:, 0:abs(y)] = 255
                img[:, img.shape[1] - abs(y):] = 255
        except:
            pass
        # y_border_size = int(img.shape[0] * (.05))
        # x_border_size = int(img.shape[1] * (.05))
        # img[0:y_border_size, :] = 255
        # img[img.shape[0] - y_border_size: img.shape[0], :] = 255
        # img[:, 0:x_border_size] = 255
        # img[:, img.shape[1] - x_border_size:img.shape[1]] = 255
        # h, w = img.shape[:2]
        # mask = np.zeros((h + 2, w + 2), np.uint8)
        # cv2.floodFill(img, mask, (0, 0), (255, 255, 255))

        return img

    img = cv2.imread(img_file)

    # 1 - correct rotation to more accurately find lines

    corrected_rotation =  correct_rotation(img)
    gray_corrected_rotation = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_corrected_rotation, (5, 5), 0)
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    gray_env = cv2.bitwise_not(otsu)
    gray_corrected_rotation = otsu
    # 2 - find the high compression vertical area

    vertical_hist = [sum(gray_env[i,:]) for i in range(corrected_rotation.shape[0])]
    vertical_temp = gray_corrected_rotation.copy()
    vertical_limit = gray_env.shape[1] * 255 * vertical_percent *.01
    for i in range(len(vertical_hist)):
        if vertical_hist[i] > vertical_limit:
            vertical_temp[i,:] = 255
        else:
            vertical_temp[i,:] = 0

    # cv2.imwrite('find_line_by_semi_histogram_1_vertical_line_detected.jpg' , vertical_temp)
    contour , _ = cv2.findContours(vertical_temp , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(corrected_rotation , contour , -1 , 100 , 3)

    # 3 - in vertical high compression areas, make all horizontal high compression areas

    vertical_lines_positions = []  # they are vertical high compression areas
    for cnt in contour:
        x , y , w , h = cv2.boundingRect(cnt)
        vertical_lines_positions.append([y,y+h])
        # corrected_rotation = cv2.rectangle(corrected_rotation , (x,y) , (x+w , y+h) , (0,0,200) ,-1)

    gray_corrected_rotation_env = cv2.bitwise_not(otsu)
    for y1,y2 in vertical_lines_positions:
        temp_img_env = gray_corrected_rotation_env[y1:y2,:]
        horizontal_limit = (y2-y1) * 255 * horizontal_percent * .01
        for j in range(temp_img_env.shape[1]):
            if sum(temp_img_env[:,j]) > horizontal_limit:
                temp_img_env[:, j] = 255
            else:
                temp_img_env[:, j] = 0
        temp_img = cv2.bitwise_not(temp_img_env)
        gray_corrected_rotation[y1:y2,:] = temp_img

    # cv2.imwrite('a.jpg', cv2.bitwise_not(otsu))
    cv2.imwrite(img_file+'_find_line_by_semi_histogram_2_horizontal_line_rected.jpg', gray_corrected_rotation)


if __name__ == '__main__':
    n1 = 2
    n2 = 6
    for i in range(n1,n2):
        img_file = str(i)+'.jpg'
        find_line_by_semi_histogram(img_file,11,10)
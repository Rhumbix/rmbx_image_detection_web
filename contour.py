import cv2
import sys
import numpy as np
import mask

def contains(big, small):
    return big[0] <= small[0] and big[1] <= small[1] and (big[0] + big[2]) >= (small[0] + small[2]) and (big[1] + big[3]) >= (small[1] + small[3])

def contour(image, std):
    im = cv2.imread(image)
    blur = cv2.GaussianBlur(im,(3,3),0)
    imgray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('static/img/static_005.jpg', imgray)
    #thresh = cv2.adaptiveThreshold(imgray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,8)
    ret,thresh = cv2.threshold(imgray,80,255,0)
    #thresh = cv2.Canny(imgray, 20,100)
    cv2.imwrite('static/img/static_006.jpg', thresh)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite('static/img/static_007.jpg', im2)

    candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        if area > 2*cv2.contourArea(std) and (area/(w*h)) > 0.65 and contains(cv2.boundingRect(cnt), cv2.boundingRect(std)):
            candidates += [cnt]

    winner = sorted(candidates, key=lambda cnt: cv2.contourArea(cnt))[0]
    im3 = cv2.drawContours(cv2.imread("static/img/original.jpg"),[winner], -1, (0,255,0), 3)
    cv2.imwrite('static/img/static_004.jpg', im3)
    return winner

if __name__ == "__main__":

    std = mask.mask_for_yellow("static/img/original.jpg")
    contour(sys.argv[1], std)

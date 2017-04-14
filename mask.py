import cv2
import sys
import numpy as np

def mask_for_yellow(image):
    img = cv2.imread(image)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([40,50,50])
    upper_blue = np.array([75,180,180])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imwrite("static/img/static_001.jpg", mask)

    im = cv2.imread("static/img/static_001.jpg")
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)
    cv2.imwrite("static/img/static_002.jpg", thresh)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        if area > 2000 and (area/(w*h)) > 0.65:
            candidates += [cnt]

    im3 = cv2.drawContours(img, candidates, -1, (0,255,0), 3)
    cv2.imwrite('static/img/static_003.jpg', im3)
    print(len(candidates))

    winner = sorted(candidates, key=lambda cnt: cv2.contourArea(cnt), reverse=True)[1]
    return winner
	    
if __name__ == "__main__":

    mask_for_yellow(sys.argv[1])

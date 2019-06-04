import cv2
from sys import argv as argv

im = cv2.imread(argv[1])
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
hierarchy = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours = hierarchy[0]
hierarchy = hierarchy[1]
idx =0 
max = 0
image_max = []
for cnt in contours:
    idx += 1
    x,y,w,h = cv2.boundingRect(cnt)
    print(w*h)
    roi=im[y:y+h,x:x+w]
    if w*h > max:
        max = w*h
        image_max = roi
    # cv2.imwrite(str(idx) + '.jpg', roi)
    cv2.rectangle(im,(x,y),(x+w,y+h),(200,0,0),2)

cv2.imshow('img',image_max)
cv2.waitKey(0)  
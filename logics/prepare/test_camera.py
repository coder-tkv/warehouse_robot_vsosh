import cv2
video = cv2.VideoCapture(0)


while True:
    ret, img = video.read()
    if not ret:
        print('Frame is empty')
        break
    else:
        cv2.imshow('VIDEO', img)
        cv2.waitKey(1)

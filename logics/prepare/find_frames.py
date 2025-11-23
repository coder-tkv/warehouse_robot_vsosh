import numpy as np
import cv2
video = cv2.VideoCapture(0)


ret, img = video.read()
frame = img[50:270, 0:400] # [y1:y2, x1:x2]

orig = frame.copy()

# переводим в HSV
hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)

# твой диапазон для красного
lower_red = np.array([147, 62, 99], dtype=np.uint8)
upper_red = np.array([255, 255, 255], dtype=np.uint8)

# маска по цвету
mask = cv2.inRange(hsv, lower_red, upper_red)

# ищем контуры на маске
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    raise RuntimeError("Красная рамка не найдена")

# берём самый большой контур (по площади)
c = max(contours, key=cv2.contourArea)

# получаем минимальный повернутый прямоугольник
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
pts = np.array(box, dtype="float32")

# сортировка углов (левый-верх, правый-верх, правый-низ, левый-низ)
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # левый верх
    rect[2] = pts[np.argmax(s)]  # правый низ

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # правый верх
    rect[3] = pts[np.argmax(diff)]  # левый низ
    return rect

rect = order_points(pts)
(tl, tr, br, bl) = rect

# считаем размеры результата
widthA = np.linalg.norm(br - bl)
widthB = np.linalg.norm(tr - tl)
maxWidth = int(max(widthA, widthB))

heightA = np.linalg.norm(tr - br)
heightB = np.linalg.norm(tl - bl)
maxHeight = int(max(heightA, heightB))

dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]
], dtype="float32")

# матрица перспективного преобразования и выравнивание
M = cv2.getPerspectiveTransform(rect, dst)
warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

resized_image = cv2.resize(warped, (1287, 720))

start_offset_y = 110
start_offset_x = 110
size = 250
offset_y = 8
offset_x = 8

for y in range(2):
    for x in range(4):
        cv2.rectangle(
            resized_image,
            (
                size*x + offset_x*x + start_offset_x,
                size*y + offset_y*y + start_offset_y
            ),
            (
                size*x + offset_x*x + size + start_offset_x,
                size*y + offset_y*y + size + start_offset_y
            ),
            (0, 255, 255),
            1
        )

cv2.imshow('VIDEO', resized_image)
cv2.waitKey()

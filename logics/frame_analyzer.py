import numpy as np
from logics.config import *
import cv2


def blob_find (hsv, min, max): #Бинаризация
    blob = cv2.inRange(hsv, min,max)
    return cv2.countNonZero(blob)


def analyze_frame(local_frame):
    hsv = cv2.cvtColor(local_frame,cv2.COLOR_BGR2HSV)
    robot_pixels_number = blob_find(hsv, robot_range[0], robot_range[1])
    goto_pixels_number = blob_find(hsv, goto_range[0], goto_range[1])
    danger_pixels_number = blob_find(hsv, danger_range[0], danger_range[1])
    if debug:
        print('robot_pixels_number', robot_pixels_number)
        print('goto_pixels_number', goto_pixels_number)
        print('danger_pixels_number', danger_pixels_number)
    start_pos = False
    goto_pos = False
    tile_type = FLOOR
    if robot_pixels_number > 5000:
        start_pos = True
    elif goto_pixels_number > 100:
        goto_pos = True
    elif danger_pixels_number > 1000:
        tile_type = DANGER
    return tile_type, start_pos, goto_pos


def get_rectangle(frame):
    orig = frame.copy()

    blur = cv2.GaussianBlur(orig, (5, 5), 0)

    # переводим в HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

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

    return resized_image
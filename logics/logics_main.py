import cv2
from logics.config import *
from logics.path_finder import dijkstra, get_matrix
from logics.frame_analyzer import analyze_frame, get_rectangle
from logics.bluetooth_send import send_to_robot

video = cv2.VideoCapture(1)

def run(is_auto, goto_x=None, goto_y=None):
    global video
    ret, img = video.read()
    # cv2.imwrite('123.png', img)
    # img = cv2.imread('123.png')
    frame = img[50:270, 0:400] # [y1:y2, x1:x2]
    frame = get_rectangle(frame)

    if debug:
        x = 2
        y = 1
        tile = analyze_frame(
            frame
            [
                size*y + offset_y*y + start_offset_y:size*y + offset_y*y + size + start_offset_y,
                size*x + offset_x*x + start_offset_x:size*x + offset_x*x + size + start_offset_x
            ]
        )
        cv2.rectangle(
            frame,
            (
                size * x + offset_x * x + start_offset_x,
                size * y + offset_y * y + start_offset_y
            ),
            (
                size * x + offset_x * x + size + start_offset_x,
                size * y + offset_y * y + size + start_offset_y
            ),
            (0, 255, 255),
            1
        )
        print(tile)
    else:
        tiles_array = [[0] * list_width for i in range(list_height)]
        robot_pos = -1
        goto_pos = -1
        for y in range(list_height):
            for x in range(list_width):
                tile = analyze_frame(
                    frame
                    [
                    size * y + offset_y * y + start_offset_y:size * y + offset_y * y + size + start_offset_y,
                    size * x + offset_x * x + start_offset_x:size * x + offset_x * x + size + start_offset_x
                    ]
                )
                cv2.putText(
                    frame,
                    str(list_width * y + x),
                    (size * x + offset_x * x + start_offset_x, size * y + offset_y * y + 65 + start_offset_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 5)
                cv2.rectangle(
                    frame,
                    (
                        size * x + offset_x * x + start_offset_x,
                        size * y + offset_y * y + start_offset_y
                    ),
                    (
                        size * x + offset_x * x + size + start_offset_x,
                        size * y + offset_y * y + size + start_offset_y
                    ),
                    (0, 255, 255),
                    2
                )
                if tile[1]:
                    robot_pos = list_width * y + x
                elif tile[2] and is_auto:
                    goto_pos = list_width * y + x
                tiles_array[y][x] = tile[0]

        if not is_auto:
            goto_pos = list_width * goto_y + goto_x

        print('Карта: ')
        for el in tiles_array:
            print(*el)

        matrix = get_matrix(tiles_array)

        print('Позиция робота:', robot_pos)
        print('Конечная позиция:', goto_pos)

        path, total_cost = dijkstra(matrix, robot_pos, goto_pos)
        if path is None:
            raise RuntimeError('Путь не найден')

        to_send = 'p'
        for j in path:
            to_send += str(j) + '-'
        to_send += f's0e'
        print('Путь:', to_send)
        print('-------------')

        send_to_robot(to_send)

    # cv2.imshow('VIDEO', frame)
    # cv2.waitKey()

    return frame


def get_robot_pos():
    global video
    ret, img = video.read()
    frame = img[50:270, 0:400] # [y1:y2, x1:x2]
    frame = get_rectangle(frame)

    for y in range(list_height):
        for x in range(list_width):
            tile = analyze_frame(
                frame
                [
                size * y + offset_y * y + start_offset_y:size * y + offset_y * y + size + start_offset_y,
                size * x + offset_x * x + start_offset_x:size * x + offset_x * x + size + start_offset_x
                ]
            )
            if tile[1]:
                return x, y
    return None

if __name__ == '__main__':
    frame = run(True, None, None)
    cv2.imshow('VIDEO', frame)
    cv2.waitKey()

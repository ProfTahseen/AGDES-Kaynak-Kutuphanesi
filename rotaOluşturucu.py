import cv2
import numpy as np

import time

def solve(point1, point2, y):

    x1, y1 = point1
    x2, y2 = point2
    m = (y2 - y1) / (x2 - x1 + 0.000001)
    x = x1 + (y - y1) / m
    return x

def generate_back_and_forth_path(area_corners, step_size):

    path = []
    x1, y1 = area_corners[0]
    x2, y2 = area_corners[1]
    x3, y3 = area_corners[2]
    x4, y4 = area_corners[3]

    current_point = (x1 + step_size, y1 - step_size)
    path.append(current_point)

    scanDirection = True

    tracker = iter([True, False])
    ref = True
    while current_point[1] - step_size > y3 or (ref := next(tracker)):
        while (current_point[0] + step_size < solve(area_corners[1], area_corners[2], current_point[1])) and scanDirection:
            new_point = (current_point[0] + step_size, current_point[1])
            path.append(new_point)
            current_point = new_point

        while (current_point[0] - step_size > solve(area_corners[0], area_corners[3], current_point[1])) and not scanDirection:
            new_point = (current_point[0] - step_size, current_point[1])
            path.append(new_point)
            current_point = new_point

        scanDirection = not scanDirection

        if tracker:
            new_point = (current_point[0], current_point[1] - step_size)
            path.append(new_point)
            current_point = new_point

    return path

area_corners = [(100, 500), (500, 500), (700, 100), (100, 100)]

step_size = 40

path_points = generate_back_and_forth_path(area_corners, step_size)
image = np.zeros((700, 800, 3), dtype=np.uint8)
cv2.polylines(image, np.array([area_corners], dtype=np.int32), isClosed=True, color=(255, 255, 255), thickness=2)

for i in range(len(path_points) - 1):
    cv2.line(image, path_points[i], path_points[i + 1], color=(0, 0, 255), thickness=3)
    cv2.imshow("Rota", image)
    if cv2.waitKey(15) == ord('q'):
        cv2.destroyAllWindows()
        break

for point in path_points:
    cv2.circle(image, point, 4, (0, 255, 0), -1)
    cv2.imshow("Rota", image)
    if cv2.waitKey(15) == ord('q'):
        cv2.destroyAllWindows()
        break

cv2.waitKey()
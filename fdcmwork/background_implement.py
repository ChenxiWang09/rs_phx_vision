import numpy
import cv2
import utils.furniture as furniture
import utils.mouse_input as mouse_input

'''
This function helps to remove background noise.
'''


def left_top(gray_img, name, point1, point2, output_path, trigger=False):
    k = (point2[1] - point1[1]) / (point2[0] - point1[0])
    b = (point2[1] - point2[0] * k)

    m = len(gray_img)
    n = len(gray_img[0])
    for i in range(m):
        for j in range(n):
            if k * j + b > i:
                gray_img[i][j] = 0

    while trigger:
        cv2.imshow('img_modified', gray_img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite(output_path + name, gray_img)
            print('Successfully save gray!')

    return gray_img


if __name__ == '__main__':
    input_path = '/home/hlabbunri/Desktop/wcx/wrs-wcx/wcx/fdcmwork/data/query/'
    output_path = '/home/hlabbunri/Desktop/wcx/wrs-wcx/wcx/fdcmwork/data/query/implement/'
    img_name = 'rs3_rgb_8.jpg'
    save_name = 'rs3_rgb_8.jpg'
    obj = cv2.imread(input_path + img_name)

    fur_1 = furniture.furniture_image(rgb_image=obj, type='query', number=8)
    gray = fur_1.get_gray(trigger=False)

    points = mouse_input.input(gray)
    left_top(gray, save_name, points[0], points[1], trigger=True, output_path=output_path)

import cv2
import numpy as np
a=[]
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append([y,x])
        print(y,x)


def choose_point(img):
    while True:
        cv2.namedWindow("edge_map")
        cv2.setMouseCallback("edge_map", on_EVENT_LBUTTONDOWN)
        cv2.imshow("edge_map", img)
        key = cv2.waitKey(1)
        if key==ord('q'):
            break


def cut_off_based_on_mouse(num,edge_map,a,trigger=False):
    new_edge_map=edge_map[a[0][0]:a[1][0],a[0][1]:a[1][1]]
    while trigger:
        cv2.imshow('outline',new_edge_map)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite('C:/wrs-cx/wcx/outline/data/'+str(num)+'.pgm', new_edge_map)
            print('Successfully save edge '+str(num)+'!')


if __name__ =="__main__":
    edge=cv2.imread(r'C:\wrs-cx\wcx\outline\data\query12.27\rs\rotate_6.pgm',0)
    choose_point(edge)
    cut_off_based_on_mouse(4, edge, a, trigger=True)
    # obj5 p1 313 286  p2 535 523

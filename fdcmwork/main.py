import numpy as np
import cv2
import math
import time
import wcx.utils1.furniture as furniture

import wcx.utils1.realsense as rs
import wcx.utils1.furniture as furniture
import wcx.utils1.furniture_function as furniture_function

def cadidates(imgs, save_path):
    n = len(imgs)
    camera_img=[]
    template_outline_path='data/temp/temp_outline/'
    for i in range(n):
        camera_img.append(furniture.furniture_image(rgb_image=imgs[i], name=str(i+1), save_path=save_path))
        camera_img[i].get_gray(trigger=True)
        camera_img[i].get_edge_map(threshold=[25,100], trigger=True)
        camera_img[i].get_outline(trigger=True)
        camera_img[i].line_fit(trigger=True)
        camera_img[i].image_rotation(template_outline_path=template_outline_path, trigger=True)


def template_outline_slope():
    template = []
    slope = np.zeros(8)
    input_path = 'E:/wrs-cx\wcx/fdcmwork/data/temp/temp/'
    save_path = 'E:/wrs-cx\wcx/fdcmwork/data/temp/temp_outline/'

    for i in range(8):
        template_image = cv2.imread(input_path + str(i + 1) + '.png')
        template.append(furniture.furniture_image(rgb_image=template_image, name=str(i+1), save_path=save_path))
        template[i].get_gray()
        template[i].get_edge_map(threshold=[25,100], trigger=True)
        template[i].get_outline(trigger=True)
        template[i].line_fit(trigger=True)
        cv2.imwrite(save_path+str(i+1)+'.pgm', template[i].outline)
        slope[i]=template[i].slope

    np.save(save_path+'outline_slope.npy', slope)
    print('Successfully saving!')





if __name__=='__main__':

    '''
    1,extract target image, generate edge map and outline of edge map.
    2,comparing different outline.
    '''

    '''
    extract target image, generate edge map and outline
    '''

    # template_outline_slope()
    # phxi_host = "127.0.0.1:18300"
    # phxi_client = phoxi.Phoxi(host=phxi_host)
    # realsense_client: object = rs.RealSense()
    #
    # rs_rgb = realsense_client.get_rgb()
    # phx_grayimg, phx_depthnparray_float32, phx_pcd = phxi_client.getalldata()
    img=cv2.imread('data/query/phx_rgb_2.jpg')
    imgs=[]
    imgs.append(img)
    save_path='data/temp/temp_outline/'
    cadidates(imgs, save_path)




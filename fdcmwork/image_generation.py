import wcx.utils1.furniture as furniture
import wcx.utils1.phoxi as phoxi
import wcx.utils1.realsense as rs
import cv2

if __name__=='__main__':

    phxi_host = "127.0.0.1:18300"
    phxi_client = phoxi.Phoxi(host=phxi_host)
    realsense_client: object = rs.RealSense()

    phx_grayimg, phx_depthnparray_float32, phx_pcd = phxi_client.getalldata()
    num=1
    while True:
        rs_depth = realsense_client.get_depth()
        rs_rgb = realsense_client.get_rgb()
        cv2.imshow('rs image' , rs_rgb)
        cv2.imshow('phx_gray',phx_grayimg)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite('data/rs1_rgb_'+str(num)+'.jpg', rs_rgb)
            print('Successfully save rgb image ' + str(num) + '!')
        if key ==ord('g'):
            cv2.imwrite('data/phx_rgb_' + str(num) + '.jpg', phx_grayimg)
            print('Successfully save rgb image ' + str(num) + '!')




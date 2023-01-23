import cv2
import math
import utils1.phoxi as phoxi
import numpy as np
import copy
import open3d as o3d


def judge_zero(input):
    if math.fabs(input[0])+math.fabs(input[1])+math.fabs(input[2]) == 0:
        return True
    else:
        return False

def save_start_pos_rat(MA):
    pos, rot_mat, jnts = MA.get_pos_rot_jnts_right_now()
    np.save('data/start_pos.npy',pos)
    np.save('data/start_rot_mat.npy',rot_mat)
    np.save('data/start_jnts.npy', jnts)

def get_point_cloud_env(phxi_client,name):

    grayimg, depthnparray_float32, pcd = phxi_client.getalldata()  # graying image,depth array [772,1032], while pcd= 772x1032 = 796704
    pcd_new=copy.deepcopy(pcd)
    pt = o3d.geometry.PointCloud()
    pt.points = o3d.utility.Vector3dVector(pcd_new)
    o3d.visualization.draw_geometries([pt])
    while True:

        cv2.imshow("img", grayimg)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    o3d.io.write_point_cloud('data/pcd_env_'+name+'.pcd', pt)
    cv2.imwrite('data/env_gray_img'+name+'.jpg',grayimg)
    np.save('data/env_depth_img'+name+'.npy',depthnparray_float32)
    print('success!')

def extract_plane(phxi_client,name):

    grayimg, depthnparray_float32, pcd = phxi_client.getalldata()  # graying image,depth array [772,1032], while pcd= 772x1032 = 796704
    pcd_new=copy.deepcopy(pcd)
    pt = o3d.geometry.PointCloud()
    n = len(grayimg)
    m = len(grayimg[0])
    pcd_list = []

    for i in range(n):
        for j in range(m):
            if 189<i<517 and 284<j<702:
                pcd_list.append(pcd_new[i*m+j])
    pcd_nnew=np.array(pcd_list)
    pt.points = o3d.utility.Vector3dVector(pcd_nnew)
    o3d.visualization.draw_geometries([pt])


    o3d.io.write_point_cloud('data/pcd_box_env_'+name+'.pcd', pt)
    print('success!')

def extract_obj_point_cloud(phxi_client,name):

    pcd_env=o3d.io.read_point_cloud('data/pcd_env_'+name+'.pcd', format='pcd')
    np_pcd_env=np.asarray(pcd_env.points)

    grayimg, depthnparray_float32, pcd = phxi_client.getalldata()  # graying image,depth array [772,1032], while pcd= 772x1032 = 796704
    origin_pt=o3d.geometry.PointCloud()
    origin_pt.points = o3d.utility.Vector3dVector(copy.deepcopy(pcd))
    o3d.visualization.draw_geometries([origin_pt])


    n = len(grayimg)
    m = len(grayimg[0])
    pt = o3d.geometry.PointCloud()
    pcd_list = []

    shreshold_dis = pcd[495 * m + 409]
    wigth_range=[320, 686]
    height_range=[234, 514]
    for i in range(n):
        for j in range(m):
            if height_range[0] < i < height_range[1] and wigth_range[0] < j < wigth_range[1]:
                if (math.fabs(np_pcd_env[i*m+j][0]-pcd[i*m+j][0])+math.fabs(np_pcd_env[i*m+j][1]-pcd[i*m+j][1])+math.fabs(np_pcd_env[i*m+j][2]-pcd[i*m+j][2])) > 5:
                        pcd_list.append(pcd[i*m+j])

    pcd_new=np.array(pcd_list)
    pt.points = o3d.utility.Vector3dVector(pcd_new)
    o3d.visualization.draw_geometries([pt])
    o3d.io.write_point_cloud('data/pcd_object'+name+'.pcd', pt)
    cv2.imwrite('data/gray_img'+name+'.jpg',grayimg)
    np.save('data/depth_img'+name+'.npy',depthnparray_float32)
    print('success!')

if __name__ == '__main__':
    phxi_host = "127.0.0.1:18300"
    phxi_client = phoxi.Phoxi(host=phxi_host)
    # MA = ma.ur3eusing_example()
    # MA.get_pos_rot_jnts_right_now()
    # start_jnts=np.load('data/start_jnts.npy')
    # save_start_pos_rat(MA)
    '''
    get env pcd
    '''
    # MA.just_move(start_jnts)
    # time.sleep(1)
    get_point_cloud_env(phxi_client, name='5')
    get_point_cloud_env(phxi_client,name='6')
    # extract_plane(phxi_client,'1')
    # MA.rotate_move(angle=-90, axis='y', planning=True, save=True, move=True)
    # time.sleep(1)
    # get_point_cloud(phxi_client, name='2')
    '''
    extract obj pcd(compared gripper carry obj with gripper pcd)
    '''
    # MA.just_move(start_jnts)
    # time.sleep(1)
    # extract_obj_point_cloud(phxi_client, name='3')
    # extract_obj_point_cloud(phxi_client,name='4')
    # MA.rotate_move(angle=-90,axis='y',planning=True,save=True,move=True)
    # time.sleep(1)
    # extract_obj_point_cloud(phxi_client, name='2')
    # clear_block_space('1')
    # # clear_block_space('2')
    # get_extrinsic_matrix(phxi_client)
    # get_position(phxi_client)


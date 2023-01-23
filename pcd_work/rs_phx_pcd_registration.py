import wcx.utils1.realsense as rs
import wcx.utils1.phoxi as phx
import cv2
import numpy as np
import wcx.pcd_work.Aruco_marker_estimation as Aruco_marker_estimation
import open3d as o3d
import copy
import wcx.utils1.rotate_matrix as rmt

def pcd_registration(source, target, transformation, trigger=False):
    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=np.array([0, 0, 0]))
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    check = np.asarray(source.points)
    source_temp.transform(transformation)
    check = np.asarray(source_temp.points)

    if trigger:
        o3d.visualization.draw_geometries([source, target, axis_pcd])


    return source_temp, target_temp
def trabsformation_coordinate(source, target, transformation,trigger=False):
    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=np.array([0,0,0]))
    check = np.asarray(source.points)
    source.transform(transformation)
    check = np.asarray(source.points)
    target.transform(transformation)
    source.paint_uniform_color([1, 0.706, 0])
    target.paint_uniform_color([0, 0.651, 0.929])
    if trigger:
        o3d.visualization.draw_geometries([axis_pcd, source, target])

    return source,target

def rs_to_phx_pcd_registration(phx_client, realsense_client, change_matrix, rs_camera_id=0):
    phx_intrinsic_matrix = np.array([[1.33930543e+03, 0.00000000e+00, 3.34683556e+02],
                                     [0.00000000e+00, 1.43253751e+03, 4.66736263e+02],
                                     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    phx_distortion = np.array(
        [-0.12194237677679813, 0.18344112700622126, 0.00057639831338004, -0.00026201715594945677, 0])
    threshold = 0.02
    realsense_client.change_camera(camera_id=rs_camera_id)
    '''
    data preparation
    '''
    grayimg, depthnparray_float32, pcd = phx_client.getalldata()
    phx_extrinsic = Aruco_marker_estimation.get_extrinsic_matrix(img=grayimg, intr_matrix=phx_intrinsic_matrix,distortion=phx_distortion,trigger=True)
    phx_center = Aruco_marker_estimation.getcenter_two_aruco_maker(img=grayimg, pcd=pcd)
    print('phx_center:', phx_center)
    rs_extrinsic = realsense_client.get_extrinsic_matrix_two_aruco_maker(trigger=True)
    rs_ceter = realsense_client.getcenter_two_aruco_maker()
    print('rs_center:', rs_ceter)
    transform_matrix=np.dot(phx_extrinsic,np.linalg.inv(rs_extrinsic))
    # modification

    transform_matrix = np.dot(change_matrix,transform_matrix)
    print('modified_matrix:', transform_matrix)
    phx_pcd = o3d.geometry.PointCloud()
    pcdn = copy.deepcopy(pcd)
    phx_pcd.points = o3d.utility.Vector3dVector(pcdn)
    rs_pcd = realsense_client.depth2pcd()
    source_initial = rs_pcd
    target_initial = phx_pcd
    '''
    pcd work
    '''
    start_pos = np.array([-phx_center]).T
    start_rot_mat = np.array([[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])
    coordinate_build_matrix = np.hstack((start_rot_mat, start_pos))
    coordinate_build_matrix = np.vstack((coordinate_build_matrix, np.array([[0, 0, 0, 1]])))
    source, target = pcd_registration(source=source_initial, target=target_initial, transformation=transform_matrix, trigger=False)
    source, target = trabsformation_coordinate(source=source, target=target, transformation= coordinate_build_matrix, trigger=True)


if __name__=='__main__':
    # phxi_host = "127.0.0.1:18300"
    phx_client = phx.Phoxi()
    realsense_client=rs.RealSense()

    #camera1_pcd
    # change_matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    movement = np.array([[-220, +160, -200]]).T
    # # rotation = np.dot(rmt.matrix_generate(30, 'x'),rmt.matrix_generate(5, 'y'))
    rotation = rmt.matrix_generate(0, 'x')
    change_matrix = np.hstack((rotation,movement))
    change_matrix = np.vstack((change_matrix, np.array([[0, 0, 0, 1]])))

    rs_to_phx_pcd_registration(phx_client=phx_client,realsense_client=realsense_client,change_matrix=change_matrix,rs_camera_id=0)


    '''
    modification
    '''
    # check1 = np.asarray(source.points)
    # check2 = np.asarray(target.points)
    # movement = np.array([[0, 0, -1000]]).T
    # rotation = np.array([[1, 0, 0],
    #                           [0, 1, 0],
    #                           [0, 0, 1]])
    # change_matrix = np.hstack((movement, rotation))
    # change_matrix = np.vstack((change_matrix, np.array([[0, 0, 0, 1]])))
    # source, target = pcd_registration(source=source, target=target, transformation=change_matrix,
    #                                   trigger=True)








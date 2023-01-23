import open3d as o3d
import numpy as np
import copy

def draw_registration_result(source, target, transformation):
    # axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=np.array([0,0,0]))

    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)

    o3d.visualization.draw_geometries([source_temp, target_temp])

def robot_coordinate(source, target, transformation):
    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=np.array([0,0,0]))
    source.transform(transformation)
    target.transform(transformation)
    o3d.visualization.draw_geometries([axis_pcd, source, target])

    return source, target

if __name__ == "__main__":
    source_initial = o3d.io.read_point_cloud('data/pcd_object1.pcd', format='pcd')
    target_initial = o3d.io.read_point_cloud('data/pcd_object2.pcd', format='pcd')
    threshold = 0.02
    homography_transformation = np.load('data/extrinsic_matrix_pcd.npy')
    # pos1: [725.8834675   80.71593035 930.81910947]
    # start_pos = np.array([[703.40078856, 155.80866675, 902.31295062]]).T
    start_pos=np.array([[-668.98184382,  -67.59441751, -925.12990381]]).T
    start_rot_mat=np.array([[ 1, 0, 0],
     [ 0,  1, 0],
     [ 0,  0,  1]])
    robot_to_ee=np.hstack((start_rot_mat,start_pos))
    robot_to_ee=np.vstack((robot_to_ee,np.array([[0,0,0,1]])))
    homo=np.dot(robot_to_ee,homography_transformation)
    source, target = robot_coordinate(source_initial,target_initial,homo)

    init_source_to_target=np.array([[1,  0,  0, 0],
     [0,  -1,  0, 0],
     [0,  0,  -1, 0],[0, 0, 0 ,1]])
    print("Initial alignment")
    draw_registration_result(source, target, init_source_to_target)
    evaluation = o3d.pipelines.registration.evaluate_registration(source, target,
            threshold, init_source_to_target)
    print(evaluation)

    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(source, target, threshold, init_source_to_target,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    print("")
    draw_registration_result(source, target, reg_p2p.transformation)

    # print("Apply point-to-plane ICP")
    # reg_p2l = o3d.pipelines.registration.registration_icp(source, target, threshold, init_source_to_target,
    #         o3d.pipelines.registration.TransformationEstimationPointToPlane())
    # print(reg_p2l)
    # print("Transformation is:")
    # print(reg_p2l.transformation)
    # print("")
    # draw_registration_result(source, target, reg_p2l.transformation)
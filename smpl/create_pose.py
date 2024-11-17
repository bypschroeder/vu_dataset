import numpy as np
import pickle

def generate_random_pose(filepath):
    """
        Generates a random pose for the SMPL model based on modifying the numbers of the pose file manually.

        :param filepath: The path to save the pose data.
        :type filepath: str
        :return: The path to the pose data.
        :rtype: str
    """
    # np.random.seed()

    # x, z, y
    root_min = np.array([-0.1, -0.1, -0.1])
    root_max = np.array([0.1, 0.1, 0.1])

    pelvis_min = np.array([-0.5, -0.5, -0.5])
    pelvis_max = np.array([0.5, 0.5, 0.5])

    left_hip_min = np.array([-0.5, -0.5, -0.5])
    left_hip_max = np.array([0.5, 0.5, 0.5])

    right_hip_min = np.array([-0.5, -0.5, -0.5])
    right_hip_max = np.array([0.5, 0.5, 0.5])

    left_knee_min = np.array([-0.5, -0.5, -0.5])
    left_knee_max = np.array([0.5, 0.5, 0.5])

    right_knee_min = np.array([-0.5, -0.5, -0.5])
    right_knee_max = np.array([0.5, 0.5, 0.5])

    left_ankle_min = np.array([-0.5, -0.5, -0.5])
    left_ankle_max = np.array([0.5, 0.5, 0.5])

    right_ankle_min = np.array([-0.5, -0.5, -0.5])
    right_ankle_max = np.array([0.5, 0.5, 0.5])

    left_foot_min = np.array([-0.5, -0.5, -0.5])
    left_foot_max = np.array([0.5, 0.5, 0.5])

    right_foot_min = np.array([-0.5, -0.5, -0.5])
    right_foot_max = np.array([0.5, 0.5, 0.5])

    spine1_min = np.array([-0.5, -0.5, -0.5])
    spine1_max = np.array([0.5, 0.5, 0.5])

    spine2_min = np.array([-0.5, -0.5, -0.5])
    spine2_max = np.array([0.5, 0.5, 0.5])

    spine3_min = np.array([-0.5, -0.5, -0.5])
    spine3_max = np.array([0.5, 0.5, 0.5])

    neck_min = np.array([-0.5, -0.5, -0.5])
    neck_max = np.array([0.5, 0.5, 0.5])

    head_min = np.array([-0.5, -0.5, -0.5])
    head_max = np.array([0.5, 0.5, 0.5])

    jaw_min = np.array([-0.5, -0.5, -0.5])
    jaw_max = np.array([0.5, 0.5, 0.5])

    left_eye_min = np.array([-0.5, -0.5, -0.5])
    left_eye_max = np.array([0.5, 0.5, 0.5])

    right_eye_min = np.array([-0.5, -0.5, -0.5])
    right_eye_max = np.array([0.5, 0.5, 0.5])

    left_collar_min = np.array([-0.5, -0.5, -0.5])
    left_collar_max = np.array([0.5, 0.5, 0.5])

    left_shoulder_min = np.array([-0.5, -0.5, -0.5])
    left_shoulder_max = np.array([0.5, 0.5, 0.5])

    left_elbow_min = np.array([-0.5, -0.5, -0.5])
    left_elbow_max = np.array([0.5, 0.5, 0.5])

    left_wrist_min = np.array([-0.5, -0.5, -0.5])
    left_wrist_max = np.array([0.5, 0.5, 0.5])

    left_index1_min = np.array([-0.5, -0.5, -0.5])
    left_index1_max = np.array([0.5, 0.5, 0.5])

    left_index2_min = np.array([-0.5, -0.5, -0.5])
    left_index2_max = np.array([0.5, 0.5, 0.5])

    left_index3_min = np.array([-0.5, -0.5, -0.5])
    left_index3_max = np.array([0.5, 0.5, 0.5])

    left_middle1_min = np.array([-0.5, -0.5, -0.5])
    left_middle1_max = np.array([0.5, 0.5, 0.5])

    left_middle2_min = np.array([-0.5, -0.5, -0.5])
    left_middle2_max = np.array([0.5, 0.5, 0.5])

    left_middle3_min = np.array([-0.5, -0.5, -0.5])
    left_middle3_max = np.array([0.5, 0.5, 0.5])
    
    left_pinky1_min = np.array([-0.5, -0.5, -0.5])
    left_pinky1_max = np.array([0.5, 0.5, 0.5])

    left_pinky2_min = np.array([-0.5, -0.5, -0.5])
    left_pinky2_max = np.array([0.5, 0.5, 0.5])

    left_pinky3_min = np.array([-0.5, -0.5, -0.5])    
    left_pinky3_max = np.array([0.5, 0.5, 0.5])

    left_ring1_min = np.array([-0.5, -0.5, -0.5])
    left_ring1_max = np.array([0.5, 0.5, 0.5])

    left_ring2_min = np.array([-0.5, -0.5, -0.5])
    left_ring2_max = np.array([0.5, 0.5, 0.5])

    left_ring3_min = np.array([-0.5, -0.5, -0.5])
    left_ring3_max = np.array([0.5, 0.5, 0.5])

    left_thumb1_min = np.array([-0.5, -0.5, -0.5])
    left_thumb1_max = np.array([0.5, 0.5, 0.5])

    left_thumb2_min = np.array([-0.5, -0.5, -0.5])
    left_thumb2_max = np.array([0.5, 0.5, 0.5])

    left_thumb3_min = np.array([-0.5, -0.5, -0.5])
    left_thumb3_max = np.array([0.5, 0.5, 0.5])

    right_collar_min = np.array([-0.5, -0.5, -0.5])
    right_collar_max = np.array([0.5, 0.5, 0.5])

    right_shoulder_min = np.array([-0.5, -0.5, -0.5])
    right_shoulder_max = np.array([0.5, 0.5, 0.5])

    right_elbow_min = np.array([-0.5, -0.5, -0.5])
    right_elbow_max = np.array([0.5, 0.5, 0.5])

    right_wrist_min = np.array([-0.5, -0.5, -0.5])
    right_wrist_max = np.array([0.5, 0.5, 0.5])

    right_index1_min = np.array([-0.5, -0.5, -0.5])
    right_index1_max = np.array([0.5, 0.5, 0.5])

    right_index2_min = np.array([-0.5, -0.5, -0.5])
    right_index2_max = np.array([0.5, 0.5, 0.5])

    right_index3_min = np.array([-0.5, -0.5, -0.5])
    right_index3_max = np.array([0.5, 0.5, 0.5])

    right_middle1_min = np.array([-0.5, -0.5, -0.5])
    right_middle1_max = np.array([0.5, 0.5, 0.5])

    right_middle2_min = np.array([-0.5, -0.5, -0.5])
    right_middle2_max = np.array([0.5, 0.5, 0.5])

    right_middle3_min = np.array([-0.5, -0.5, -0.5])
    right_middle3_max = np.array([0.5, 0.5, 0.5])
    
    right_pinky1_min = np.array([-0.5, -0.5, -0.5])
    right_pinky1_max = np.array([0.5, 0.5, 0.5])

    right_pinky2_min = np.array([-0.5, -0.5, -0.5])
    right_pinky2_max = np.array([0.5, 0.5, 0.5])

    right_pinky3_min = np.array([-0.5, -0.5, -0.5])
    right_pinky3_max = np.array([0.5, 0.5, 0.5])

    right_ring1_min = np.array([-0.5, -0.5, -0.5])
    right_ring1_max = np.array([0.5, 0.5, 0.5])

    right_ring2_min = np.array([-0.5, -0.5, -0.5])
    right_ring2_max = np.array([0.5, 0.5, 0.5])

    right_ring3_min = np.array([-0.5, -0.5, -0.5])
    right_ring3_max = np.array([0.5, 0.5, 0.5])

    right_thumb1_min = np.array([-0.5, -0.5, -0.5])
    right_thumb1_max = np.array([0.5, 0.5, 0.5])

    right_thumb2_min = np.array([-0.5, -0.5, -0.5])
    right_thumb2_max = np.array([0.5, 0.5, 0.5])

    right_thumb3_min = np.array([-0.5, -0.5, -0.5])    
    right_thumb3_max = np.array([0.5, 0.5, 0.5])

    pose_data = {
        'betas': np.random.normal(0, 0.1, (1, 10)).astype(np.float32),
        'global_orient': np.random.normal(0, 0.1, (1, 3)).astype(np.float32),
        'transl': np.random.normal(0, 0.1, (1, 3)).astype(np.float32),
        'left_hand_pose': np.random.normal(0, 0.1, (1, 45)).astype(np.float32),
        'right_hand_pose': np.random.normal(0, 0.1, (1, 45)).astype(np.float32),
        'jaw_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),  # Smaller range for jaw
        'leye_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),
        'reye_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),
        'expression': np.random.normal(0, 0.1, (1, 10)).astype(np.float32),
        'body_pose': np.random.normal(0, 0.1, (1, 63)).astype(np.float32)  # 63 for SMPL model body pose
    }

    with open("D:\\Projects\\vu_blender\\smpl\\random_pose.pkl", "wb") as f:
        pickle.dump(pose_data, f)

    return filepath

if __name__ == '__main__':
    generate_random_pose("D:\\Projects\\vu_blender\\smpl\\random_pose.pkl")
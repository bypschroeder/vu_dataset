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
        'body_pose': np.random.normal(0, 0.2, (1, 63)).astype(np.float32)  # 63 for SMPL model body pose
    }

    with open("D:\\Projects\\vu_blender\\smpl\\random_pose.pkl", "wb") as f:
        pickle.dump(pose_data, f)

    return filepath
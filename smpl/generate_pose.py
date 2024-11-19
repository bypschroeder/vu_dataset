import os
import numpy as np
import pickle
from human_body_prior.tools.model_loader import load_vposer
from human_body_prior.tools.omni_tools import copy2cpu as c2c
from pathlib import Path

def generate_random_pose(output_path, num_samples=1):
    """
    Generates and saves a pose image using the SMPL model and VPoser model.

    :param bm_path: The path to the SMPL model.
    :type bm_path: str
    :param expr_dir: The path to the VPoser model.
    :type expr_dir: str
    :param output_image_path: The path to save the pose image.
    :type output_image_path: str
    :param num_samples: The number of samples to generate.
    :type num_samples: int
    """

    base_dir = Path(__file__).parent
    expr_dir = base_dir / "vposer_v1_0"

    # Loading VPoser model
    vposer_pt, _ = load_vposer(expr_dir, vp_model='snapshot')
    
    # Generate a random pose
    sampled_pose_body = c2c(vposer_pt.sample_poses(num_poses=num_samples))
    flat_pose_body = sampled_pose_body.reshape(sampled_pose_body.shape[1] * sampled_pose_body.shape[2] * sampled_pose_body.shape[3])
    flat_pose_body = np.expand_dims(flat_pose_body, axis=0)

    # Insert pose into SMPL model structure
    pose_dict = {
        'betas': np.zeros((1, 10), dtype=np.float32),
        'global_orient': np.zeros((1, 3), dtype=np.float32),
        'transl': np.zeros((1, 3), dtype=np.float32),
        'left_hand_pose': np.zeros((1, 45), dtype=np.float32),
        'right_hand_pose': np.zeros((1, 45), dtype=np.float32),
        'jaw_pose': np.zeros((1, 3), dtype=np.float32),
        'leye_pose': np.zeros((1, 3), dtype=np.float32),
        'reye_pose': np.zeros((1, 3), dtype=np.float32),
        'expression': np.zeros((1, 10), dtype=np.float32),
        'body_pose': flat_pose_body
    }

    # Export Pose to .pkl file
    with open(output_path, "wb") as f:
        pickle.dump(pose_dict, f)

    return output_path, pose_dict
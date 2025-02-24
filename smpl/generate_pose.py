import numpy as np
import pickle
from human_body_prior.tools.model_loader import load_vposer
from human_body_prior.tools.omni_tools import copy2cpu as c2c
from pathlib import Path


def generate_random_pose(output_path):
    """Generates a random pose for the SMPLX model.

    Args:
        output_path (str): The path to the output file as .pkl.

    Returns:
        str: The path to the output file.
        dict: The pose dictionary.
    """
    base_dir = Path(__file__).parent
    expr_dir = base_dir / "vposer_v1_0"

    # Loading VPoser model
    vposer_pt, _ = load_vposer(expr_dir, vp_model="snapshot")

    # Generate a random pose
    sampled_pose = c2c(vposer_pt.sample_poses(num_poses=1))
    flat_pose = sampled_pose.reshape(
        sampled_pose.shape[1] * sampled_pose.shape[2] * sampled_pose.shape[3]
    )
    flat_pose = np.expand_dims(flat_pose, axis=0)

    # Insert pose into SMPL model structure
    pose_dict = {
        "betas": np.zeros((1, 10), dtype=np.float32),
        "global_orient": np.zeros((1, 3), dtype=np.float32),
        "transl": np.zeros((1, 3), dtype=np.float32),
        "left_hand_pose": np.zeros((1, 45), dtype=np.float32),
        "right_hand_pose": np.zeros((1, 45), dtype=np.float32),
        "jaw_pose": np.zeros((1, 3), dtype=np.float32),
        "leye_pose": np.zeros((1, 3), dtype=np.float32),
        "reye_pose": np.zeros((1, 3), dtype=np.float32),
        "expression": np.zeros((1, 10), dtype=np.float32),
        "body_pose": flat_pose,
    }

    # Export Pose to .pkl file
    with open(output_path, "wb") as f:
        pickle.dump(pose_dict, f)

    return output_path, pose_dict

import os
import numpy as np
import pickle
from human_body_prior.body_model.body_model import BodyModel
from human_body_prior.tools.model_loader import load_vposer
from human_body_prior.tools.omni_tools import copy2cpu as c2c
from human_body_prior.tools.visualization_tools import imagearray2file
from human_body_prior.mesh.mesh_viewer import MeshViewer
import trimesh
from pathlib import Path

def generate_and_save_pose(bm_path, expr_dir, output_image_path, num_samples=1):
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
    # Lade das SMPL-Modell
    bm = BodyModel(bm_path=bm_path, model_type='smplx')
    
    # Lade das VPoser-Modell
    vposer_pt, _ = load_vposer(expr_dir, vp_model='snapshot')
    
    # Generiere Posen
    sampled_pose_body = c2c(vposer_pt.sample_poses(num_poses=num_samples))
    # print(sampled_pose_body) # 1 x 1 x 21 x 3 = 63 -> auch Größe des Arrays von body_pose
    flat_pose_body = sampled_pose_body.reshape(sampled_pose_body.shape[1] * sampled_pose_body.shape[2], sampled_pose_body.shape[3])
    # print(flat_pose_body) # 63

    pose_dict = {
        'betas': np.random.normal(0, 0.1, (1, 10)).astype(np.float32),
        'global_orient': np.random.normal(0, 0.1, (1, 3)).astype(np.float32),
        'transl': np.random.normal(0, 0.1, (1, 3)).astype(np.float32),
        'left_hand_pose': np.random.normal(0, 0.1, (1, 45)).astype(np.float32),
        'right_hand_pose': np.random.normal(0, 0.1, (1, 45)).astype(np.float32),
        'jaw_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),  # Smaller range for jaw
        'leye_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),
        'reye_pose': np.random.normal(0, 0.05, (1, 3)).astype(np.float32),
        'expression': np.random.normal(0, 0.1, (1, 10)).astype(np.float32),
        'body_pose': flat_pose_body
    }
    # Exakt gleiche Struktur mit gleicher Anzahl an Werten, allerdings ändert sich hier die Pose nicht

    print(pose_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, "random_pose2.pkl")

    with open(relative_path, "wb") as f:
        pickle.dump(pose_dict, f)

    # # Erstelle eine Ansicht der generierten Pose und speichere sie als Bild
    # view_angles = [0, 90, -90]  # Verschiedene Winkel für die Ansicht
    # imw, imh = 400, 400
    # mv = MeshViewer(width=imw, height=imh, use_offscreen=True)
    # images = np.zeros([len(view_angles), num_samples, 1, imw, imh, 3])

    # for cId in range(num_samples):
    #     bm.pose_body.data[:] = bm.pose_body.new(sampled_pose_body[cId].reshape(-1))
    #     body_mesh = trimesh.Trimesh(vertices=c2c(bm().v[0]), faces=c2c(bm.f))

    #     for rId, angle in enumerate(view_angles):
    #         # Drehe das Mesh und rendere es
    #         rotation_matrix = trimesh.transformations.rotation_matrix(np.radians(angle), (0, 1, 0))
    #         body_mesh.apply_transform(rotation_matrix)
    #         mv.set_meshes([body_mesh], group_name='static')
    #         images[rId, cId, 0] = mv.render()
    #         body_mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-angle), (0, 1, 0)))

    # # Speichere das Bild als PNG
    # imagearray2file(images, output_image_path)
    # print(f'Saved generated pose image at {output_image_path}')

if __name__ == '__main__':
    # Pfade zum SMPL-Modell und VPoser-Verzeichnis
    base_dir = Path(__file__).parent
    bm_path = base_dir / "models" / "smplx" / "SMPLX_MALE.npz"  # Pfad zum SMPL/SMPLX Modell
    expr_dir = base_dir / "vposer_v1_0"  # Pfad zum VPoser Modell
    
    output_image_path = base_dir / "output.png"
    generate_and_save_pose(str(bm_path), str(expr_dir), str(output_image_path))
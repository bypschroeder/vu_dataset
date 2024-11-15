import os
import numpy as np
import pickle
from human_body_prior.body_model.body_model import BodyModel
from human_body_prior.tools.model_loader import load_vposer
from human_body_prior.tools.omni_tools import copy2cpu as c2c
from human_body_prior.tools.visualization_tools import imagearray2file
from human_body_prior.mesh.mesh_viewer import MeshViewer
import trimesh

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

    # Erstelle eine Ansicht der generierten Pose und speichere sie als Bild
    view_angles = [0, 90, -90]  # Verschiedene Winkel für die Ansicht
    imw, imh = 400, 400
    mv = MeshViewer(width=imw, height=imh, use_offscreen=True)
    images = np.zeros([len(view_angles), num_samples, 1, imw, imh, 3])

    for cId in range(num_samples):
        bm.pose_body.data[:] = bm.pose_body.new(sampled_pose_body[cId].reshape(-1))
        body_mesh = trimesh.Trimesh(vertices=c2c(bm().v[0]), faces=c2c(bm.f))

        for rId, angle in enumerate(view_angles):
            # Drehe das Mesh und rendere es
            rotation_matrix = trimesh.transformations.rotation_matrix(np.radians(angle), (0, 1, 0))
            body_mesh.apply_transform(rotation_matrix)
            mv.set_meshes([body_mesh], group_name='static')
            images[rId, cId, 0] = mv.render()
            body_mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-angle), (0, 1, 0)))

    # Speichere das Bild als PNG
    imagearray2file(images, output_image_path)
    print(f'Saved generated pose image at {output_image_path}')

if __name__ == '__main__':
    # Pfade zum SMPL-Modell und VPoser-Verzeichnis
    bm_path = 'D:/Projects/vu_blender/smpl/models/smplx/SMPLX_NEUTRAL.npz'  # Pfad zu deinem SMPL/SMPLX Modell
    expr_dir = 'D:/Projects/vu_blender/smpl/vposer_v1_0'  # Pfad zum VPoser Modell
    
    output_image_path = r"D:\\Projects\\vu_blender\\output.png"
    generate_and_save_pose(bm_path, expr_dir, output_image_path)
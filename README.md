# Installation

### Code
1. Clone this repository.
2. Set up a venv with python 3.11.xx ``python -m venv venv`` and set it as your Python Interpreter.
3. Activate the venv in the Terminal with ``venv\Scripts\activate``
4. Install the dependencies with ``pip install -r ./requirements.txt``

### Blender
It is recommended to install a fresh version of Blender for your production setup.
Additionally, add Blender's installation folder to your system's PATH environment variable for easier execution.

To install the required addon and setup Blender, run the setup.py script with ``blender --python setup.py``. 

Modify the configuration file as needed for settings like Cycles and others.

Now you can start the main-script by running ``blender --python main.py`` or if you want to run it in background ``blender --background --python main.py``

# VPoser
When running the VPoser to generate a SMPLX-Pose and visualize it with an SMPLX-Model some dependencies need to be adjusted.

1. torchgeometry: torchgeometry\core\conversions.py, line 302, 
    - mask_c1 = mask_d2 * (1 - mask_d0_d1) => mask_c1 = mask_d2 * ~(mask_d0_d1)
    - mask_c2 = (1 - mask_d2) * mask_d0_nd1 => mask_c2 = ~(mask_d2) * mask_d0_nd1
    - mask_c3 = (1 - mask_d2) * (1 - mask_d0_nd1) => mask_c3 = ~(mask_d2) * ~(mask_d0_nd1)
2. human_body_prior: human_body_prior\body_model\body_model.py
    -  verts, joints = lbs(betas=shape_components, pose=full_pose, v_template=self.v_template,
                         shapedirs=shapedirs, posedirs=self.posedirs,
                         J_regressor=self.J_regressor, parents=self.kintree_table[0].long(),
                         lbs_weights=self.weights,
                         dtype=self.dtype)
    
    - verts, joints = lbs(betas=shape_components, pose=full_pose, v_template=self.v_template,
                shapedirs=shapedirs, posedirs=self.posedirs,
                J_regressor=self.J_regressor, parents=self.kintree_table[0].long(),
                lbs_weights=self.weights)

# TODOs

- [x] Blender crashes fixen
- [x] Installationsanleitung + Dokumentation
- [ ] Mehr Tops/Bottoms erstellen in XS - XXL
- [ ] Hosenbund in Blender an Hüfte anpassen und pinnen?
- [x] SMPLX-Posen generieren 
- [x] Mesh in 1 Farbe, damit man es unterscheiden kann
- [x] 3 Bilder einmal nur Mesh, nur Kleidung und beides
- [x] 1x .obj, 3 Bilder, 1x SMPL-Pose, 1x Größe, Gewicht, Geschlecht, Kleidergröße
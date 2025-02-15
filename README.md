# VU_Blender

This is a Blender script to generate 3D avatars with SMPLX models and fit clothes to them.

## Installation

### Code

1. Clone this repository.
2. Set up a venv with python 3.11.xx (only works with 3.11 or lower) `python -m venv venv` and set it as your Python Interpreter.
3. Activate the venv in the Terminal with `venv\Scripts\activate`.
4. Install the dependencies with `pip install -r ./requirements.txt`.
5. Download the [Blender-Addon](https://nextcloud.hof-university.de/s/SXQAAxskkddQD4E), [VPoser](https://nextcloud.hof-university.de/s/jFzqDKyj8DwDwE7) and the [Clothes](https://nextcloud.hof-university.de/s/FL7qc6ywYTGyEgK). Put them in the directory like this:

```bash
   vu_blender
   ├── clothing
   │   ├── models
   │   │   ├── t-shirt
   │   │   ├── ...
   ├── smpl
   │   ├── vposer_v1_0
   │   ├── smplx_blender_addon_20220623.zip # Do not unzip this
   └── ...
```

### Blender

It is recommended to install a fresh version of Blender for your production setup.
Additionally, add Blender's installation folder to your system's PATH environment variable for easier execution.

To install the required addon and setup Blender, run the setup.py script with `blender --python setup.py`.

### Configs

The configs are located in the `config` folder. There is a base config file `config.json` which stores the general settings for the script. For each garment, a seperate config file is required. The config files are located in the `config/garments` folder. These store individual settings for each garment.

### VPoser

On the first run, an error will occur when generating an SMPLX-Pose with Vposer. To fix this, adjust the following lines in `.venv/lib/site-packages/torchgeometry/core/conversions.py`:

- line 302: Replace `mask_c1 = mask_d2 * (1 - mask_d0_d1)` with `mask_c1 = mask_d2 * ~(mask_d0_d1)`
- line 303: Replace `mask_c2 = (1 - mask_d2) * mask_d0_nd1` with `mask_c2 = ~(mask_d2) * mask_d0_nd1`
- line 304: Replace `mask_c3 = (1 - mask_d2) * (1 - mask_d0_nd1)` with `mask_c3 = ~(mask_d2) * ~(mask_d0_nd1)`

## Usage

Run the following command to start the script:

```bash
blender -b -P main.py -- --iterations {number of iterations} --garments {list of garments} --gender {gender of avatar} --output_path {path where the results should be saved}
```

Blender arguments:

- `-b` (`--background`): Run Blender in the background.
- `-P` (`--python`): Specify the Python script to run.
- `--`: This is required to seperate blender arguments from script arguments.

Script arguments:

- `--iterations`: The number of iterations to run for each garment.
- `--garments`: Specify one or more garments to use. If not specified all garments will be processed.
- `--gender`: The gender of the avatar. If not specified, a random gender will be used.
- `--output_path`: The output path for the results.

Example:

```bash
blender -b -P main.py -- --iterations 10 --garments t-shirt hoodie --output_path ./output
```

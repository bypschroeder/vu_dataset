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
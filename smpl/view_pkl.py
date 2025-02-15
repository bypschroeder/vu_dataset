import pickle
import os

with open(os.path.abspath("./smpl/random_pose.pkl"), "rb") as f:
    data = pickle.load(f)

print(data)

import pickle

path = "D:\\Projects\\vu_blender\\smpl\\random_pose.pkl"

with open(path, 'rb') as f:
    data = pickle.load(f)

print(data) 
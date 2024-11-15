import pickle

path = "D:\\Projects\\vu_blender\\output.pkl"

with open(path, 'rb') as f:
    data = pickle.load(f)

print(data) 
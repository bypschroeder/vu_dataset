import pickle

path = "D:\\Projects\\vu_blender\\000.pkl"

with open(path, 'rb') as f:
    data = pickle.load(f)

print(data) 
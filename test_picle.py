import pickle

with open('dictionary', 'rb') as f:
    x = pickle.load(f)
    print(x)
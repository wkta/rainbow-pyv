import pickle
from internal import MAP as legacyMAP


# fix imports for piclk ok
import sys
sys.modules['MAP'] = legacyMAP


with open('assets/WORLDS/MainWorldxx', 'rb') as fptr:
    obj = pickle.load(fptr)
    print(obj)

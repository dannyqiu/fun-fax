import base64
import numpy as np

def normalize_range(r):
    r = np.log(r)
    min_r = np.min(r)
    max_r = np.max(r)
    normalized_r = (r - min_r) / (max_r - min_r)
    return np.sqrt(normalized_r)

def encode_numpy_array(arr):
    b = base64.b64encode(arr)
    return b.decode('utf-8')

def decode_numpy_array(encoded_arr):
    b = base64.b64decode(encoded_arr)
    return np.frombuffer(b, dtype=np.float32)

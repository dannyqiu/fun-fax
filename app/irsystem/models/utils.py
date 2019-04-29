import numpy as np

def normalize_range(r):
    r = np.log(r)
    min_r = np.min(r)
    max_r = np.max(r)
    normalized_r = (r - min_r) / (max_r - min_r)
    return np.sqrt(normalized_r)

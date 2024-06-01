import numpy as np

def smooth(trajectory, radius):
    smoothed_trajectory = np.copy(trajectory)
    for i in range(radius, len(trajectory) - radius):
        smoothed_trajectory[i] = np.mean(trajectory[i-radius:i+radius], axis=0)
    return smoothed_trajectory

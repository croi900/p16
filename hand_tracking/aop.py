import numpy as np


def angle_between_points(a, b, c):
    # Convert points to numpy arrays
    a, b, c = np.array(a), np.array(b), np.array(c)

    # Calculate vectors
    ab = b - a
    bc = c - b

    # Compute magnitudes
    ab_norm = np.linalg.norm(ab)
    bc_norm = np.linalg.norm(bc)

    # Handle zero-length vectors
    if ab_norm == 0 or bc_norm == 0:
        raise ValueError("One of the vectors has zero length.")

    # Calculate the cosine of the angle
    cos_theta = np.dot(ab, bc) / (ab_norm * bc_norm)

    # Clamp to avoid numerical errors
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    # Compute the angle in radians
    angle = np.arccos(cos_theta)
    return angle * 180 / np.pi


def angle_between_points_2d(a, b, c):
    # Convert points to numpy arrays and keep only x, y coordinates
    a, b, c = np.array(a[:2]), np.array(b[:2]), np.array(c[:2])

    # Calculate vectors
    ab = b - a
    bc = c - b

    # Compute magnitudes
    ab_norm = np.linalg.norm(ab)
    bc_norm = np.linalg.norm(bc)

    # Handle zero-length vectors
    if ab_norm == 0 or bc_norm == 0:
        raise ValueError("One of the vectors has zero length.")

    # Calculate the cosine of the angle
    cos_theta = np.dot(ab, bc) / (ab_norm * bc_norm)

    # Clamp to avoid numerical errors
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    # Compute the angle in radians
    angle = np.arccos(cos_theta)
    return angle * 180 / np.pi


import numpy as np
from ripser import ripser
import persim
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def compute_angle_constrained_distance_matrix(points, normals, max_angle_degrees=45):
    """
    Compute a distance matrix where points are considered infinitely far apart
    if their normal vectors differ by more than max_angle_degrees.
    """
    # Compute pairwise distances
    distances = squareform(pdist(points))
    
    # Compute angles between normal vectors
    # Normalize normals to unit vectors
    normals = normals / np.linalg.norm(normals, axis=1)[:, np.newaxis]
    
    # Compute dot products between all pairs of normals
    dot_products = np.dot(normals, normals.T)
    # Clip to [-1, 1] to avoid numerical errors
    dot_products = np.clip(dot_products, -1.0, 1.0)
    angles = np.arccos(dot_products)
    angles_degrees = np.degrees(angles)
    
    # Set distances to infinity where angle constraint is violated
    distances[angles_degrees > max_angle_degrees] = np.inf
    
    return distances

def compute_segmented_persistence(points, normals, max_angle_degrees=45, max_dim=2):
    """
    Compute persistence diagrams with normal angle constraints.
    """
    # Compute distance matrix with angle constraints
    distances = compute_angle_constrained_distance_matrix(
        points, normals, max_angle_degrees
    )
    
    # Compute persistence diagrams using the modified distances
    diagrams = ripser(distances, maxdim=max_dim, distance_matrix=True)
    
    return diagrams

def visualize_point_cloud_with_segments(points, normals, max_angle_degrees=45):
    """
    Visualize point cloud with colors indicating connected components
    based on normal angle constraints.
    """
    # Compute distance matrix with angle constraints
    distances = compute_angle_constrained_distance_matrix(
        points, normals, max_angle_degrees
    )
    
    # Find connected components (segments)
    from scipy.sparse.csgraph import connected_components
    _, labels = connected_components(distances < np.inf)
    
    # Plot
    fig = plt.figure(figsize=(15, 5))
    
    # Point cloud colored by segments
    ax1 = fig.add_subplot(121, projection='3d')
    scatter = ax1.scatter(points[:, 0], points[:, 1], points[:, 2], 
                         c=labels, cmap='tab20')
    ax1.set_title('Segmented Point Cloud')
    plt.colorbar(scatter)
    
    # Normal vectors
    ax2 = fig.add_subplot(122, projection='3d')
    # Plot a subset of normals for clarity
    subset = np.random.choice(len(points), size=min(100, len(points)), replace=False)
    ax2.scatter(points[subset, 0], points[subset, 1], points[subset, 2], 
                c=labels[subset], cmap='tab20')
    # Plot normal vectors
    ax2.quiver(points[subset, 0], points[subset, 1], points[subset, 2],
               normals[subset, 0], normals[subset, 1], normals[subset, 2],
               length=0.1, normalize=True)
    ax2.set_title('Normal Vectors')
    
    plt.tight_layout()
    return fig

def analyze_face_topology(points, normals, max_angle_degrees=45, max_dim=2):
    """
    Complete analysis of face topology using normal-constrained persistence.
    """

    diagrams = compute_segmented_persistence(points, normals, 
                                           max_angle_degrees, max_dim)
    
    fig1 = visualize_point_cloud_with_segments(points, normals, max_angle_degrees)
    
    # Plot persistence diagrams
    fig2, ax = plt.subplots(figsize=(8, 6))
    persim.plot_diagrams(diagrams['dgms'], ax=ax)
    ax.set_title('Persistence Diagram')
    
    return {
        'diagrams': diagrams,
        'visualization_fig': fig1,
        'persistence_fig': fig2
    }

if __name__ == "__main__":

    ply_file_1 = "color_group_43_211_0.ply"
    # color_group_113_141_0.ply
    ply_file_2 = "file2.ply"







    # Generate sample data (you would replace this with your face point cloud)
    n_points = 100
    points = np.random.rand(n_points, 3)
    # Generate random unit normals
    normals = np.random.randn(n_points, 3)
    normals = normals / np.linalg.norm(normals, axis=1)[:, np.newaxis]
    
    results = analyze_face_topology(points, normals, max_angle_degrees=45)
    plt.show()
from plyfile import PlyData
import numpy as np
import matplotlib.pyplot as plt
from ripser import ripser
from gudhi.wasserstein import wasserstein_distance
from persim import plot_diagrams

def load_vs(ply_files):
    vertices = []
    for ply_file in ply_files:
        plydata = PlyData.read(ply_file)
        vertices_indiv = np.array([[v[0], v[1], v[2]] for v in plydata['vertex']])
        vertices.append(vertices_indiv)
    return vertices

if __name__ == "__main__":
    points_list = load_vs(["color_group_files/color_group_43_211_0.ply", "color_group_files/color_group_113_141_0.ply"])  # Identify corresponding groups in Blender and note their ply files
    segment_points = np.vstack(points_list)

    vertex_file = 'objFiles/nosereference.obj'  # reference obj file
    vertices = []
    with open(vertex_file, 'r') as v_file:
        for line in v_file:
            parts = line.strip().split()
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:])
                vertices.append([x, y, z])
    model_points = np.array(vertices)

    seg_diagram_0 = ripser(segment_points, maxdim=1)['dgms'][0]
    model_diagram_0 = ripser(model_points, maxdim=1)['dgms'][0]
    seg_diagram_1 = ripser(segment_points, maxdim=1)['dgms'][1]
    model_diagram_1 = ripser(model_points, maxdim=1)['dgms'][1]

    plot_diagrams([seg_diagram_0, model_diagram_0] , labels=['Segmented', 'Model'])
    plt.title("Dimension 0")
    plt.show()

    plot_diagrams([seg_diagram_1, model_diagram_1] , labels=['Segmented', 'Model'])
    plt.title("Dimension 1")
    plt.show()

    cost, matchings = wasserstein_distance(seg_diagram_0, model_diagram_0, matching=True, order=1, internal_p=2)
    print(f"Wasserstein distance value (Dim 0) = {cost:.2f}")

    cost, matchings = wasserstein_distance(seg_diagram_1, model_diagram_1, matching=True, order=1, internal_p=2)
    print(f"Wasserstein distance value (Dim 1) = {cost:.2f}")


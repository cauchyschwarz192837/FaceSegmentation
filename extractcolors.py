from plyfile import PlyData, PlyElement
from collections import defaultdict
import numpy as np

if __name__ == "__main__":
    plydata = PlyData.read('output_files/output_file_1.ply')  # should change this according to which file to be analyzed
    vertex_data = plydata['vertex']
    vertices = np.array([vertex_data['x'], vertex_data['y'], vertex_data['z']]).T
    colors = np.array([vertex_data['red'], vertex_data['green'], vertex_data['blue']]).T

    color_groups = defaultdict(list)
    for vertex, color in zip(vertices, colors):
        color_tuple = tuple(color)
        color_groups[color_tuple].append(vertex)

    for color, vertex_list in color_groups.items():
        color_str = f"{color[0]}_{color[1]}_{color[2]}"
        output_ply = f"color_group_{color_str}.ply"

        color_data = np.array([(v[0], v[1], v[2], color[0], color[1], color[2]) for v in vertex_list], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])

        vertex_element = PlyElement.describe(color_data, 'vertex')
        PlyData([vertex_element], text = True).write(output_ply)

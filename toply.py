import numpy as np

def read_obj_with_cols(obj_file):
    vertices = []
    faces = []

    with open(obj_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                r, g, b = map(float, parts[4:7])
                vertices.append((x, y, z, r, g, b))

            elif parts[0] == 'f':
                face = [int(idx.split('/')[0]) - 1 for idx in parts[1:]]
                faces.append(face)

    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32)

def write_ply(vertices, faces, ply_file):
    with open(ply_file, 'w') as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(vertices)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")
        file.write("property uchar red\n")
        file.write("property uchar green\n")
        file.write("property uchar blue\n")
        file.write(f"element face {len(faces)}\n")  # number of faces
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")

        for v in vertices:
            x, y, z, r, g, b = v
            file.write(f"{x} {y} {z} {int(r * 255)} {int(g * 255)} {int(b * 255)}\n")

        for f in faces:
            file.write(f"{len(f)} {' '.join(map(str, f))}\n")

if __name__ == "__main__":
    obj_file = "vertex_region_files/vertex_regions_1.obj"  # should change this accordingly to which file to be analyzed
    ply_file = "output_files/output_file_1.ply"  # should change this accordingly to which file to be analyzed

    vertices, faces = read_obj_with_cols(obj_file)
    write_ply(vertices, faces, ply_file)

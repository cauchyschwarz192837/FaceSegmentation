import numpy as np
from quickunion import WeightedQuickUnionWithPathCompressionUF
from scipy.spatial import KDTree
from tqdm import tqdm

def compute_normal_angle(normal1, normal2):
    dot_product = np.dot(normal1, normal2) / (np.linalg.norm(normal1) * np.linalg.norm(normal2))
    dot_product = np.clip(dot_product, -1.0, 1.0)
    angle = np.arccos(dot_product)
    return angle

def compute_curvature_criterion(vertex1, vertex2):  
    # See 
    # https://pixl.cs.princeton.edu/pubs/Rusinkiewicz_2004_ECA/curvpaper.pdf, 
    # http://rodolphe-vaillant.fr/entry/33/curvature-of-a-triangle-mesh-definition-and-computation
    # TODO: Implement curvature computation between vertex1 and vertex2
    return True

def inRange(val, min, max):
    if min <= val <= max:
        return True
    
def grow_regions(points, normals, vertex_to_normal_map, edges, theta_max, eps_min, eps_max):
    tree = KDTree(points)
    unionArray = WeightedQuickUnionWithPathCompressionUF(len(points))
    death_times = np.full(len(points), np.inf)

    # edge_set = set(tuple(sorted(edge)) for edge in edges)

    total_steps = int((eps_max - eps_min) / 0.1) + 1
    progBar = tqdm(total = total_steps, desc = "Growing Regions", unit = "step")

    eps = eps_min
    while eps <= eps_max:
        for i, point in enumerate(points):
            neighbors = tree.query_ball_point(point, r=eps)
            similar_nn = []

            # Check if there is a normal for this vertex
            if not i in vertex_to_normal_map:
                continue

            for nn in neighbors:
                if nn == i:
                    continue

                # Check if normals are within bounds
                # if i >= len(normals) or nn >= len(normals):
                #     print(f"Skipping out-of-bounds normal index: i={i}, nn={nn}")
                #     continue

                # Check if there is a normal for this neighbor
                if not nn in vertex_to_normal_map:
                    continue

                # Check angle
                theta = compute_normal_angle(normals[vertex_to_normal_map[i]], normals[vertex_to_normal_map[nn]])
                if not (theta <= theta_max):
                    continue

                similar_nn.append(nn)

            if similar_nn:
                min_nn = min(similar_nn)

            for nn in similar_nn:
                if unionArray.find(nn) != unionArray.find(min_nn):
                    death_times[nn] = eps  # Set death time for the point, record for persistence
                    unionArray.union(nn, min_nn)  # Merge regions

        eps += 0.1  # arbitrary
        progBar.update(1)

    progBar.close()
    return unionArray, death_times

def get_regions_with_cols(vertices, labels, faces, filename):
    max_label = max(labels)

    with open(filename, "w") as objfile:
        for i, vertex in enumerate(vertices):
            color = labels[i] / max_label  # Value between 0 and 1
            color += np.random.rand()
            objfile.write(f"v {vertex[0]} {vertex[1]} {vertex[2]} {color} {1-color} 0\n")

        for face in faces:
            objfile.write(f"f {' '.join(str(v + 1) for v in face)}\n")

#-----------------------------------------------------------------------------
# DATA READING

if __name__ == "__main__":

    vertex_file = 'data_text_files/vertices2.txt'
    normal_file = 'data_text_files/normals2.txt'
    face_file = 'data_text_files/faces2.txt'

    # Parse vertices
    vertices = []
    with open(vertex_file, 'r') as v_file:
        for line in v_file:
            parts = line.strip().split()
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:])
                vertices.append([x, y, z])
    vertices = np.array(vertices)

    unionArray = (len(vertices)) # USE THIS FOR LATER UNION OPERATIONS

    # Parse vertex normals, assume each vertex has its own normal
    normals = []
    with open(normal_file, 'r') as vn_file:
        for line in vn_file:
            parts = line.strip().split()
            if parts[0] == 'vn':
                nx, ny, nz = map(float, parts[1:])
                normals.append([nx, ny, nz])
    normals = np.array(normals)

    # Parse faces
    faces = []
    vertex_to_normal_map = {}
    with open(face_file, 'r') as f_file:
        for line in f_file:
            parts = line.strip().split()
            if len(parts) > 4:
                print("Polygonal face that is not triangular")  # Is this necessary if we just triangulate the mesh in Blender?
                
            if parts[0] == 'f':
                face = []
                for v in parts[1:]:
                    vertex_index = int(v.split('/')[0]) - 1  # OBJ indices are 1-based
                    face.append(vertex_index)

                    vertex_to_normal_map[vertex_index] = int(v.split('/')[2]) - 1
                faces.append(face)
    faces = np.array(faces)

    edges_set = set()
    for face in faces:
        v0, v1, v2 = face
        edges_set.update({
            tuple(sorted([v0, v1])),
            tuple(sorted([v1, v2])),
            tuple(sorted([v2, v0])),
        })
    edges = list(edges_set)

    # Thresholds and parameters
    theta_max_values = [np.pi/36, np.pi/34, np.pi/32, np.pi/30, np.pi/28, np.pi/26, np.pi/24, np.pi/22, np.pi/20, np.pi/18, np.pi/16, np.pi/14, np.pi/12, np.pi/10, np.pi/8, np.pi/6, np.pi/4, np.pi/2]
    eps_min = 0.001
    eps_max = 20

    for i, theta_max in enumerate(theta_max_values):
        unionArray, death_times = grow_regions(vertices, normals, vertex_to_normal_map, edges, theta_max, eps_min, eps_max)
        labels = np.array([unionArray.find(i) for i in range(len(vertices))])

        # print("Labels:", labels)
        # print("Death Times:", death_times)

        get_regions_with_cols(vertices, labels, faces, "vertex_region_files/vertex_regions_" + str(i) + ".obj")
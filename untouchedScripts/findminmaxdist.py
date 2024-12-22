import numpy as np

vertex_file = 'vertices2.txt'
vertices = []
with open(vertex_file, 'r') as v_file:
    for line in v_file:
        parts = line.strip().split()
        if parts[0] == 'v':
            x, y, z = map(float, parts[1:])
            vertices.append([x, y, z])
vertices = np.array(vertices)

min = 100000000000
max = 0
total_comparisons = len(vertices) ** 2
print("Beginning " + str(total_comparisons) + " comparisons...")
step_size = total_comparisons / 100
comparisons_made = 0
steps_taken = 0

for p1 in vertices:
    for p2 in vertices:
        if (p1 == p2).all():
            continue
        distance = np.linalg.norm(p1 - p2)
        if distance > max:
            max = distance
        if distance < min:
            min = distance

        comparisons_made += 1
        if comparisons_made > (steps_taken + 1) * step_size:
            print(str((steps_taken + 1)) + "%")
            steps_taken += 1

print("Minimum distance: " + str(min))
print("Maximum distance: " + str(max))
if __name__ == "__main__":
    input_file = 'objFiles/secondlowresface.obj' # we are testing on this OBJ file

    v_file = 'data_text_files/vertices2.txt'
    vertex_count = 0
    vn_file = 'data_text_files/normals2.txt'
    normal_count = 0
    f_file = 'data_text_files/faces2.txt'
    face_count = 0

    with open(input_file, 'r') as obj_file, \
        open(v_file, 'w') as v_out, \
        open(vn_file, 'w') as vn_out, \
        open(f_file, 'w') as f_out:
        
        for line in obj_file:
            if line.startswith('v '):  
                v_out.write(line)
                vertex_count += 1
            elif line.startswith('vn '): 
                vn_out.write(line)
                normal_count += 1
            elif line.startswith('f '):
                f_out.write(line)
                face_count += 1

    print(f"{vertex_count} vertices saved in: {v_file}")
    print(f"{normal_count} normals saved in: {vn_file}")
    print(f"{face_count} faces saved in: {f_file}")

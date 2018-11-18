import numpy as np
from extract_data import extract_data


def floyd(dis_map):
    vertices_num = len(dis_map)
    for k in range(1, vertices_num):
        for i in range(1, vertices_num):
            for j in range(1, vertices_num):
                temp = dis_map[i][k] + dis_map[k][j]
                if dis_map[i][j] > temp:
                    dis_map[i][j] = temp
    for i in range(vertices_num):
        dis_map[i][i] = 0
    return dis_map


def get_information(filename):
    info, req_edges, dis_map = extract_data(filename)
    dis_map = floyd(dis_map)
    return info, req_edges, dis_map


if __name__ == '__main__':
    filename = 'C:\FILES and WORKS\学习\大三上\AI\AILAB\CARP\CARPResource\Proj2_Carp\CARP_samples\gdb1.dat'
    info, req_edges, dis_map = extract_data(filename)
    # print(dis_map)
    # print()
    dis_map = floyd(dis_map)
    print(dis_map)

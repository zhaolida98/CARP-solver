import numpy as np

def extract_data(filename):
    file = open(filename,'r')
    req_edges = {}
    content = []

    # 初始化json
    keys = ('name', 'vertices', 'depot', 'required_edges','non_required_edges', 'vehicles','capacity', 'total_cost')
    info = {k: None for k in keys}

    # 读取文件
    counter = 0
    for i in file:
        counter += 1
        if counter < 9:
            temp = i.strip('\n').split(' : ')
        else:
            temp = []
            ij = i.strip('\n').split(' ')
            for char in ij:
                if char: temp.append(char)
        content.append(temp)

    # 获取需求边，保存格式为（v1,v2) : demand
    for i in range(9, len(content)):
        if content[i] == 'END':
            break
        if content[i][3] != '0':
            v1 = int(content[i][0])
            v2 = int(content[i][1])
            cost = int(content[i][2])
            demand = int(content[i][3])
            req_edges[(v1, v2)] = (cost, demand)
            req_edges[(v2, v1)] = (cost, demand)
    # print(req_edges)

    # 获取json信息
    # print(content)
    for i in range(8):
        if i == 0:
            info[keys[i]] = content[i][1]
        else:
            info[keys[i]] = int(content[i][1])

    # 初始化地图二维数组
    vertices = info['vertices']+1
    dis_map = np.zeros((vertices,vertices))
    for i in range(1, vertices):
        for j in range(1, vertices):
            dis_map[i][j] = float('inf')
    for k in range (9,len(content) - 1):
        i = content[k]
        ver1 = int(i[0])
        ver2 = int(i[1])
        cost = int(i[2])
        demand = int(i[3])
        dis_map[ver1][ver2] = cost
        dis_map[ver2][ver1] = cost
    return info, req_edges, dis_map

if __name__ == '__main__':
    filename = 'C:\FILES and WORKS\学习\大三上\AI\AILAB\CARP\CARPResource\Proj2_Carp\CARP_samples\gdb1.dat'
    info, req_edges, dis_map = extract_data(filename)
    print(info, req_edges, dis_map)
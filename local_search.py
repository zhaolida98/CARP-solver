import copy
from PathScanning import *

def single_insertion(solution, req_edges, info, dis_map):
    # print('single insertion begin')
    s = copy.deepcopy(solution[0])
    c = solution[1]
    fin = (None, None, None, None, 0) # remove route num, remove task num, insert route num, insert task num, cos_var
    len_s = len(solution[0])
    for i in range(len_s):
        temp1 = cal_cost(s[i], req_edges, dis_map)
        for j in range(len(s[i])):
            removed_item = s[i][j]
            # print('remove',i,j, 'lenth s is', len_s, 'len(s[i]) is', len(s[i]))
            s[i].remove(removed_item)
            s_wait_insert = copy.deepcopy(s)
            temp2 = cal_cost(s[i], req_edges, dis_map)
            dec = abs(temp2 - temp1)
            for k in range(len_s):
                temp3 = cal_cost(s[k], req_edges, dis_map)
                for l in range(len(s[k])):
                    s[k].insert(l, removed_item)
                    # print('insert in', k,l)
                    temp4 = cal_cost(s[k], req_edges, dis_map)
                    if temp4 > info['capacity']:
                        s = copy.deepcopy(s_wait_insert)
                        break
                    inc = abs(temp4 - temp3)
                    delta = int(inc - dec)
                    if delta < fin[4]:
                        fin = (i, j, k, l, delta)
                    s = copy.deepcopy(s_wait_insert)

            s = copy.deepcopy(solution[0])
    s = copy.deepcopy(solution[0])
    # print(fin)
    if fin == (None, None, None, None, 0):
        # print('best of single insertion is', solution[1])
        # print(solution[0])
        return solution
    element = s[fin[0]][fin[1]]
    s[fin[0]].remove(s[fin[0]][fin[1]])
    # print(element)
    s[fin[2]].insert(fin[3], element)
    c = c + fin[4]
    # print(s)
    # print(c)
    # to_format(s, c)
    return single_insertion((s,c), req_edges, info, dis_map)


def double_insertion(solution, req_edges, info, dis_map):
    # print('double_insertions begin')
    s = copy.deepcopy(solution[0])
    c = solution[1]
    # fin: remove route num, remove task num, insert route num1,
    # insert task num1,insert route num2, insert task num2, cos_var
    fin = (None, None, None, None, None, None, 0)
    len_s = len(solution[0])
    for i in range(len_s):
        temp1 = cal_cost(s[i], req_edges, dis_map)
        for j in range(len(s[i]) - 1):
            removed_item1 = s[i][j]
            removed_item2 = s[i][j+1]
            # print('remove',i,j, 'lenth s is', len_s, 'len(s[i]) is', len(s[i]))
            s[i].remove(removed_item1)
            s[i].remove(removed_item2)
            # 保存等待第一条边插入的状态
            s_wait_insert1 = copy.deepcopy(s)
            temp2 = cal_cost(s[i], req_edges, dis_map)
            dec = abs(temp2 - temp1)
            for k in range(len_s):
                temp3 = cal_cost(s[k], req_edges, dis_map)
                for l in range(len(s[k])):
                    s[k].insert(l, removed_item1)
                    # print('insert in', k,l)
                    # 保存等待第二条边插入的状态
                    s_wait_insert2 = copy.deepcopy(s)
                    temp4 = cal_cost(s[k], req_edges, dis_map)
                    # 超出容量，回到待插入第一边状态
                    if temp4 > info['capacity']:
                        s = copy.deepcopy(s_wait_insert1)
                        break
                    inc1 = abs(temp4 - temp3)

                    for m in range(len_s):
                        temp5 = cal_cost(s[m], req_edges, dis_map)
                        for n in range(len(s[m])):
                            s[m].insert(n, removed_item2)
                            # print('insert in', m,n)
                            temp6 = cal_cost(s[m], req_edges, dis_map)
                            # 超出容量，回到带插入第二条边的状态
                            if temp6 > info['capacity']:
                                s = copy.deepcopy(s_wait_insert2)
                                break
                            inc2 = abs(temp6 - temp5)
                            delta = int(inc1 + inc2 - dec)
                            if delta < fin[6]:
                                fin = (i, j, k, l, m, n, delta)
                            # 回到待插入第二条边状态
                            s = copy.deepcopy(s_wait_insert2)
                    # 回到待插入第一边状态
                    s = copy.deepcopy(s_wait_insert1)
            # 回到移除边之前的状态
            s = copy.deepcopy(solution[0])
    # 查找完毕，回到初始状态
    s = copy.deepcopy(solution[0])
    # print(fin)
    if fin == (None, None, None, None, None, None, 0):
        # print('best of double insertion is', solution[1])
        # print(solution[0])
        return solution
    element1 = s[fin[0]][fin[1]]
    element2 = s[fin[0]][fin[1] + 1]
    s[fin[0]].remove(element1)
    s[fin[0]].remove(element2)
    # print("remove:",element1, element2)
    s[fin[2]].insert(fin[3], element1)
    s[fin[4]].insert(fin[5], element2)
    c = c + fin[6]
    # print(s)
    # print(c)
    return double_insertion((s,c), req_edges, info, dis_map)


def swap(solution, req_edges, info, dis_map):
    # print('swap begin')
    s = copy.deepcopy(solution[0])
    c = solution[1]
    fin = (None, None, None, None, 0)  # remove route num, remove task num, insert route num, insert task num, cos_var
    len_s = len(solution[0])
    for i in range(len_s):
        temp1 = cal_cost(s[i], req_edges, dis_map)
        for j in range(len(s[i])):
            for k in range(len_s):
                temp3 = cal_cost(s[k], req_edges, dis_map)
                for l in range(len(s[k])):
                    if i == k and j == l:
                        continue
                    element1 = s[i][j]
                    element2 = s[k][l]
                    s[i][j] = element2
                    s[k][l] = element1

                    temp2 = cal_cost(s[i], req_edges, dis_map)
                    temp4 = cal_cost(s[k], req_edges, dis_map)
                    if temp4 > info['capacity'] or temp2 > info['capacity']:
                        s = copy.deepcopy(solution[0])
                        break
                    delta = abs(temp4 + temp2 - temp3 - temp1)
                    if delta < fin[4]:
                        fin = (i, j, k, l, delta)
                    s = copy.deepcopy(solution[0])
    # print(fin)
    if fin == (None, None, None, None, 0):
        # print('best of swap is', solution[1])
        # print(solution[0])
        return solution
    element1 = s[fin[0]][fin[1]]
    element2 = s[fin[2]][fin[3]]
    # print('elements are ', element1, element2)
    s[fin[0]][fin[1]] = element2
    s[fin[2]][fin[3]] = element1
    c = c + fin[4]
    # print(s)
    # print(c)
    return swap((s,c), req_edges, info, dis_map)


def cal_cost(r, req_edges, dis_map):
    route_cost = 0
    position = 1
    for task in r:
        route_cost += dis_map[position][task[0]]
        route_cost += req_edges[task][0]
        position = task[1]
    route_cost += dis_map[position][1]
    # print('route_cost',route_cost)
    return route_cost


def local_search(solution, req_edges, info, dis_map):
    best_r = None
    best_c = float('inf')
    for i in [single_insertion(solution, req_edges, info, dis_map),
              # double_insertion(solution, req_edges, info, dis_map),
              swap(solution, req_edges, info, dis_map)]:
        r, c = i
        if c < best_c:
            best_r = r
    if best_r is None or best_c == float('inf'):
        return solution
    else:
        return best_r, best_c

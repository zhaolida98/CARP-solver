from PathScanning import *
from local_search import *
import random, time, math, copy, signal


def get_dif_random(a, range):
    '''
    获取一个不同于a的随机数
    :param a:
    :param range:
    :return:
    '''
    b = random.randint(0, range)
    if b == a:
        return get_dif_random(a, range)
    else:
        return b


def is_same_solution(s1, s2):
    '''
    判断solution1和solution2是不是一个解
    :param s1: solution1（routes， cost）
    :param s2: solution2
    :return: True or False
    '''
    same = True
    if s1[1] != s2[1]:
        return False
    else:
        for i in s1[0]:
            for j in s2[0]:
                if i != j:
                    same = False
                else:
                    same = True
                    break
            if not same:
                break
        return same


def contains(s, pop):
    '''
    判断一个solution是否存在于population中
    :param s: solution
    :param pop:
    :return:
    '''
    contain = False
    for i in pop:
        contain = is_same_solution(i, s)
        if contain:
            break
    return contain


def generate_set(list):
    s = set()
    for i in list:
        s.add(str(i))
    return s


def combine(r_11, r_22):
    '''
    combine the segment and remove the redundant elements
    :param r_11:
    :param r_22:
    :return:
    '''
    for e in r_11:
        if r_22.__contains__(e):
            r_22.remove(e)
        elif r_22.__contains__(invert(e)):
            r_22.remove(invert(e))
    return r_11 + r_22


def time_out(begin, limit, unit_time):
    now = time.time()
    if now - begin > limit - unit_time:
        return True
    else:
        return False


def cal_load(r, req_edges, dis_map):
    load = 0
    for i in r:
        load += req_edges[i][1]
    return load


def crossover(pop_t, info, req_edges, dis_map):
    '''
    在pop_t中选取两个随机解中的两个随机路径进行随机拆分。然后错位拼接
    再经过一系列去重，补漏
    :param pop_t: > 每个解 = routes， cost
    :return: （s_x, cost of s_x)
    '''
    s_x = None
    s_num1 = random.randint(0, len(pop_t) - 1)
    s_num2 = get_dif_random(s_num1, len(pop_t) - 1)
    r_num1, r_num2 = random.randint(0, len(pop_t[s_num1][0]) - 1), random.randint(0, len(pop_t[s_num2][0]) - 1)
    r1, r2 = pop_t[s_num1][0][r_num1], pop_t[s_num2][0][r_num2]
    # split_p1 = random.randint(math.floor(0.25*len(r1)), math.ceil(0.75*len(r1)) - 1)
    split_p1 = random.randint(0, len(r1)-1)
    # split_p2 = random.randint(math.floor(0.25*len(r2)), math.ceil(0.75*len(r2)) - 1)
    split_p2 = random.randint(0, len(r2) - 1)
    r_11, r_12 = r1[:split_p1], r1[split_p1:]
    r_21, r_22 = r2[:split_p2], r2[split_p2:]
    s_get, s_lost = None, None
    set_12 = generate_set(r_12)
    set_22 = generate_set(r_22)
    r_new = combine(r_11, r_22)
    if cal_load(r_new, req_edges, dis_map) <= info['capacity']:
        s_x = copy.deepcopy(pop_t[s_num1][0])
        s_x[r_num1] = copy.deepcopy(r_new)
        s_get = set_22.difference(set_12)
        s_lost = set_12.difference(set_22)
        # delete step
        for edge in s_get:
            edge = edge[1:len(edge) - 1].split(', ')
            edge = (int(edge[0]), int(edge[1]))
            for indx in range(len(s_x)):
                if indx == r_num1:
                    continue
                if s_x[indx].__contains__(edge):
                    s_x[indx].remove(edge)
                    break
                elif s_x[indx].__contains__(invert(edge)):
                    s_x[indx].remove(invert(edge))
                    break
    else:
        r_new = combine(r_21, r_12)
        # s_x 现在只是解的部分
        s_x = copy.deepcopy(pop_t[s_num2][0])
        s_x[r_num2] = copy.deepcopy(r_new)
        s_get = set_12.difference(set_22)
        s_lost = set_22.difference(set_12)
        # delete step
        for edge in s_get:
            edge = edge[1:len(edge) - 1].split(', ')
            edge = (int(edge[0]), int(edge[1]))
            for indx in range(len(s_x)):
                if indx == r_num2:
                    continue
                if s_x[indx].__contains__(edge):
                    s_x[indx].remove(edge)
                    break
                elif s_x[indx].__contains__(invert(edge)):
                    s_x[indx].remove(invert(edge))
                    break


    # adding step
    load_table = []
    cost_table = []
    for r in s_x:
        cost_table.append(cal_cost(r, req_edges, dis_map))
        load_table.append(cal_load(r, req_edges, dis_map))

    for edge in s_lost:
        record = (None, None, float('inf'))
        edge = edge[1:len(edge) - 1].split(', ')
        edge = (int(edge[0]), int(edge[1]))
        demand = req_edges[edge][1]
        for indx in range(len(s_x)):
            if load_table[indx] + req_edges[edge][1] > info['capacity']:
                continue
            for i in range(len(s_x[indx])+1):
                temp_route = copy.deepcopy(s_x[indx])
                temp_route.insert(i, edge)
                new_cost = cal_cost(temp_route, req_edges, dis_map)
                new_load2 = cal_load(temp_route, req_edges, dis_map)
                new_load = load_table[indx] + req_edges[edge][1]
                if new_load <= info['capacity'] and new_cost < record[2]:
                    record = (indx, i, new_cost)
        if record == (None, None, float('inf')):
            return None
        s_x[record[0]].insert(record[1], edge)
        cost_table[record[0]] = record[2]
        load_table[record[0]] = load_table[record[0]] + req_edges[edge][1]

    # 计算总cost
    total_cost = 0
    for c in cost_table:
        total_cost += c
    # print('total_cost for this cross is',total_cost)
    return s_x, total_cost


def MAENS(info, req_edges, dis_map, psize, opsize, ubtrial, p_ls, begin_time, time_limit):
    best_r, best_c = None, float('inf')
    # initial
    pop = []
    while len(pop) < psize:
        ntrial = 0
        temp_contain = True
        temp_solution, temp_cost = None, 0
        while True:
            s, c = generate_solution(req_edges, info, dis_map, 6)
            ntrial += 1
            temp_contain = contains((s, c),pop)
            if not temp_contain or ntrial == ubtrial:
                temp_solution, temp_cost = s,c
                break
        if temp_contain:
            break
        pop.append((temp_solution, temp_cost))
        if temp_cost < best_c:
            best_r, best_c = temp_solution, temp_cost
    print('initial part finished')
    print('best in this stage', best_c)
    # to_format(best_r,best_c)
    # Main Loop
    psize = len(pop)
    while True:
        time1 = time.time() # 用来测量单个循环的时间
        pop_t = copy.deepcopy(pop)
        for i in range(opsize):
            # 交叉互换
            s_x = crossover(pop_t, info, req_edges, dis_map)
            if s_x is None:
                continue
            elif not contains(s_x, pop_t):
                if s_x[1] < best_c:
                    best_r = s_x[0]
                    best_c = s_x[1]
                pop_t.append(s_x)
            else:
                continue
            # print('crossover finished')
            if time.time() - begin_time > time_limit - 3:
                print('time is up1', time.time() - begin_time)
                to_format(best_r, best_c)
                exit(0)
            # 确定是否将交叉结果进一步优化
            thresh = int(1.05 * best_c)
            r = random.random()
            if s_x[1] <= thresh:
                s_ls = local_search(s_x, req_edges, info, dis_map)
                if s_ls[1] < best_c:
                    best_r, best_c = s_ls[0], s_ls[1]
                # print('local search finished')
                # print('best in this stage', best_c)
                # print(best_r)
                if not contains(s_ls, pop_t):
                    pop_t.append(s_ls)
                elif not contains(s_x, pop_t):
                    pop_t.append(s_x)
            elif not contains(s_x, pop_t):
                pop_t.append(s_x)

        # print('almost finished')
        pop_t = sorted(pop_t, key=lambda s: s[1])
        pop = pop_t[:psize]
        unit_time = time.time() - time1
        if time_out(begin_time, time_limit, unit_time):
            print('time is up2', time.time() - begin_time)
            to_format(best_r, best_c)
            exit(0)
            break
    return pop[0][0], pop[0][1]


if __name__ == '__main__':
    # random.seed(10)
    t = time.time()
    filename = 'C:\FILES and WORKS\学习\大三上\AI\AILAB\CARP\CARPResource\Proj2_Carp\CARP_samples\\val4A.dat'  # egl-e1-A egl-s1-A val4A val7A
    info, req_edges, dis_map = get_information(filename)
    print(info)
    print(req_edges)
    print("time for floyd", time.time() - t)

    psize = 30
    ubtrial = 50
    opsize = 6*psize
    p_ls = 0.2
    begin_time = time.time()
    time_limit = 20
    r, c = MAENS(info, req_edges, dis_map, psize, opsize, ubtrial, p_ls, begin_time, time_limit)
    to_format(r, c)
    print('time for MAENS',time.time() - t)
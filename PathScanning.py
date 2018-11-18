from Floyd import get_information
from local_search import *
import random, copy, time

def invert(x):
    return (x[1], x[0])


def to_format(R, cost):
    output = ''
    output += 's '
    for road in R:
        output += '0,'
        for i in road:
            output += '(%d,%d),'%(i[0],i[1])
        output += '0,'
    output = output.strip(',')
    print(output)
    print('q',int(cost))


def fullable(info, req_edges):
    total_require = 0
    for i in req_edges:
        total_require += req_edges[i][1]
    if total_require < info['vehicles'] * info['capacity'] * 2:
        return True
    else:
        return False


def max_depot(edge, choice_edge, dis_map):
    '''
    strategy 1
    maximize the distance from current edge to the depot
    :param edge:
    :param choice_edge:
    :param load:
    :param capacity:
    :param dis_map:
    :return:
    '''
    head = 1
    if dis_map[edge[head]][1] > dis_map[choice_edge[head]][1]:
        return True
    elif dis_map[edge[head]][1] < dis_map[choice_edge[head]][1]:
        return False
    else:
        return random_choose()


def min_depot(edge, choice_edge, dis_map):
    '''
    strategy 2
    minimize the distance from current edge to the depot
    :param edge:
    :param choice_edge:
    :param load:
    :param capacity:
    :param dis_map:
    :return:
    '''
    head = 1
    if dis_map[edge[head]][1] < dis_map[choice_edge[head]][1]:
        return True
    elif dis_map[edge[head]][1] > dis_map[choice_edge[head]][1]:
        return False
    else:
        return random_choose()


def max_ds(edge, choice_edge, req_edges):
    '''
    strategy 3
    maximize the (demand / serve) cost
    :param edge:
    :param choice_edge:
    :return:
    '''
    edge_ds = req_edges[edge][1] / req_edges[edge][0]
    choice_edge_ds = req_edges[choice_edge][1] / req_edges[choice_edge][0]
    if edge_ds > choice_edge_ds:
        return True
    elif edge_ds < choice_edge_ds:
        return False
    else:
        return random_choose()


def min_ds(edge, choice_edge, req_edges):
    '''
    strategy 4
    minimize the (demand / serve) cost
    :param edge:
    :param choice_edge:
    :return:
    '''
    edge_ds = req_edges[edge][1] / req_edges[edge][0]
    choice_edge_ds = req_edges[choice_edge][1] / req_edges[choice_edge][0]
    if edge_ds < choice_edge_ds:
        return True
    elif edge_ds > choice_edge_ds:
        return False
    else:
        return random_choose()


def HFLC(edge, choice_edge, load, capacity, dis_map):
    '''
    stratege 5
    hight far low close
    :return:
    '''
    rate = 0.5
    head = 1
    if load < rate * capacity:
        if dis_map[edge[head]][1] > dis_map[choice_edge[head]][1]:
            return True
        else:
            return False
    if load >= rate * capacity:
        if dis_map[edge[head]][1] < dis_map[choice_edge[head]][1]:
            return True
        else:
            return False


def random_choose():
    '''
    strategy 6
    randomly choose an edge
    :return:
    '''
    a = random.random()
    if a < 0.5:
        return True
    elif a > 0.5:
        return False
    else:
        random_choose()


def path_scanning(requier_edges, info, dis_map, strategynum=6):
    '''

    :param requier_edges: all the edges has 'demand'
    :param info: basic information provided by the question
    :param dis_map: distance map
    :param strategynum: determine which strategy to use
    :return:
    '''
    req_edges = requier_edges.copy()
    b_full = fullable(info, req_edges)
    R = []
    capacity = info['capacity']
    total_cost = 0
    rate = 0.91*capacity
    while req_edges:
        load = 0
        cost = 0
        i = 1
        road = []
        while True:
            distance = float('inf')
            choice_edge = None
            for edge in req_edges:
                if req_edges[edge][1] + load <= capacity:
                    temp_distance = dis_map[i][edge[0]]
                    if load > rate and b_full:
                        back_dis = dis_map[i][1]
                        finish_back_dis = dis_map[edge[1]][1]
                        s_cost = req_edges[edge][1]
                        if temp_distance + s_cost + finish_back_dis > back_dis:
                            continue
                    if temp_distance < distance:
                        distance = temp_distance
                        choice_edge = edge
                    elif temp_distance == distance:
                        operator = False
                        if strategynum == 1:
                            operator = max_depot(edge, choice_edge, dis_map)
                        elif strategynum == 2:
                            operator = min_depot(edge, choice_edge, dis_map)
                        elif strategynum == 3:
                            operator = max_ds(edge, choice_edge, req_edges)
                        elif strategynum == 4:
                            operator = min_ds(edge, choice_edge, req_edges)
                        elif strategynum == 5:
                            operator = HFLC(edge, choice_edge, load, capacity, dis_map)
                        elif strategynum == 6:
                            operator = random_choose()
                        if operator:
                            choice_edge = edge
            if choice_edge is None:
                break
            if i != 1 and choice_edge[0] != 1 and dis_map[i][choice_edge[0]] == dis_map[i][1] + dis_map[1][choice_edge[0]]:
                # print('find')
                break
            road.append(choice_edge)
            # print(choice_edge)
            load += req_edges[choice_edge][1]
            cost += distance + req_edges[choice_edge][0]
            i = choice_edge[1]
            req_edges.pop(choice_edge)
            req_edges.pop(invert(choice_edge))
            if (not req_edges) or (distance == float('inf')):
                break
        cost += dis_map[i][1]
        R.append(road)
        total_cost += cost
        if not req_edges:
            break
    return R, total_cost


def generate_solution(req_edges, info, dis_map, strategy):
    bestR = None
    bestC = float('inf')
    for i in range(500):
        R, cost = path_scanning(req_edges, info, dis_map, strategynum=strategy)
        if cost < bestC:
            bestC = cost
            bestR = R
    # print(strategy)
    # to_format(bestR, bestC)
    # print()
    return bestR, bestC


if __name__ == '__main__':
    # random.seed(10)
    t = time.time()
    filename = 'C:\FILES and WORKS\学习\大三上\AI\AILAB\CARP\CARPResource\Proj2_Carp\CARP_samples\\val1A.dat'  # egl-s1-A gdb10 val7A
    info, req_edges, dis_map = get_information(filename)
    print(info)
    print(req_edges)
    print("time for floyd",time.time() - t)


    # print(dis_map)
    t = time.time()
    print('\r\nbefore si')
    r, c = generate_solution(req_edges, info, dis_map, 6)
    print(r,c)
    to_format(r,c)
    print("time of path scanning:",time.time() - t)

    # t = time.time()
    # print('\r\nafter local search')
    # r1, c1 = local_search((r,c), req_edges, info, dis_map)
    # to_format(r1, c1)
    # print('time of local search', time.time() - t)

    t = time.time()
    print('\r\nafter local search')
    r1, c1 = single_insertion((r,c), req_edges, info, dis_map)
    to_format(r1, c1)
    print('time of local search', time.time() - t)
import sys, random, time
from MAENS import *
from PathScanning import *
if __name__ == '__main__':
    filename = sys.argv[1]
    time_limit = int(sys.argv[3]) - 3
    print(time_limit)
    seed = int(sys.argv[5])
    random.seed(seed)
    psize = 30
    ubtrial = 50
    opsize = 6 * psize
    p_ls = 0.2

    t = time.time()
    info, req_edges, dis_map = get_information(filename)
    print(info)
    # print(req_edges)
    print("time for floyd", time.time() - t)

    begin_time = time.time()
    r, c = MAENS(info, req_edges, dis_map, psize, opsize, ubtrial, p_ls, begin_time, time_limit)
    to_format(r, c)
    print('time for MAENS', time.time() - t)
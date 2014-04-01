import sys
import math
    

### === READ INPUT  === ###
# first 4 readline instances are for l, h, s, n
#
# info: list of tuples (x_i, t_i)
### only want attached nodes in neighbours, so don't populate while read
# neighbours: dictionary, where
#     value: int, x_i,
#     key  : list, first index is t_i
#                  remaining indeces are neighbours (x_j) of this node
### =================== ###

count = 0
info = [(0, 0)]
info2 = [(0, 0)]
neighbours = {}
neighbours[(0, 0)] = [0]

fname = sys.argv[1]
with open(fname) as f:
    for line in f:
        if line[0] != "#":
            if count == 0:
                l = int(line.strip())

            elif count == 1:
                h = int(line.strip())

            elif count == 2:
                s = int(line.strip())

            elif count == 3:
                n = int(line.strip())

            else: # info
                nums = line.strip().split() # list of strings
                x = int(nums[0])
                t = int(nums[1])
                info.append((x, t))
                info2.append((x, t))
                neighbours[(x, t)] = [0]

            count += 1

def get_next(info):
    """
    Given the list of (position, time) tuples,
    returns the position of the minimum time.
    """
    p = -1
    t = float('inf')
    for i in range(len(info)):
        if info[i][1] < t:
            p = i
            t = info[i][1]
    return p


### === BUILD GRAPH === ###
# for all nodes with bigger t than cur_node,
#     make edge only if tot_time >= (physical difference)/s
#     all weights = -1
#
# tot_time = (neigh[time] - cur[time]) + h - (cur[time])
#          = neigh[time] + h - 2*cur[time]
#
# first value of values in neighbours: min weight to get there
### =================== ###

# from source: one time thing!
first = True

while info != []:
    cur = get_next(info)
    # TODO: what to do if cur == -1?
    # for all nodes that's not this one
    for i in range(len(info)):
        if i != cur:

            tot_time = info[i][1] - info[cur][1]
            x_diff   = (float(info[i][0] - info[cur][0])) / float(s)

            # from source
            if (info[cur][0] == 0) & (info[cur][1] == 0) & (first == True):
                tot_time += h

            # if we can reach the neighbour node in time
            if tot_time >= x_diff:
                neighbours[info[cur]].append(info[i])

    if (info[cur][0] == 0) & (info[cur][1] == 0):
        first = False
    del info[cur]

print (neighbours)


### === pruning graph === ###
# start with neighbours
# start with source
# for each neighbour neigh of source,


# given a node, 
# remove all of its neighbours from info2 if they exist
# call exists on each neighbour

def exists(info2, neighbours, node):
    """
    Given a list info2, a dictionary neighbours, and a node,
    removes itself from info2, and
    calls exists on all its neighbours.
    Ultimate result is info2 having nodes that are not reachable.
    """
    if node in info2:
        ind = info2.index(node)
        del info2[ind]
    for neigh in neighbours[node][1:]:
       exists(info2, neighbours, neigh)
    return None


# call exists here, starting with source
exists(info2, neighbours, (0, 0))

print (info2)


# prune neighbours here: remove any nodes that are in info2
for extra in info2:
    del neighbours[extra]

print (neighbours)

# check each node cur:
# if cur has no neighbours, return 0
# else, for each neighbour of this node,
#     result = check neighbour
#     if result == 0 and neighbour is still in info2,
#         remove neighbour from info2
### ======================###


### === BELLMAN-FORD === ###
### ==================== ###
items = 0
# current node's number of neighbours:
# if it has no neighbours, then 
# for each cur's neighbours, if all of them return -1, 
num_n = 0 # number of neighbours of current node
num_k = 0

for i in range(1, n):
    # for each reachable key in neighbours, check each of its neighbours
    for key in neighbours:
        for neigh in neighbours[key][1:]:
            old = neighbours[neigh][0]
            new = neighbours[key][0] - 1

            if new < old:
                neighbours[neigh][0] = new

                # keep track of how many items caught so far
                if new < items:
                    items = new

            # this node does have neighbours!
            num_n = 1

print (-items)

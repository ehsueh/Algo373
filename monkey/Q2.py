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
neighbours[0] = [0]

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
                neighbours[x] = [0]

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
                neighbours[info[cur][0]].append(info[i][0])

    if (info[cur][0] == 0) & (info[cur][1] == 0):
        first = False
    del info[cur]


### === BELLMAN-FORD === ###
### ==================== ###
items = 0


for i in range(1, n):
    # for each key in neighbours, check each neighbour
    for key in neighbours:
        for neigh in neighbours[key][1:]:
             old = neighbours[neigh][0]
             new = neighbours[key][0] - 1

             if new < old:
                 neighbours[neigh][0] = new

                 # keep track of how many items caught so far
                 if new < items:
                     items = new

print (-items)

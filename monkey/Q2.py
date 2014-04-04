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

# TODO: monkey can drop >1 thing at same time, same place
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
                
                # if more than one item is dropped at the same time and place
                if (x, t) in info:
                    neighbours[(x, t)][0] -= 1
                    
                else:
                    info.append((x, t))
                    info2.append((x, t))
                    neighbours[(x, t)] = [0]

            count += 1

def get_next(info):
    """
    Given the list of (position, time) tuples,
    returns the tuple of the smallest time.
    """

    t = float('inf')
    for i in range(len(info)):
        if info[i][1] < t:
            t = info[i][1]
            s = info[i]
    return s


### build graph ver. 2 ###
# keep track of which nodes we've visited ==> delete from info
# 
# start at (0, 0), and check all of the remaining nodes in info;
# insert into its neighbours only if reachable
# remove (0, 0) from info
# 
# repeat above each neighbour:
# check remaining nodes in info;
# insert into its neighbours only if reachable
# remove node from info

# from source: one time thing!
first = True

def populate(info, neighbours, node):
    """
    Given a list info, a dictionary neighbours, and a node,
    for all other nodes in info
    insert into node's neighbours list only if reachable
    remove node from info
    
    Checks and populates recursively all of node's neighbours list
    """
    global first
    cur = info.index(node)
    
    for i in range(len(info)):
        # for all nodes other than this one
        if i != cur:

            tot_time = info[i][1] - info[cur][1]
            x_diff   = (float(info[i][0] - info[cur][0])) / float(s)

            # from source
            if (info[cur] == (0, 0)) & (first == True):
                tot_time += h
                
            # if we can reach the neighbour node in time
            if tot_time >= x_diff:
                neighbours[info[cur]].append(info[i])  

    if (info[cur] == (0, 0)):
        first = False
        
    # remove this node from info, and populate its neighbours
    del info[cur]
    neighbours[node][1:] = sorted(neighbours[node][1:], key=lambda x: x[1])
    for neigh in neighbours[node][1:]:
        if neigh in info:
            populate(info, neighbours, neigh)
        
    return


populate(info, neighbours, (0, 0))
### ================== ###


### === BELLMAN-FORD === ###
### ==================== ###
items = neighbours[(0, 0)][0]

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


print (-items)

import sys
import math

def reachable(a, b, x, c, d, y):
    """
    Returns true if node at (a, b) with radius x
    can reach node at (c, d) with radius y.
    Returns false otherwise.
    """
    i = math.pow((a - c), 2)
    j = math.pow((b - d), 2)
    dist = math.sqrt(i+j)
    return (dist - x <= y)


###  Read input from file,
#    initialize variables:
#    info: list of tuples of (x_i, y_i, r_i)
#    neighbours: dictionary, where
#        value: int, index of agent
#        key: list, first index is dist from source
#                   remaining indices are neighbours of this agent
####

info = []
neighbours = {}
nodes = 0

fname = sys.argv[1]
with open(fname) as f:
    for line in f:
        # read only if the line doesn't start with #
        if line[0] != "#":
            try:
                n
            except NameError: # we're at the first line
                n = int(line.strip())
            else: # we're past the first line
                cur = line.strip().split(" ")
                info.append((float(cur[0]), float(cur[1]), float(cur[2])))
                # distance from source node; initialized to infinity
                neighbours[nodes] = [float('inf')]
                nodes += 1
            
# no hops from source to itself
neighbours[0][0] = 0


# BBBB ==== building graph ==== BBBB
#for each agent a_i in info,
    #for each key a_e in neighbour that's not itself,
    #if a_i can reach a_e
        #add a_i to value list of a_e
        
# populate neighbours
for nodes in range(n): # index
    for agent in neighbours: # use as index in info
        if nodes != agent:
            old = info[nodes]
            new = info[agent]
            if reachable(new[0], new[1], new[2], old[0], old[1], old[2]):
                neighbours[nodes].append(agent)
        

# BBBB ==== building graph ==== BBBB
### edges between each key in neighbours and each entry in its value list
### edges are all weight 1
# we don't need the 'previous' array; it's inefficient anyway
# we just need the dist; dist of a neighbour = current dist + 1


# CCCC ==== dijkstra's ==== CCCC
def min_dist(avail, agents):
    """
    Given a dictionary of agents, and all non-visited info, avail,
    returns the index of agent with smallest distance.
    """
    small = float('inf')
    ind = -1;
    for i in range(len(avail)):
        if agents[avail[i]][0] < small:
            ind = i
            small = agents[i][0]
    return ind


avail = list(range(n))
# Dijkstra's algorithm
while avail != []:
    # get neighbour 
    small = min_dist(avail, neighbours)
    if small == -1: # no more accessible vertices! D:
        break
    
    cur = avail[small]
    # distance from source through this node
    new_dist = neighbours[cur][0] + 1
    for neigh in neighbours[cur][1:]: # all neighbours of this node
        if new_dist < neighbours[neigh][0]: # relax
            neighbours[neigh][0] = new_dist
        
    del avail[small]

# process and return
for i in range(n):
    if neighbours[i][0] == float('inf'):
        print (0)
    else:
        print (neighbours[i][0])
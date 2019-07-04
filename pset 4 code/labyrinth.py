import queue
class Labyrinth(object):
    def __init__(self, rooms, corridors, filters, start, goal):
        # rooms is a list of the names of the rooms. Each name is a (short) string.
        # For convenience, we won't give you any room names containing numbers.
        self.rooms = rooms  
        # corridors is a list of tuples (room1, room2, type).
        # type is an integer between 0 and 3 (inclusive).
        # All corridors are bidirectional (i.e. can be traversed in either direction).
        # An explorer cannot traverse a corridor of a certain type without possessing the corresponding filter.
        self.corridors = corridors
        # filters gives the initial locations of the filters as a list of tuples (room, type).
        # There may be multiple filters in a room, but there is only one filter of each type.
        # Each explorer may carry any number of filters on his person.
        self.filters = filters
        # start is the name of the room in which the explorer starts.
        self.start = start
        # goal is the name of the (single) room in which the treasure is located.
        self.goal = goal


# This method should return the minimum number of timesteps required to reach the goal room.
# If it is not possible to reach the goal room, return None.
# As stated in the problem set, at the beginning of each timestep, the explorer may pick up any filter 
# located in the same room, and then traverse at most one corridor (provided he possesses the proper filter).
def explore_single(labyrinth):
    # adjacency list
    adj = {}
    # filters at each vertex
    fil = {}
    state = {}
    level = {}
    frontier = queue.Queue()
    time = 0
    collected = [False,False,False,False]
    degree = {}
    print ()
    for v in labyrinth.rooms:
        adj.update({v:[]})
        level.update({v:-1})
        state.update({v:[False,False,False,False]})
        degree.update({v:0})
        fil.update({v:[False,False,False,False]})
    for (v,f) in labyrinth.filters:
        fil[v][f] = True
    for u,v,f in labyrinth.corridors:
        adj[u].append((v,f))
        adj[v].append((u,f))
    collected = fil[labyrinth.start]
    state[labyrinth.start] = collected.copy()
    frontier.put(labyrinth.start)
    level[labyrinth.start] = 0
    while not frontier.empty():
        u = frontier.get()
        if level[u] > 20:
            return None
        print ('u = ',u, state[u], level[u])
        if u is labyrinth.goal:
 #           print ('time = ', time)
            return level[u]
        time +=1
        for f in range (0,4):
            if state[u][f] and (labyrinth.goal,f) in adj[u]:
                frontier.put(labyrinth.goal)
        for v,f in adj[u]:
           # print (v)
            #if state[u][f] and degree[v] >= 0:
 #          print (v, state[u][f], state[v]!= state[u])
           if state[u][f] and state[v] != state[u]:
#                a = collected.copy()
#                if degree[u] == 1:
#                    degree[u] -= 1
                for i in range(0,4):
                    if fil[v][i] and not state[u][i]:
                        state[u][i] = True
                if adj[v]!= []:
                    frontier.put(v)
                    level[v] = level[u]+1
                    
                state[v] = state[u].copy()
 #               adj[u].remove((v,f))
                
    return None


# This method should return the minimum number of explorers (working simultaneously) required (for any explorer)
# to reach the goal room within the given timelimit. If no group of explorers is big enough, return None.
def explore_multiple(labyrinth, timelimit):
    time = explore_single(labyrinth)
    if time == None or time > 4*timelimit:
        return None
    elif time <= timelimit:
        return 1
    else:
        return 2
    #raise NotImplementedError()
    

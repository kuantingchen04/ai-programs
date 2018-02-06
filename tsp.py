from quicksort.quicksort import quicksort
from utils import Stack, Queue, PriorityQueue, cal_path_cost, Node
import math

def heuristic(coords,v,w):
    (x1, y1, z1) = coords[v]
    (x2, y2, z2) = coords[w]
    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2 )

def goal_test(problem, node, visited_set = None):
    if problem['domain'] == 'route':
        return node.value == problem['goal']
    elif problem['domain'] == 'tsp':
        if node.value != problem['goal']:
            return False
        path = node.get_path()
        print "goal test", path
        visited_set = set(path)
        if len(visited_set) == len(problem['graph'].get_nodes()):
            return True

def queue_check(problem,child_value,frontier,closed_set):
    if problem['domain'] == 'route':
        return child_value not in closed_set and child_value not in frontier
    elif problem['domain'] == 'tsp':
        pass

def graph_search(problem):
    """Problem: {graph:, coords:, start:, goal:}
    method: B, D, I, U, A
    """
    method = problem['method']

    if method not in ['B', 'D', 'I', 'U', 'A']:
        print ("Enter Correct method!")
        return None
    if problem['start'] not in problem['graph'].get_nodes() or problem['goal'] not in problem['graph'].get_nodes():
        print("Enter Correct Start/Goal!")
        return None


    # BFS, DFS
    if method in ['B','D']:
        if method == 'B':
            frontier = Queue()
        else:
            frontier = Stack()
        frontier.push( Node(problem['start']) )
        closed_set = set()
        i = 0
        while not frontier.isEmpty():
            node = frontier.pop()
            print "node:",node
            if goal_test(problem, node):
                # path = [ x.value for x in node.get_path() ]
                path = node.get_path()
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count

            # Expansion
            closed_set.add(node.value)
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                # if child_value not in closed_set and child_value not in frontier: # dont allow duplicates in frontier
                # if child_value not in closed_set: # route
                # if queue_check(problem,child_value,frontier,closed_set):
                if not node.parent or (node.parent and child_value != node.parent.value): # tsp
                    child = Node(child_value, node)
                    frontier.push(child)
                    print "push", child
            print frontier
            print("------------------------------")
            # if i == 5:
            #     break
            i += 1

        return None

    # UCS, Astar
    if method in ['U','A']:
        frontier = PriorityQueue()
        priority = 0 if method == 'U' else heuristic(problem['coords'],problem['goal'],problem['start'])
        frontier.push(priority, Node(problem['start']))

        closed_set = set()
        cost = dict()
        cost[problem['start']] = 0

        while not frontier.isEmpty():
            node = frontier.pop()
            print "node:", node
            if goal_test(problem, node):
                path = node.get_path()
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count
            # Expansion
            closed_set.add(node)
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                new_cost = cost[node.value] + problem['graph'].get_cost(node.value,child_value) # g_n

                # if child_value not in cost or new_cost < cost[child_value]:
                if not node.parent or (node.parent and child_value != node.parent.value):
                    # del frontier[child_value] # if key with lower priority is in frontier, delete it first
                    cost[child_value] = new_cost
                    priority = new_cost if method == 'U' else new_cost + heuristic(problem['coords'],problem['goal'],child)
                    child = Node(child_value, node)
                    frontier.push(priority,child)
                    print "push", child
            print frontier
            print("------------------------------")
        return None

    # IDS
    if method == 'I':
        def depth_limited(problem, limit):
            frontier = Stack()
            frontier.push(Node(problem['start']))
            closed_set = set()
            while not frontier.isEmpty():
                node = frontier.pop()
                print "node:", node
                if goal_test(problem, node):
                    path = node.get_path()
                    cost = cal_path_cost(problem['graph'], path)
                    return path, cost, frontier.count

                if node.depth == limit:
                    # print "reach", frontier.count
                    pass
                else:
                    # Expansion
                    closed_set.add(node.value)
                    adj = problem['graph'].adj(node.value)
                    for child_value in quicksort(adj):
                        # if child_value not in closed_set:  # dont allow duplicates in frontier
                        if not node.parent or (node.parent and child_value != node.parent.value):  # tsp: start or others
                            child = Node(child_value, node)
                            frontier.push(child)
                            print "push", child
                print("------------------------------")
            return None
        max_depth = 15
        for i in range(max_depth):
            result = depth_limited(problem, i)
            if result:
                return result
import numpy as np
import itertools
import heapq
class Heap():
    def __init__(self):
        self.memory = []

    def add(self, entry):
        heapq.heappush(self.memory, entry)

    def pop(self):
        return heapq.heappop(self.memory)

    def all(self):
        return (self.memory)
    def length(self):
        return len(self.memory)


class Node():
    def __init__(self, point, parent, cost_so_far= 0, cost_to_go= 0):
        self.parent = parent
        self.state = point
        self.grid = point[1:]
        self.cost_so_far = cost_so_far
        self.cost_to_go = cost_to_go




class Solution():

    def __init__(self, l): # algo, W,H, ini, target, n_channel, channels_connector):
        self.file = open("output.txt", "w")

        self.algo = l[0]
        self.W = l[1][0]
        self.W = l[1][0]
        self.H = l[1][1]

        self.Total_counter_output = 1
        self.Total_cost_output = 0

        self.frontier = Heap()
        self.counter = itertools.count()

        self.frontier.add([0, next(self.counter),  Node(l[2], None)])



        self.target = l[3]

        self.explored = {}
        self.frontier_inid = {}
        self.goal = l[3]
        ####################### Make these based on algorthim
        if algo == 'BFS':
            self.c_r = 1
            self.c_d = 1
            self.c_j = 1
        elif algo == 'UCS' or 'A*':
            self.c_r = 10
            self.c_d = 14

        else:
            print("Fail")
            exit(0)



        self.possible_move = [[0,1],[1,0],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]

        self.n_channel = l[4][0]

        self.channels_connector = l[5:]

        self.Jumping = {}

    def jumper(self):

        for i in range(self.n_channel):
            link = [self.channels_connector[i][1] , self.channels_connector[i][2]]

            y1 = self.channels_connector[i][0:3]

            y2 = [self.channels_connector[i][-1]] + link

            self.Jumping[str(y1)] = y2
            self.Jumping[str(y2)] = y1

    def goal_test(self, node, goal):
        if np.array_equal(node.state, goal):
            return True
        return False
    def ranger(self, p):
        if 0<=p[3] <= self.W and 0<= p[-1] <= self.H:
            return True
        else:
            return False

    def expand(self, node):
        s = node.state[0]
        x = node.state[1]
        y = node.state[-1]
        c_c = node.cost_so_far

        c_est =  abs(self.target[0] - s) + 10 * np.linalg.norm(np.array([self.target[0] - x,self.target[1] - y]))  if self.algo == 'A*' else 0
        child_all = [ [self.c_r ,c_c + c_est +  self.c_r , s,x, y+ 1],[self.c_r ,c_c + c_est+ self.c_r,s, x+ 1, y],[self.c_r ,c_c +c_est+ self.c_r,s, x-1 , y],[self.c_r ,c_c + c_est+ self.c_r,s, x, y-1],[self.c_d ,c_c +  c_est + self.c_d, s,x-1, y-1],[self.c_d ,c_c + c_est + self.c_d, s, x- 1, y+ 1],[self.c_d ,c_c + c_est + self.c_d,s, x+ 1, y- 1],[self.c_d ,c_c + c_est + self.c_d, s, x+ 1, y+ 1]]
        child = filter(self.ranger, child_all)

        child = list(child)


        if str(node.state) in self.Jumping:
            jump = self.c_j if self.algo == 'BFS' else abs(self.Jumping[str(node.state)][0] -node.state[0])
            jump_1 = jump #### Cost to go to next state
            if self.algo == 'A*':
                s1 = self.Jumping[str(node.state)][0]
                x1 = self.Jumping[str(node.state)][1]
                y1 = self.Jumping[str(node.state)][2]
                jump = jump + abs(self.target[0] - s1) + 10 * np.linalg.norm(np.array([self.target[0] - x1,self.target[1] - y1]))

            child.append([jump_1, c_c + jump] + self.Jumping[str(node.state)])

        return child



    def solution(self, node):


        [self.file.write (str(i) + ' ') for i in node.state]
        self.file.write(str(node.cost_to_go) + '\n')
        print(node.state, node.cost_to_go)

        while(node.parent != None):
            self.Total_counter_output += 1
            self.Total_cost_output += node.cost_to_go

            node = node.parent
            [self.file.write(str(i) + ' ') for i in node.state]
            self.file.write(str(node.cost_to_go) + '\n')
            print(node.state,node.cost_to_go )

        self.file.write(str(self.Total_counter_output) + '\n')
        self.file.write(str(self.Total_cost_output) + '\n')
        self.file.close()


    def insert(self, child, parent):
        new_node = Node(child[2:], parent, child[1], child[0])


        self.frontier.add((child[1],next(self.counter), new_node) )
        self.frontier_inid[str(child[2:])] = [child[1], next(self.counter), new_node]


    def insert_explored(self, node):

        self.explored[str(node.state)] = node


    def run(self):
        self.jumper()
        countt = 0
        while True:
            countt += 1

            if  self.frontier.length() == 0:
                print('Fail')
                f2 = open("output.txt", 'w')
                f2.write("FAIL")
                f2.close()
                return 'FAIL'

            _, _, node = self.frontier.pop()

            if self.goal_test(node, self.goal):
                return self.solution(node)

            self.insert_explored(node)



            z = self.expand( node)
            for j in z:

                if (str(j[2:]) not in self.explored) and (str(j[2:]) not in self.frontier_inid):
                    self.insert(j, node)

                elif str(j[2:]) in self.frontier_inid:
                    temp_node_fornt = self.frontier_inid[str(j[2:])][-1]

                    path_cost_node = temp_node_fornt.cost_so_far
                    path_cost_child = j[1]
                    if path_cost_child < path_cost_node:
                        entry = self.frontier_inid.pop(str(j[2:]))
                        new_node = Node(j[2:], node, j[1],j[0])
                        entry[0:] = [j[1], next(self.counter), new_node]
                        self.frontier_inid[str(j[2:])] =  [j[1], next(self.counter), new_node]


                        heapq.heapify(self.frontier.all())


                elif str(j[2:]) in self.explored:

                    temp_node_fornt = self.explored[str(j[2:])]
                    path_cost_child = j[1]
                    path_cost_node = temp_node_fornt.cost_so_far

                    if  path_cost_child < path_cost_node:

                        del self.explored[str(j[2:])]
                        new_node = Node(j[2:], node, j[1],j[0])
                        self.frontier.add((j[1],next(self.counter), new_node) )



f = 'input.txt'
numbers = []
with open(f) as fp:
    algo = fp.readline().strip()
    numbers.append(algo)

    for line in fp:
        numbers.append([int(x) for x in line.split()])


h = Solution(numbers)

h.run()

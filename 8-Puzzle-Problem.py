# function to get the position of a block value in the puzzle
def get_position(puzzle, value):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == value:
                return (i, j)

# function to get the Manhattan distance heuristic value for a given puzzle
def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                goal_pos = get_position(goal, puzzle[i][j]) # get the position of the block in the goal state
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance


def get_neighbors(puzzle):
    neighbors = []
    # position of the empty block (0)
    zero_pos = get_position(puzzle, 0)
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_pos = (zero_pos[0] + dx, zero_pos[1] + dy) # neighboring positions of 0 value
        if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
            # create a new puzzle by swapping the empty block with the neighboring block
            new_puzzle = [row[:] for row in puzzle]
            new_puzzle[zero_pos[0]][zero_pos[1]] = puzzle[new_pos[0]][new_pos[1]]
            new_puzzle[new_pos[0]][new_pos[1]] = 0
            # add the new puzzle to the list of neighbors
            neighbors.append(new_puzzle)
    return neighbors

# Initial and goal configurations
initial = [[1, 2, 3], [7, 8, 5], [0, 6, 4]]
# initial=[]  # for taking input from user
# for i in range(3):
#     s=[]
#     for j in range(3):
#         k = int(input())
#         s.append(k)
#     initial.append(s)
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


queue = [(manhattan_distance(initial), initial)]
visited = set()
came_from = {}
cost_so_far = {str(initial): 0}  # actual cost in reaching to that configuration

while queue:
    # sort the queue by priority (f(x) value i.e., the sum of the current cost and the heuristic value)
    queue.sort()
    _, current = queue.pop(0)
    # if the current state is the goal state, break out of the loop
    if current == goal:
        break
    # mark the current state as visited
    visited.add(str(current))


    for neighbor in get_neighbors(current):
        new_cost = cost_so_far[str(current)] + 1
        if str(neighbor) not in cost_so_far or new_cost < cost_so_far[str(neighbor)]: # if we haven't seen the neighbor before, or if the new cost is lower than the previous cost
            cost_so_far[str(neighbor)] = new_cost   # update the cost and priority and add the neighbor to the queue
            priority = new_cost + manhattan_distance(neighbor)
            queue.append((priority, neighbor))
            if str(neighbor) not in visited:
                came_from[str(neighbor)] = current

# Backtrack to get the path from initial to goal
current = goal
path = [current]
while current != initial:
    current = came_from[str(current)]
    path.append(current)
path.reverse()


print("Size of explored list using sum of Manhattan distances:", len(visited))
print("Total number of steps:", len(path)-1)
for i, state in enumerate(path):
    print('\n')
    print(f"Step {i}:")
    for row in state:
        print(row)
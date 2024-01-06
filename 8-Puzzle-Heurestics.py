# function to get the number of misplaced blocks heuristic value for a given puzzle
def get_position(puzzle, value):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == value:
                return (i,j)


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


def misplaced_blocks(puzzle):
    count = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal[i][j]:
                count += 1
    return count


# function to get the Manhattan distance heuristic value for the "0" block in a given puzzle
def manhattan_distance_zero(puzzle):
    zero_pos = get_position(puzzle, 0)
    goal_pos = get_position(goal, 0)
    return abs(zero_pos[0] - goal_pos[0]) + abs(zero_pos[1] - goal_pos[1])


# Initial and goal configurations
initial = [[1, 2, 3], [7, 8, 5], [0, 6, 4]]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# A* search algorithm using the sum of Manhattan distances heuristic
queue = [(manhattan_distance(initial), initial)]
visited_sum = set()
came_from = {}
cost_so_far = {str(initial): 0}

while queue:
    queue.sort()
    _, current = queue.pop(0)
    visited_sum.add(str(current))
    if current == goal:
        break

    for neighbor in get_neighbors(current):
        new_cost = cost_so_far[str(current)] + 1
        if str(neighbor) not in cost_so_far or new_cost < cost_so_far[str(neighbor)]:
            cost_so_far[str(neighbor)] = new_cost
            priority = new_cost + manhattan_distance(neighbor)
            queue.append((priority, neighbor))
            if str(neighbor) not in visited_sum:
                came_from[str(neighbor)] = current

# A* search algorithm using the number of misplaced blocks heuristic
queue = [(misplaced_blocks(initial), initial)]
visited_misplaced = set()
came_from = {}  # dictionary for parents
cost_so_far = {str(initial): 0}

while queue:
    queue.sort()
    _, current = queue.pop(0)
    visited_misplaced.add(str(current))
    if current == goal:
        break

    for neighbor in get_neighbors(current):
        new_cost = cost_so_far[str(current)] + 1
        if str(neighbor) not in cost_so_far or new_cost < cost_so_far[str(neighbor)]:
            cost_so_far[str(neighbor)] = new_cost
            priority = new_cost + misplaced_blocks(neighbor)
            queue.append((priority, neighbor))
            if str(neighbor) not in visited_misplaced:
                came_from[str(neighbor)] = current  # parent of neighbor is current

# A* search algorithm using the Manhattan distance of the "0" block alone heuristic
queue = [(manhattan_distance_zero(initial), initial)]
visited_zero = set()
came_from = {}
cost_so_far = {str(initial): 0}

while queue:
    queue.sort()
    _, current = queue.pop(0)
    visited_zero.add(str(current))
    if current == goal:
        break

    for neighbor in get_neighbors(current):
        new_cost = cost_so_far[str(current)] + 1
        if str(neighbor) not in cost_so_far or new_cost < cost_so_far[str(neighbor)]:
            cost_so_far[str(neighbor)] = new_cost
            priority = new_cost + manhattan_distance_zero(neighbor)
            queue.append((priority, neighbor))
            if str(neighbor) not in visited_zero:
                came_from[str(neighbor)] = current

# Print the sizes of the visited lists for each heuristic
print("Size of explored list using sum of Manhattan distances:", len(visited_sum))
print("Size of explored list using number of misplaced blocks:", len(visited_misplaced))
print("Size of explored list using Manhattan distance of '0' block alone:", len(visited_zero))
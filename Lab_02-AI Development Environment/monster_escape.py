import queue  # Importing queue to implement BFS
import random  # Importing random to place player, monster, and safe zone randomly

# Function to create the grid with player, monster, and safe zone
def create_grid_with_monster(size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]  # Create an empty grid filled with spaces
    
    # Place the player at a random position
    player_x, player_y = random.randint(0, size-1), random.randint(0, size-1)
    grid[player_x][player_y] = 'P'
    
    # Place the monster at a random position, different from the player
    monster_x, monster_y = random.randint(0, size-1), random.randint(0, size-1)
    while (monster_x, monster_y) == (player_x, player_y):
        monster_x, monster_y = random.randint(0, size-1), random.randint(0, size-1)
    grid[monster_x][monster_y] = 'M'
    
    # Place the safe zone at a random position, different from both player and monster
    safe_x, safe_y = random.randint(0, size-1), random.randint(0, size-1)
    while (safe_x, safe_y) == (player_x, player_y) or (safe_x, safe_y) == (monster_x, monster_y):
        safe_x, safe_y = random.randint(0, size-1), random.randint(0, size-1)
    grid[safe_x][safe_y] = 'Z'
    
    return grid, (player_x, player_y), (monster_x, monster_y), (safe_x, safe_y)

# Function to add random obstacles to the grid
def add_obstacles(grid, num_obstacles):
    size = len(grid)
    for _ in range(num_obstacles):
        obstacle_x, obstacle_y = random.randint(0, size-1), random.randint(0, size-1)
        # Ensure obstacles are not placed on the player, monster, or safe zone
        while grid[obstacle_x][obstacle_y] in ['P', 'M', 'Z']:
            obstacle_x, obstacle_y = random.randint(0, size-1), random.randint(0, size-1)
        grid[obstacle_x][obstacle_y] = 'X'  # Place the obstacle 'X'
    return grid

# Function to check if a position is valid (within bounds and not blocked by an obstacle)
def is_valid_position(grid, x, y):
    size = len(grid)
    return 0 <= x < size and 0 <= y < size and grid[x][y] not in ['X', 'M']  # Ensure it's not blocked or occupied by monster

# BFS function for finding the shortest path
def bfs(grid, start, goal):
    size = len(grid)
    q = queue.Queue()  # Create a queue for BFS
    q.put(start)  # Start from the initial position
    visited = set()  # Set to track visited positions
    visited.add(start)  # Mark start as visited
    parent = {}  # Dictionary to store the parent of each state for path reconstruction

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible directions: up, down, left, right

    while not q.empty():
        current = q.get()  # Get the current position from the queue

        # If we reach the goal, stop the search
        if current == goal:
            break

        # Explore neighboring positions (up, down, left, right)
        for direction in directions:
            next_x = current[0] + direction[0]  # Calculate next x-coordinate
            next_y = current[1] + direction[1]  # Calculate next y-coordinate
            next_state = (next_x, next_y)  # Form the next state (position)

            # Check if the next position is valid and not already visited
            if is_valid_position(grid, next_x, next_y) and next_state not in visited:
                q.put(next_state)  # Add the valid position to the queue
                visited.add(next_state)  # Mark as visited
                parent[next_state] = current  # Track how we reached this state

    # Reconstruct the path from start to goal
    path = []
    current = goal  # Start from the goal and work backwards
    while current != start:
        path.append(current)  # Add current position to the path
        current = parent.get(current, start)  # Move to the parent of the current state
    path.append(start)  # Add the start position to the path
    path.reverse()  # Reverse the path to start from the beginning (start to goal)

    return path

# Function to print the grid with lines and the path marked
def print_grid_with_monster_and_path(grid, player_pos, monster_pos, path):
    grid_with_path = [row.copy() for row in grid]  # Copy the original grid to preserve it
    for (x, y) in path:
        if grid_with_path[x][y] not in ['P', 'M', 'Z']:  # Don't overwrite player, monster, or safe zone
            grid_with_path[x][y] = '*'  # Mark the path with '*'

    grid_with_path[player_pos[0]][player_pos[1]] = 'P'  # Mark player position
    grid_with_path[monster_pos[0]][monster_pos[1]] = 'M'  # Mark monster position

    # Print the grid with lines to separate cells clearly
    print("\nGrid with Path:")
    print('-' * (len(grid_with_path) * 4 + 1))  # Print top border line
    for row in grid_with_path:
        print('| ' + ' | '.join(row) + ' |')  # Print row with borders between cells
        print('-' * (len(grid_with_path) * 4 + 1))  # Print horizontal line after each row

# Main function to play the game
def monster_chase():
    # Ask the user for grid size and number of obstacles
    size = int(input("Enter the grid size (e.g., 6 for a 6x6 grid): "))
    num_obstacles = int(input(f"Enter the number of obstacles (less than {size * size - 3}): "))  # Ensure enough space

    # Create the grid and place the player, monster, and safe zone
    grid, player_pos, monster_pos, safe_zone = create_grid_with_monster(size)

    # Add random obstacles to the grid
    grid = add_obstacles(grid, num_obstacles)

    # Print the initial grid
    print("\nInitial Grid:")
    print_grid_with_monster_and_path(grid, player_pos, monster_pos, [])  # Empty path initially

    # Game loop
    while True:
        # Player moves toward the safe zone
        path_to_safe_zone = bfs(grid, player_pos, safe_zone)
        player_pos = path_to_safe_zone[1]  # Move player to the next step on the path

        # Check if player reached the safe zone
        if player_pos == safe_zone:
            print("\nYou reached the safe zone! You win!")
            break

        # Monster moves toward the player
        path_to_player = bfs(grid, monster_pos, player_pos)
        monster_pos = path_to_player[1]  # Move monster to the next step on the path

        # Check if monster caught the player
        if monster_pos == player_pos:
            print("\nThe monster caught you! Game over!")
            break

        # Print the updated grid with the player's and monster's positions
        print_grid_with_monster_and_path(grid, player_pos, monster_pos, path_to_safe_zone)

# Run the game
monster_chase()

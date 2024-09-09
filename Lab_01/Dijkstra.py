import heapq

def dijkstra_search(low, high):
    print("Think of a number between 1 and 100, and I (the AI) will try to guess it.")

    # Priority queue to store (cost, low, high)
    priority_queue = [(0, low, high)]
    visited = set()  # To keep track of visited ranges

    while priority_queue:
        # Get the node with the lowest cost
        cost, low, high = heapq.heappop(priority_queue)

        # Avoid revisiting the same range
        if (low, high) in visited:
            continue
        visited.add((low, high))

        # Make a guess in the current range
        guess = (low + high) // 2  # Choosing the middle of the range
        print(f"AI's guess is: {guess}")

        feedback = input("Enter 'h' if too high, 'l' if too low, or 'c' if correct: ").lower()

        if feedback == 'c':
            print(f"I (AI) guessed the number in {cost + 1} attempts!")
            return
        elif feedback == 'h':
            # Move to the left half
            if low <= guess - 1:
                heapq.heappush(priority_queue, (cost + 1, low, guess - 1))
        elif feedback == 'l':
            # Move to the right half
            if guess + 1 <= high:
                heapq.heappush(priority_queue, (cost + 1, guess + 1, high))

dijkstra_search(1, 100)
import random
from collections import deque

def bfs_game(low, high):
    attempts = 0
    # Initialize the queue with the full range of possible numbers
    queue = deque([(low, high)])  

    print("Think of a number between 1 and 100, and I (the AI) will try to guess it.")

    # Continue until the queue is empty or the correct number is guessed
    while queue:
        # Get the current range from the front of the queue
        current_low, current_high = queue.popleft()
        
        # AI makes a random guess within the current range
        guess = random.randint(current_low, current_high)
        print(f"AI's guess is: {guess}")

        # Increment the attempt counter
        attempts += 1
        
        # Get feedback from the user about the guess
        feedback = input("Enter 'h' if too high, 'l' if too low, or 'c' if correct: ").lower()

        if feedback == 'c':
            # If the guess is correct, print the number of attempts and end the game
            print(f"I (AI) guessed the number in {attempts} attempts!")
            return
        elif feedback == 'h':
            # If the guess is too high, add a new range to the queue with an updated high value
            if current_low <= guess - 1:  # Ensure the range is valid before adding to the queue
                queue.append((current_low, guess - 1))
        elif feedback == 'l':
            # If the guess is too low, add a new range to the queue with an updated low value
            if guess + 1 <= current_high:  # Ensure the range is valid before adding to the queue
                queue.append((guess + 1, current_high))
    
    # If the queue is empty and the number hasn't been guessed, this prints (though in this scenario, it shouldn't happen).
    print(queue)

# Start the guessing game by calling the function with the initial range
bfs_game(1, 100)

import random

def guess_number_dfs(min_val, max_val, tries=0):
    # AI makes a guess within the provided range
    current_guess = random.randint(min_val, max_val)
    print("Think of number between 1 and 100, and I (the AI) will try to guess it.")

    print(f"AI's guess is: {current_guess}")

    # Increment the attempt counter
    tries += 1
    # Get feedback from the user
    response = input("Enter 'h' if too high, 'l' if too low, or 'c' if correct: ").lower()

    if response == 'c':
        print(f"AI guessed the number in {tries} attempts!")
        return
    elif response == 'h':
        guess_number_dfs(min_val, current_guess - 1, tries)
    elif response == 'l':
        guess_number_dfs(current_guess + 1, max_val, tries)

# To start the guessing game, call the function:
guess_number_dfs(1, 100)

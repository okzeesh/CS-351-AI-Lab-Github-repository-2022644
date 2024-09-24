import os
import sys
import random
from copy import deepcopy

# Maximum number of rows and columns.
NMAX = 32
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Number of random words to generate
NUM_RANDOM_WORDS = 10

# Minimum and maximum lengths of generated random words
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 8

def circle_mask(grid):
    """A circular mask to shape the grid."""
    r2 = min(ncols, nrows)**2 // 4
    cx, cy = ncols // 2, nrows // 2
    for irow in range(nrows):
        for icol in range(ncols):
            if (irow - cy)**2 + (icol - cx)**2 > r2:
                grid[irow][icol] = '*'

def squares_mask(grid):
    """A mask of overlapping squares to shape the grid."""
    a = int(0.38 * min(ncols, nrows))
    cy = nrows // 2
    cx = ncols // 2
    for irow in range(nrows):
        for icol in range(ncols):
            if a <= icol < ncols-a:
                if irow < cy-a or irow > cy+a:
                    grid[irow][icol] = '*'
            if a <= irow < nrows-a:
                if icol < cx-a or icol > cx+a:
                    grid[irow][icol] = '*'

def no_mask(grid):
    """The default, no mask."""
    pass

apply_mask = {
    None: no_mask,
    'circle': circle_mask,
    'squares': squares_mask,
}

def make_grid(mask=None):
    """Make the grid and apply a mask (locations a letter cannot be placed)."""
    grid = [[' ']*ncols for _ in range(nrows)]
    apply_mask[mask](grid)
    return grid

def generate_random_word():
    """Generate a random word with length between MIN_WORD_LENGTH and MAX_WORD_LENGTH."""
    word_length = random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)
    word = ''.join(random.choice(alphabet) for _ in range(word_length))
    return word

def generate_random_wordlist():
    """Generate a list of random words."""
    return [generate_random_word() for _ in range(NUM_RANDOM_WORDS)]

def _make_wordsearch(nrows, ncols, wordlist, allow_backwards_words=True, mask=None):
    """Attempt to make a word search with the given parameters."""
    grid = make_grid(mask)
    placed_words = []  # To track placed words and their positions

    def fill_grid_randomly(grid):
        """Fill up the empty, unmasked positions with random letters."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == ' ':
                    grid[irow][icol] = random.choice(alphabet)

    def remove_mask(grid):
        """Remove the mask, for text output, by replacing with whitespace."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == '*':
                    grid[irow][icol] = ' '

    def test_candidate(irow, icol, dx, dy, word):
        """Test the candidate location (icol, irow) for word in orientation dx, dy)."""
        for j in range(len(word)):
            if grid[irow][icol] not in (' ', word[j]):
                return False
            irow += dy
            icol += dx
        return True

    def place_word(word):
        """Place word randomly in the grid and return True, if possible."""
        dxdy_choices = [(0,1), (1,0), (1,1), (1,-1)]
        random.shuffle(dxdy_choices)
        for (dx, dy) in dxdy_choices:
            if allow_backwards_words and random.choice([True, False]):
                word = word[::-1]
            n = len(word)
            colmin = 0
            colmax = ncols - n if dx else ncols - 1
            rowmin = 0 if dy >= 0 else n - 1
            rowmax = nrows - n if dy >= 0 else nrows - 1
            if colmax - colmin < 0 or rowmax - rowmin < 0:
                continue
            candidates = []
            for irow in range(rowmin, rowmax+1):
                for icol in range(colmin, colmax+1):
                    if test_candidate(irow, icol, dx, dy, word):
                        candidates.append((irow, icol))
            if not candidates:
                continue
            loc = irow, icol = random.choice(candidates)
            for j in range(n):
                grid[irow][icol] = word[j]
                irow += dy
                icol += dx
            placed_words.append((word, loc, (dx, dy)))  # Track the placed word's data
            return True
        return False

    for word in wordlist:
        word = word.replace(' ', '')
        if not place_word(word):
            return None, None

    solution = deepcopy(grid)
    fill_grid_randomly(grid)
    remove_mask(grid)
    remove_mask(solution)

    return grid, solution, placed_words

def make_wordsearch(*args, **kwargs):
    """Make a word search, attempting to fit words into the specified grid."""
    NATTEMPTS = 10
    for i in range(NATTEMPTS):
        grid, solution, placed_words = _make_wordsearch(*args, **kwargs)
        if grid:
            print('Fitted the words in {} attempt(s)'.format(i+1))
            return grid, solution, placed_words
    print('I failed to place all the words after {} attempts.'.format(NATTEMPTS))
    return None, None, None

def show_wordsearch_with_words(grid, wordlist, placed_words):
    """Display the grid and list of words along with their positions in a formatted manner."""
    # Display the wordsearch grid
    print("Word Search Grid:")
    for irow in range(nrows):
        print(' '.join(grid[irow]))

    print("\nWords to Find with Positions:")
    # Display the word list with positions
    for word, (start_row, start_col), (dx, dy) in placed_words:
        direction = 'Horizontal' if dy == 0 else ('Vertical' if dx == 0 else 'Diagonal')
        print(f"{word} starts at ({start_row+1}, {start_col+1}), Direction: {direction}")

# Automatically generate random words instead of reading from a file.
nrows, ncols = 20, 20  # You can set these values as needed
mask = None  # Optionally, set a mask ('circle', 'squares')

wordlist = generate_random_wordlist()

# This flag determines whether words can be fitted backwards into the grid
allow_backwards_words = False

grid, solution, placed_words = make_wordsearch(nrows, ncols, wordlist, allow_backwards_words, mask)

import matplotlib.pyplot as plt

def plot_wordsearch(grid, placed_words):
    """Plot the word search grid and highlight the placed words."""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Display the grid
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_xticks(range(ncols + 1))
    ax.set_yticks(range(nrows + 1))
    ax.invert_yaxis()  # Invert y-axis to have (0,0) at the top-left corner
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, color='black')

    # Fill in the letters from the grid
    for i in range(nrows):
        for j in range(ncols):
            ax.text(j + 0.5, i + 0.5, grid[i][j], va='center', ha='center', fontsize=12, color='black')

    # Highlight the placed words
    for word, (start_row, start_col), (dx, dy) in placed_words:
        x = start_col + 0.5
        y = start_row + 0.5
        for char in word:
            ax.text(x, y, char, va='center', ha='center', fontsize=12, color='red', fontweight='bold')
            x += dx
            y += dy

    # Display the plot
    plt.title("Word Search Puzzle", fontsize=16)
    plt.show()

# Plot the wordsearch grid with the placed words
if grid:
    plot_wordsearch(grid, placed_words)

if grid:
    show_wordsearch_with_words(grid, wordlist, placed_words)

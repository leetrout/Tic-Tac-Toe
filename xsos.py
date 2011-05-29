import random

class Grid(object):
    """
    A simple class for playing X's & O's (tic tac toe).
    """
    # marks as constants
    X = 1
    O = 2
    # marks as dict
    marks = {
        'X':1,
        'O':2,
        '1':'X',
        '2':'O'
    }
    cat = 'Cat'
    grid = []
    # size of the grid
    size = None
    # str representation of the winner. Will be X, O, or Cat
    winner = ''
    
    def __init__(self, size=3):
        """
        Constructs a square grid of the given size (3 by default).
        """
        self.size = size
        self._create_grid()
    
    def _create_grid(self):
        """
        Creates the playing grid from self.size in self.grid.  Will desctruct
        an existing grid.
        
        Returns None.
        """
        grid = []
        size = self.size
        rng = range(size)
        for i in rng:
            row = [0]*size
            grid.append(row)
        self.grid = grid
    
    def _get_rotated_grid(self):
        """
        Returns self.grid rotated 90 degrees so columns become rows.
        
        See http://mail.python.org/pipermail/tutor/2006-November/051039.html
        """
        size = self.size
        return [[self.grid[col][size-row-1] for col in range(size)] for row in range(size)]
    
    def _get_diagonal_rows(self):
        """
        Returns the 2 diagonal rows in a list with the top left to bottom right
        first.
        """
        size = self.size
        rng = range(size)
        return [[self.grid[x][x] for x in rng], [self.grid[x][size-x-1] for x in rng]]
    
    def _get_all_rows(self):
        """
        Returns the grid with the addition of columns and diagonals as rows.
        """
        return self.grid + self._get_rotated_grid() + self._get_diagonal_rows()
    
    def _get_pretty_print_grid(self):
        """
        Returns a string representing the current playing grid.
        """
        s = ''
        size = self.size
        rng = range(size)
        for i in rng:
            r = self.grid[i]
            for c in rng:
                if r[c]:
                    s += " %s " % self.marks[str(r[c])]
                else:
                    s += "   "
                if c+1 < size:
                    s += "|"
            if i+1 < size:
                s += "\n"
                s += "---+" * (size-1)
                s += "---\n"
        return s
    
    def _find_major_row(self, mark):
        """
        Looks for self.size-1 (two in a row for standard tic tac toe) of the
        given mark in a row and returns the grid position of the open space as
        a tuple (row, col)
        """
        size = self.size
        rng = range(size)
        rgrid = self._get_rotated_grid()
        diags = self._get_diagonal_rows()
        for r in rng:
            if self.grid[r].count(mark) >= size-1:
                return (r, self.grid[r].index(0))
            if rgrid[r].count(mark) >= size-1:
                return (rgrid[r].index(0), size-1-r)
        for r in range(len(diags)):
            # backwards diag first
            if diags[r].count(mark) >= size-1:
                idx = diags[r].index(0)
                if not r:
                    return (idx, idx)
                else:
                    return (idx, size-1-idx)
    
    def game_over(self):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        size = self.size
        all_rows = self._get_all_rows()
        if '0' not in str(all_rows):
            self.winner = self.cat
            return True
        for r in all_rows:
            # only check rows that are full
            s = sum(r)
            if 0 not in r and not s%size:
                self.winner = self.marks[str(s/size)]
                return True
        self.winner = ''
        return False
    
    def move(self, mark):
        """
        Completes a move for the given mark automatically.
        """
        # see if we need to block:
        opmark = 1 if mark == 2 else 2
        block = self._find_major_row(opmark)
        if block:
            self.grid[block[0]][block[1]] = mark
            return
        best = self._find_major_row(mark)
        if best:
            self.grid[best[0]][best[1]] = mark
            return
        # take a random open position
        while True:
            r = random.randrange(self.size)
            c = random.randrange(self.size)
            if not self.grid[r][c]:
                self.grid[r][c] = mark
                return
    
    def autoplay(self):
        players = ('X', 'O')
        over = self.game_over()
        while not over:
            for p in players:
                self.move(self.marks[p])
                over = self.game_over()
                if over:
                    break
        print("%s won!" % self.winner)
        print(self._get_pretty_print_grid())
    
    def reset(self):
        """
        Resets the current winner and grid
        """
        self.winner = ''
        self._create_grid()
    
    def play(self):
        """
        Plays the game of tic tac toe
        """
        players = ('X', 'O')
        over = self.game_over()
        rng = range(self.size)
        while not over:
            for p in players:
                print("Player %s is up!" % p)
                print("Current Grid:")
                print(self._get_pretty_print_grid())
                valid_cell = False
                while not valid_cell:
                    print "Please choose an open cell to place your mark"
                    r = -1
                    while r not in rng:
                        i = raw_input("Please select a row (1-%s): " % str(self.size))
                        try:
                            r = int(i) - 1
                        except:
                            print "Please enter a valid choice."
                            continue
                    c = -1
                    while c not in rng:
                        i = raw_input("Please select a column (1-%s): " % str(self.size))
                        try:
                            c = int(i) - 1
                        except:
                            print "Please enter a valid choice."
                            continue
                    valid_cell = not self.grid[r][c]
                self.grid[r][c] = getattr(self, p)
                over = self.game_over()
                if over:
                    break
        print("The game is over. %s won!" % self.winner)
        print(self._get_pretty_print_grid())
    
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        elif self.count == 0:
            return {}
        else:
            return "We don't know which cells are mines here"
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) == self.count:
            return {}
        elif self.count == 0:
            return self.cells
        else:
            return "We don't know which cells are safe here"
        raise NotImplementedError

    def mark_mine(self, cell):          #think this basically removes it from set of cells that we're considering moving to. THink I'll need to address the bit in spec that says "but still represents a logically correct sentence given that cell is known to be a mine" cos I dont really know what that means. Like what does fact cell is a mine have to do with sentence being log'y correct
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells: #hopefully 'cell' corresponds to cell given as input to mark_mine and 'cells' to the cells inputted in the instance of Sentence
            self.cells.remove(cell)
            self.count -= 1   #this line is the one which makes sure the sentence stays logically correct
        else:
            pass
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """
    

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  #adds cell to set of moves made
        self.safes.add(cell)  #we know this cell to be safe(since we've not lost game by moving to it), thus add it to set of safes

 
        #Creating the set of neigbours:
        if cell == (0,0):
            neighbours = {(1,0),(1,1),(0,1)}
        elif cell == (0,self.width-1):
            neighbours = {(1,self.width-1),(1,self.width-2),(0,self.width-2)}
        elif cell == (self.height-1,0):
            neighbours = {(self.height-2,0),(self.height-2,1),(self.height-1,1)}
        elif cell == (self.height-1,self.width-1):
            neighbours = {(self.height-2,self.width-1),(self.height-2,self.width-2),(self.height-1,self.width-2)}
        elif cell[0] == 0:
            neighbours = {(cell[0],cell[1]-1),(cell[0],cell[1]+1),(cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1)}
        elif cell[0] == self.height-1:
            neighbours = {(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]-1),(cell[0],cell[1]+1)}
        elif cell[1] == 0:
            neighbours = {(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]+1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1)}
        elif cell[1] == self.width-1:
            neighbours = {(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0],cell[1]-1),(cell[0]+1,cell[1]-1),(cell[0]+1,cell[1])}
        else:
            neighbours = {(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]-1),(cell[0],cell[1]+1),\
            (cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1)}


        nbs_unknown = set() #denotes the neigbours that we don't know are mines or safe, and will be added to Knowledge Base
        nbs_mines =set() #denotes neighbours that are mines
        nbs_safes = set() #denotes neighbours that are safes

        for cell_x in neighbours:
            if cell_x in self.mines:
                nbs_mines.add(cell_x)
            elif cell_x in self.safes: 
                nbs_safes.add(cell_x)   #these 2 checks ensure only cells with undetermined states are added to the KB, rest are added to mine or safe sets
            else:
                nbs_unknown.add(cell_x)


        if count == len(nbs_mines) + len(nbs_unknown):  #if this is true, we know all cells in nbs_kb are mines
            for mine_cell in nbs_unknown:
                self.mines.add(mine_cell) #adding all these cells, known to be mines, to set whole set of cells of mines in the game
        elif count == len(nbs_mines): #if this is true, then only the neighbours that are in nbs_mines are mines, i.e. none of cells in nbs_kb are mines so they're all safes
            for safe_cell in nbs_unknown:
                self.safes.add(safe_cell)
        elif len(nbs_unknown) != 0:
            self.knowledge.append(Sentence(nbs_unknown,int(count - len(nbs_mines))))  #Here I am adding the unknown cells to the kb(only after checking that we can't work out their states in above if conditions)
        else:                           
            pass


        if len(self.knowledge)==0:
            pass
        else:
            for i in range(len(self.knowledge)):       
                for j in range(i + 1, len(self.knowledge)):
                    if self.knowledge[i].cells.issubset(self.knowledge[j].cells) or self.knowledge[j].cells.issubset(self.knowledge[i].cells):
                        if len(self.knowledge[i].cells) > len(self.knowledge[j].cells):
                            superset = self.knowledge[i].cells 
                            superset_count = self.knowledge[i].count
                            subset = self.knowledge[j].cells
                            subset_count = self.knowledge[j].count
                            self.knowledge = [Sentence(superset - subset, superset_count - subset_count) if x == self.knowledge[i]\
                            else x for x in self.knowledge]
                        else:
                            superset = self.knowledge[j].cells
                            superset_count = self.knowledge[j].count
                            subset = self.knowledge[i].cells
                            subset_count = self.knowledge[i].count
                            self.knowledge = [Sentence(superset - subset, superset_count - subset_count) if x == self.knowledge[j]\
                            else x for x in self.knowledge]

# this ^ function will execute every time add_knowledge is called. This is important because every time we find out about a cell and it's count (this new info 
#can help tell us information about the cells already in the KB)
        self.removing = []

        for i in range(len(self.knowledge)):
            if len(self.knowledge[i].cells) == 0: 
                self.removing.append(self.knowledge[i])
            elif len(self.knowledge[i].cells) == self.knowledge[i].count:
                for cell_x in self.knowledge[i].cells:
                    self.mines.add(cell_x)
                self.removing.append(self.knowledge[i])
            elif self.knowledge[i].count == 0:
                for cell_x in self.knowledge[i].cells:
                    self.safes.add(cell_x)
                self.removing.append(self.knowledge[i])
            else:
                pass

        for sentence in self.removing:
                self.knowledge.remove(sentence)

#even though we did something similar to this ^^ before (line 246 to 255), we need to do it again as here we are considering all sentences in the KB, not just the one
#that has been added, which is what we were considering above




    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        poss_cells = []
        for cell in self.safes:
            if cell not in self.moves_made:
                poss_cells.append(cell)

        if len(poss_cells) == 0:
            return None 
        else:
            return random.choice(poss_cells)


        




    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be miness
        """


        self.all_cells = []
        for i in range(0,self.height-1):
            for j in range(0, self.width-1):
                self.all_cells.append((i,j))

        poss_cells = []
        for i in range(0,self.height-1):
            for j in range(0,self.width-1):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    poss_cells.append((i,j))

        poss_cells = []
        for cell in self.all_cells:
            if cell not in self.moves_made and cell not in self.mines:
                poss_cells.append(cell)

        if len(poss_cells) == 0:
            return None 
        else:
            return random.choice(poss_cells)

        





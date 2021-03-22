#!/usr/bin/env python3
import configparser
import json
import time
import tkinter as tk

config = {}
with open('./config.json') as file:
    config = json.load(file)

CELL_WIDTH = config.get('CELL_WIDTH', 3)
CELL_HEIGHT = config.get('CELL_HEIGHT', 1)
NUM_OF_ROWS = config.get('NUM_OF_ROWS', 10)
NUM_OF_COLS = config.get('NUM_OF_COLS', 10)


class ApplicationUI():
    def __init__(self, parent, rows, columns, game):
        '''UI for the Game of Life

        Args:
            parent (tk.TK): Root widget for Tkinter frame
            rows (int): No of rows in UI
            columns (iny): No of columns in UI
            game (GameOfLife): Game controller
        '''
        self.content = tk.Frame(parent)
        self.actions = tk.Frame(parent)
        self.content.grid(row=1, column=1)
        self.actions.grid(row=2, column=1)
        self.parent = parent
        self.rows = rows
        self.columns = columns
        self.game = game
        self.started = False
        self.updater_id = None

        self.init_grid()
        self.add_padding()
        self.add_buttons()

    def add_padding(self):
        '''Add padding all around to make the content appear in center of screen
        '''
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)

    def add_buttons(self):
        '''Add 2 actions buttons to UI - Start and Stop
        '''
        start_button = tk.Button(
            self.actions, text='Start', command=self.start)
        start_button.grid(row=0, column=0)

        stop_button = tk.Button(self.actions, text='Stop', command=self.stop)
        stop_button.grid(row=0, column=1)

    def update(self):
        '''Update the game state by 1 step and re-render the UI
        '''
        # Clear all alive cells. Update game state and then set alive cells
        self.clear_alive()
        self.game.update()
        for pos in self.game.living_cells:
            self.set_alive_ui(pos)

        # Call update again after a delay of 1 second, if game is still going on.
        if not self.game.life_over():
            self.updater_id = self.content.after(1000, self.update)
        else:
            self.started = False

    def clear_alive(self):
        '''Clear all alive cells in UI
        '''
        for pos in self.game.living_cells:
            self.set_dead_ui(pos)

    def start(self):
        '''Callback for Start button. Start the game animation.
        '''
        self.started = True
        self.updater_id = self.content.after(1000, self.update)

    def stop(self):
        '''Callback for Stop button. Stop the game animation and reset everything
        '''
        # If game has started, clear the scheduled update so that update is not called.
        if self.updater_id is not None:
            self.content.after_cancel(self.updater_id)
        self.clear_alive()
        self.game.reset()
        self.started = False

    def cell_clicked(self, pos):
        '''Callback when a cell on UI is clicked. Set the corresponding cell as alive

        Args:
            pos ((int, int)): Position of currently clicked cell
        '''
        if not self.started:
            self.grid[pos[0]][pos[1]].configure(bg='red')
            self.game.set_alive(pos)

    def set_alive_ui(self, pos):
        '''Set a cell in UI as alive

        Args:
            pos ((int, int)): Position of cell to be set alive
        '''
        self.grid[pos[0]][pos[1]].configure(bg='red')

    def set_dead_ui(self, pos):
        '''Set a cell in UI as dead

        Args:
            pos ((int, int)): Position of cell to be set dead
        '''
        self.grid[pos[0]][pos[1]].configure(bg='white')

    def init_grid(self):
        '''Initiate the UI by adding cells
        '''
        self.grid = []
        for row in range(self.rows):
            labels = []
            for col in range(self.columns):
                label = tk.Label(self.content, borderwidth=2, relief='solid',
                                 bg='white', width=CELL_WIDTH, height=CELL_HEIGHT)
                label.grid(row=row, column=col)
                label.bind('<Button-1>', lambda e, pos=(row, col)
                           : self.cell_clicked(pos))
                labels.append(label)

            self.grid.append(labels)


class GameOfLife:
    def __init__(self, rows, cols):
        '''Manages state of Game of Life

        Args:
            rows (int): no of rows for the grid
            cols (int): no of columns for the grid
        '''        '''
        '''
        self.rows = rows
        self.cols = cols
        self.initialise_state()

    def initialise_state(self, state=None):
        '''Initialise the game state with every cell being dead (False) and no living cells if no state is given,
        else assign the given state.

        Args:
            state (list of list), None): Initial state of game. Defaults to None.
        '''
        self.state = [[False for _ in range(self.cols)] for _ in range(
            self.rows)] if state is None else state
        self.living_cells = set()

    def set_alive(self, pos):
        '''Set a cell as alive for the given position

        Args:
            pos ((int, int)): Position of grid to be made alive
        '''
        row, col = pos
        self.state[row][col] = True
        self.living_cells.add(pos)

    def set_dead(self, pos):
        '''Set a cell as dead for the given position. Also remove from the set of living cells

        Args:
            pos ((int, int)): Position of grid to be killed
        '''
        row, col = pos
        self.state[row][col] = False
        self.living_cells.remove(pos)

    def life_over(self):
        '''Returns whether game is over (All cells are dead)

        Returns:
            boolean: True if no cell is alive, otherwise False
        '''
        return len(self.living_cells) == 0

    def get_neighbours(self, pos):
        '''Return all horizontal, vertical and diagonal neighbours of a cell depending on position

        Args:
            pos ((int, int)): Position of cell

        Returns:
            set: Set of valid neighbouring positions
        '''
        row, col = pos
        dir_vectors = [(0, 1), (0, -1), (1, 0), (1, -1),
                       (1, 1), (-1, 0), (-1, -1), (-1, 1)]
        neighbours = set([(row + dir_vector[0], col + dir_vector[1])
                          for dir_vector in dir_vectors
                          if (0 <= row + dir_vector[0] < self.rows) and (0 <= col + dir_vector[1] < self.cols)])
        return neighbours

    def update(self):
        '''Update the game state according to following rules
        * If the cell is alive, then it stays alive if it has either 2 or 3 live neighbours
        * If the cell is dead, then it springs to life only in the case that it has 3 live neighbours
        '''
        dead_neighbours = {}
        cells_to_kill = set()
        cells_to_revive = set()
        for cell in self.living_cells:
            neighbours = self.get_neighbours(cell)
            alive_neighbours = 0
            for neighbour in neighbours:
                if neighbour in self.living_cells:
                    alive_neighbours += 1
                else:
                    dead_neighbours[neighbour] = dead_neighbours.get(
                        neighbour, 0) + 1

            if alive_neighbours < 2 or alive_neighbours > 3:
                cells_to_kill.add(cell)

        for dead_neighbour, alive_neighbours in dead_neighbours.items():
            if alive_neighbours == 3:
                cells_to_revive.add(dead_neighbour)

        for cell in cells_to_kill:
            self.set_dead(cell)

        for cell in cells_to_revive:
            self.set_alive(cell)

    def reset(self):
        '''Reset the state of the game
        '''
        self.initialise_state()


if __name__ == '__main__':
    game = GameOfLife(NUM_OF_ROWS, NUM_OF_COLS)
    root = tk.Tk()
    root.attributes('-zoomed', True)

    root.title('Game of Life')
    ApplicationUI(root, NUM_OF_ROWS, NUM_OF_COLS, game)
    root.mainloop()

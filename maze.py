from cell import Cell
import random
import time

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
        ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        for i in range(self._num_cols):
            cell_col = []
            for j in range(self._num_rows):
                cell_col.append(Cell(self._win))
            self._cells.append(cell_col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        x2 = x1 + self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
        
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        
        while True:
            unvisited_neighbors = []
            if j > 0 and not self._cells[i][j - 1].visited:
                unvisited_neighbors.append((i, j - 1, "up"))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                unvisited_neighbors.append((i + 1, j, "right"))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                unvisited_neighbors.append((i, j + 1, "down"))
            if i > 0 and not self._cells[i - 1][j].visited:
                unvisited_neighbors.append((i - 1, j, "left"))
            
            if len(unvisited_neighbors) == 0:
                self._draw_cell(i, j)
                return
            
            next_cell_info = random.randrange(len(unvisited_neighbors))
            next_i, next_j, direction = unvisited_neighbors[next_cell_info]
            
            if direction == "up":
                current_cell.has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            if direction == "right":
                current_cell.has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            if direction == "down":
                current_cell.has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            if direction == "left":
                current_cell.has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            
            self._break_walls_r(next_i, next_j)
        
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        
        self._cells[i][j].visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        # right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)
                
        # left
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
                
        # up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
                
        # down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        
        return False
    
    def solve(self):
        return self._solve_r(0, 0)
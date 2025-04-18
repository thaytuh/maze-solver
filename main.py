from graphics import Window
from cell import Cell

def main():
    win = Window(800, 600)
    cell = Cell(40, 40, 80, 80, win)
    cell.has_right_wall = False
    cell.draw()
    cell2 = Cell(80, 40, 120, 80, win)
    cell2.has_left_wall = False
    cell2.draw()
    win.wait_for_close()


if __name__ == "__main__":
    main()
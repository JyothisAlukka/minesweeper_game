from tkinter import *
import random
import configure
import ctypes
import sys

class Cell:
    all = []
    cell_count = configure.cell_count
    cell_count_label_object = None
    
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened = False
        self.is_mine_candidate = False
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_btn_object(self, location):
        self.cell_btn_object = Button(
            location,
            width=12,
            height=4,
        )
        self.cell_btn_object.bind('<Button-1>', self.left_click_actions)
        self.cell_btn_object.bind('<Button-3>', self.right_click_actions)

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

            if Cell.cell_count == configure.mines_count:
                ctypes.windll.user32.MessageBoxW(0, "Congratulations! You won the game!", "Game Over", 0)
                sys.exit()

    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(None, "You clicked on a mine! Try again.", "Game Over", 0)
        self.restart_game()
    
    def restart_game(self):
        for cell in Cell.all:
            cell.is_mine = False
            cell.is_opened = False
            cell.is_mine_candidate = False
            cell.cell_btn_object.configure(text="", bg="SystemButtonFace")
        Cell.randomize_mines()
        Cell.cell_count = configure.cell_count
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(text=f"Cells Left: {Cell.cell_count}")

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        return None

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x, self.y+1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1)
        ]
        return [cell for cell in cells if cell is not None]

    @property
    def surrounded_cells_mines_length(self):
        return sum(1 for cell in self.surrounded_cells if cell.is_mine)

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length, bg="white")
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left: {Cell.cell_count}")
            self.is_opened = True

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg="orange")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg="white")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, configure.mines_count)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    @staticmethod
    def create_cell_count_label(location):
        Cell.cell_count_label_object = Label(
            location, 
            text=f"Cells Left: {Cell.cell_count}",
            bg="#5D6D7E",
            fg="white",
            font=("", 14)
        )

    def __repr__(self):
        return f"Cell({self.x},{self.y})"
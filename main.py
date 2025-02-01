from tkinter import *
import configure
from new import height_prct,width_prct
from unit import Cell

root = Tk()
root.config(bg="black")
root.geometry(f'{configure.width}x{configure.height}')
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(root, bg="#5D6D7E", width=configure.width, height=height_prct(25))
top_frame.place(x=0, y=0)

game_title = Label(top_frame, bg="#5D6D7E", fg="white", text="Minesweeper Game", font=("", 30))
game_title.place(x=width_prct(25), y=0)

center_frame = Frame(root, bg="black", width=width_prct(75), height=height_prct(75))
center_frame.place(x=width_prct(15), y=height_prct(25))

for x in range(configure.grid_size):
    for y in range(configure.grid_size):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

Cell.create_cell_count_label(top_frame)
Cell.cell_count_label_object.place(x=width_prct(42), y=height_prct(15))

Cell.randomize_mines()

root.mainloop()
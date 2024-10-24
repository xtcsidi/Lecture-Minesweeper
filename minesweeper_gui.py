import random
import tkinter as tk
from tkinter import messagebox

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.game = Minesweeper(16, 16, 40)
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        self.flag_var = tk.StringVar()
        self.flag_var.set("🚩: 0")
        flag_label = tk.Label(self.master, textvariable=self.flag_var, font=("Arial", 24))
        flag_label.grid(row=0, column=0, columnspan=self.game.width, pady=10)

        button_frame = tk.Frame(self.master)
        button_frame.grid(row=1, column=0, columnspan=self.game.width, padx=20, pady=20)

        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                button = tk.Button(button_frame, width=3, height=1, font=("Arial", 16))
                button.config(command=lambda x=x, y=y: self.on_click(x, y))
                button.bind('<Button-3>', lambda e, x=x, y=y: self.on_right_click(x, y))
                button.grid(row=y, column=x, padx=1, pady=1)
                row.append(button)
            self.buttons.append(row)

    def on_click(self, x, y):
        if not self.game.reveal(x, y):
            self.show_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.master.quit()
        elif self.game.is_win():
            self.show_mines()
            messagebox.showinfo("Congratulations", "You won!")
            self.master.quit()
        self.update_board()

    def on_right_click(self, x, y):
        self.game.flag(x, y)
        self.update_board()

    def update_board(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                button = self.buttons[y][x]
                if (x, y) in self.game.flagged:
                    button.config(text="🚩", bg="yellow")
                elif (x, y) in self.game.revealed:
                    if self.game.board[y][x] == ' ':
                        button.config(text="", bg="lightgray")
                    else:
                        button.config(text=self.game.board[y][x], bg="lightgray")
                else:
                    button.config(text="", bg="SystemButtonFace")
        
        self.flag_var.set(f"🚩: {len(self.game.flagged)}")

    def show_mines(self):
        for (x, y) in self.game.mines:
            self.buttons[y][x].config(text="💣", bg="red")

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.mines = set()
        self.revealed = set()
        self.flagged = set()
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        while len(self.mines) < self.num_mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))

    def calculate_numbers(self):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.mines:
                    count = sum(1 for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                                if (x + dx, y + dy) in self.mines)
                    if count > 0:
                        self.board[y][x] = str(count)

    def reveal(self, x, y):
        if (x, y) in self.revealed or (x, y) in self.flagged:
            return True

        self.revealed.add((x, y))

        if (x, y) in self.mines:
            return False

        if self.board[y][x] == ' ':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal(nx, ny)

        return True

    def flag(self, x, y):
        if (x, y) not in self.revealed:
            if (x, y) in self.flagged:
                self.flagged.remove((x, y))
            else:
                self.flagged.add((x, y))

    def is_win(self):
        return len(self.revealed) + len(self.mines) == self.width * self.height

if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGUI(root)
    root.mainloop()

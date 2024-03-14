import tkinter as tk
import random

class SnakesAndLaddersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snakes and Ladders")
        self.master.geometry("500x550")

        self.canvas = tk.Canvas(self.master, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        self.board_size = 10
        self.snakes_and_ladders = self.generate_snakes_and_ladders()

        self.create_board()

        self.player_position = 1
        self.create_player()

        self.button_roll = tk.Button(self.master, text="Roll Dice", command=self.roll_dice)
        self.button_roll.pack()

        self.button_history = tk.Button(self.master, text="Dice Roll History", command=self.show_history)
        self.button_history.pack()

        self.dice_history = []

        self.animation_speed = 200  # milliseconds

    def generate_snakes_and_ladders(self):
        num_snakes_ladders = 10
        snakes_ladders = {}

        for _ in range(num_snakes_ladders):
            start = random.randint(10, self.board_size ** 2 - 10)
            end = random.randint(1, start - 1) if start > self.board_size else random.randint(start + 1, self.board_size ** 2)
            snakes_ladders[start] = end

        return snakes_ladders

    def create_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = j * 50
                y1 = i * 50
                x2 = x1 + 50
                y2 = y1 + 50

                position = i * self.board_size + j + 1
                color = "white" if (i + j) % 2 == 0 else "lightgray"
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(position), fill="black")

        for start, end in self.snakes_and_ladders.items():
            start_row, start_col = self.get_row_col(start)
            end_row, end_col = self.get_row_col(end)

            x1 = start_col * 50 + 25
            y1 = start_row * 50 + 25
            x2 = end_col * 50 + 25
            y2 = end_row * 50 + 25

            color = "red" if start > end else "green"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3)

    def create_player(self):
        row, col = self.get_row_col(self.player_position)
        x1 = col * 50 + 10
        y1 = row * 50 + 10
        x2 = x1 + 30
        y2 = y1 + 30
        self.player = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="blue")

    def move_player(self, new_position):
        self.canvas.delete(self.player)
        self.player_position = new_position
        row, col = self.get_row_col(new_position)
        x1 = col * 50 + 10
        y1 = row * 50 + 10
        x2 = x1 + 30
        y2 = y1 + 30
        self.player = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="blue")

    def get_row_col(self, position):
        row = (position - 1) // self.board_size
        col = (position - 1) % self.board_size
        return row, col

    def animate_movement(self, dice_result, remaining_steps):
        if remaining_steps > 0:
            new_position = self.player_position + 1
            if new_position in self.snakes_and_ladders:
                new_position = self.snakes_and_ladders[new_position]

            self.move_player(new_position)
            self.dice_history.append(dice_result)
            self.master.after(self.animation_speed, lambda: self.animate_movement(dice_result, remaining_steps - 1))
        else:
            if self.player_position >= 100:
                self.end_game()

    def roll_dice(self):
        dice_result = random.randint(1, 6)
        self.animate_movement(dice_result, dice_result)

    def show_history(self):
        history_str = "\n".join([f"Roll {i + 1}: {self.dice_history[i]}" for i in range(len(self.dice_history))])
        tk.message

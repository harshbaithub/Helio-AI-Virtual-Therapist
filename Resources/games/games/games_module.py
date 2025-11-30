import tkinter as tk
from tkinter import ttk
import random
import math
import time

class GamesHub:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Stress Relief Games")
        self.window.geometry("800x600")
        self.window.configure(bg="#2c3e50")
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            main_frame,
            text="🎮 Stress Relief Games",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Games grid
        games_frame = ttk.Frame(main_frame)
        games_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bubble Pop
        self.create_game_card(
            games_frame,
            "Bubble Pop",
            "Pop calming bubbles to release stress",
            0, 0,
            self.start_bubble_pop
        )
        
        # Tetris
        self.create_game_card(
            games_frame,
            "Tetris",
            "The classic block-stacking game to focus your mind",
            0, 1,
            self.start_tetris
        )
        
        # Brick Smasher
        self.create_game_card(
            games_frame,
            "Brick Smasher",
            "Break colorful bricks with a bouncing ball",
            1, 0,
            self.start_brick_smasher
        )
        
        # Sliding Puzzle
        self.create_game_card(
            games_frame,
            "Sliding Puzzle",
            "Rearrange tiles to complete the picture",
            1, 1,
            self.start_sliding_puzzle
        )
        
    def create_game_card(self, parent, title, description, row, col, command):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        # Title
        ttk.Label(
            card,
            text=title,
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        # Description
        ttk.Label(
            card,
            text=description,
            wraplength=200,
            justify="center"
        ).pack(pady=(0, 10))
        
        # Play button
        ttk.Button(
            card,
            text="Play",
            command=command,
            style="Play.TButton"
        ).pack(pady=(0, 10))
        
    def start_bubble_pop(self):
        BubblePopGame(self.window)
        
    def start_tetris(self):
        TetrisGame(self.window)
        
    def start_brick_smasher(self):
        BrickSmasherGame(self.window)
        
    def start_sliding_puzzle(self):
        SlidingPuzzleGame(self.window)

class BubblePopGame:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Bubble Pop")
        self.window.geometry("600x500")
        self.window.configure(bg="#2c3e50")
        
        self.setup_game()
        
    def setup_game(self):
        self.canvas = tk.Canvas(
            self.window,
            width=600,
            height=500,
            bg="#2c3e50",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.bubbles = []
        self.score = 0
        
        # Score label
        self.score_label = tk.Label(
            self.window,
            text=f"Bubbles Popped: {self.score}",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="white"
        )
        self.score_label.place(x=10, y=10)
        
        # Start spawning bubbles
        self.spawn_bubble()
        
    def spawn_bubble(self):
        if len(self.bubbles) < 10:  # Limit number of bubbles
            x = random.randint(50, 550)
            y = random.randint(50, 450)
            size = random.randint(20, 40)
            color = random.choice(['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6'])
            
            bubble = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline="white"
            )
            
            self.bubbles.append(bubble)
            self.canvas.tag_bind(bubble, '<Button-1>', lambda e, b=bubble: self.pop_bubble(b))
            
            # Add some floating animation
            self.float_bubble(bubble)
        
        self.window.after(2000, self.spawn_bubble)
        
    def float_bubble(self, bubble):
        if bubble in self.bubbles:
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            
            self.canvas.move(bubble, dx, dy)
            
            # Keep bubble in bounds
            pos = self.canvas.coords(bubble)
            if pos[0] < 0 or pos[2] > 600:
                dx = -dx
            if pos[1] < 0 or pos[3] > 500:
                dy = -dy
            
            self.window.after(50, lambda: self.float_bubble(bubble))
        
    def pop_bubble(self, bubble):
        if bubble in self.bubbles:
            # Add pop animation
            pos = self.canvas.coords(bubble)
            x = (pos[0] + pos[2]) / 2
            y = (pos[1] + pos[3]) / 2
            
            # Create pop effect
            size = 20
            pop = self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                outline="white",
                width=2
            )
            
            self.canvas.delete(bubble)
            self.bubbles.remove(bubble)
            self.score += 1
            self.score_label.config(text=f"Bubbles Popped: {self.score}")
            
            # Remove pop effect after animation
            self.window.after(100, lambda: self.canvas.delete(pop))

class TetrisGame:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Tetris")
        self.window.geometry("400x600")
        self.window.configure(bg="#2c3e50")
        
        self.block_size = 25
        self.cols = 10
        self.rows = 20
        self.setup_game()
        
    def setup_game(self):
        # Score frame
        score_frame = ttk.Frame(self.window)
        score_frame.pack(pady=10)
        
        self.score = 0
        self.score_label = ttk.Label(
            score_frame,
            text=f"Score: {self.score}",
            font=("Arial", 14)
        )
        self.score_label.pack()
        
        # Game canvas
        self.canvas = tk.Canvas(
            self.window,
            width=self.cols * self.block_size,
            height=self.rows * self.block_size,
            bg="#34495e"
        )
        self.canvas.pack(pady=10)
        
        # Initialize game state
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = None
        self.game_over = False
        
        # Bind keys
        self.window.bind('<Left>', lambda e: self.move(-1))
        self.window.bind('<Right>', lambda e: self.move(1))
        self.window.bind('<Down>', lambda e: self.move_down())
        self.window.bind('<Up>', lambda e: self.rotate())
        
        self.new_piece()
        self.update()
        
    def new_piece(self):
        # Tetris pieces (I, O, T, S, Z, J, L)
        pieces = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 0], [1, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]]
        ]
        colors = ['#3498db', '#f1c40f', '#9b59b6', '#2ecc71', '#e74c3c', '#e67e22', '#1abc9c']
        
        piece_idx = random.randint(0, len(pieces) - 1)
        self.current_piece = {
            'shape': pieces[piece_idx],
            'color': colors[piece_idx],
            'x': self.cols // 2 - len(pieces[piece_idx][0]) // 2,
            'y': 0
        }
        
        if self.check_collision():
            self.game_over = True
    
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw placed blocks
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x]:
                    self.draw_block(x, y, self.board[y][x])
        
        # Draw current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(
                            self.current_piece['x'] + x,
                            self.current_piece['y'] + y,
                            self.current_piece['color']
                        )
    
    def draw_block(self, x, y, color):
        x1 = x * self.block_size
        y1 = y * self.block_size
        x2 = x1 + self.block_size
        y2 = y1 + self.block_size
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="white"
        )
    
    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    
                    if (board_x < 0 or board_x >= self.cols or
                        board_y >= self.rows or
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False
    
    def move(self, dx):
        self.current_piece['x'] += dx
        if self.check_collision():
            self.current_piece['x'] -= dx
    
    def move_down(self):
        self.current_piece['y'] += 1
        if self.check_collision():
            self.current_piece['y'] -= 1
            self.place_piece()
            self.new_piece()
            self.check_lines()
    
    def rotate(self):
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = list(zip(*reversed(self.current_piece['shape'])))
        if self.check_collision():
            self.current_piece['shape'] = old_shape
    
    def place_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_piece['y'] + y
                    board_x = self.current_piece['x'] + x
                    if 0 <= board_y < self.rows:
                        self.board[board_y][board_x] = self.current_piece['color']
    
    def check_lines(self):
        lines_to_clear = []
        for y in range(self.rows):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [None] * self.cols)
            self.score += 100
            self.score_label.config(text=f"Score: {self.score}")
    
    def update(self):
        if not self.game_over:
            self.move_down()
            self.draw_board()
            self.window.after(500, self.update)
        else:
            self.canvas.create_text(
                self.cols * self.block_size // 2,
                self.rows * self.block_size // 2,
                text="Game Over!",
                font=("Arial", 20, "bold"),
                fill="white"
            )

class BrickSmasherGame:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Brick Smasher")
        self.window.geometry("600x700")
        self.window.configure(bg="#2c3e50")
        
        self.setup_game()
        
    def setup_game(self):
        # Score frame
        score_frame = ttk.Frame(self.window)
        score_frame.pack(pady=10)
        
        self.score = 0
        self.score_label = ttk.Label(
            score_frame,
            text=f"Score: {self.score}",
            font=("Arial", 14)
        )
        self.score_label.pack()
        
        # Game canvas
        self.canvas = tk.Canvas(
            self.window,
            width=600,
            height=600,
            bg="#34495e",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Initialize game objects
        self.paddle_width = 100
        self.paddle_height = 10
        self.ball_radius = 8
        
        # Create paddle
        self.paddle = self.canvas.create_rectangle(
            250, 550,
            250 + self.paddle_width, 550 + self.paddle_height,
            fill="#3498db"
        )
        
        # Create ball
        self.ball = self.canvas.create_oval(
            290, 530,
            290 + self.ball_radius * 2, 530 + self.ball_radius * 2,
            fill="#f1c40f"
        )
        
        # Ball movement
        self.ball_speed_x = 4
        self.ball_speed_y = -4
        self.game_started = False
        
        # Create bricks
        self.create_bricks()
        
        # Bind controls
        self.canvas.bind('<Motion>', self.move_paddle)
        self.window.bind('<space>', self.start_game)
        
        # Start game loop
        self.game_loop()
        
    def create_bricks(self):
        self.bricks = []
        colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db']
        brick_width = 58
        brick_height = 20
        
        for row in range(5):
            for col in range(10):
                brick = self.canvas.create_rectangle(
                    col * (brick_width + 2) + 1,
                    row * (brick_height + 2) + 1,
                    (col + 1) * (brick_width + 2) - 1,
                    (row + 1) * (brick_height + 2) - 1,
                    fill=colors[row]
                )
                self.bricks.append(brick)
    
    def move_paddle(self, event):
        paddle_pos = self.canvas.coords(self.paddle)
        paddle_center = (paddle_pos[2] - paddle_pos[0]) / 2
        
        if 0 <= event.x - paddle_center <= 600 - self.paddle_width:
            self.canvas.moveto(self.paddle, event.x - paddle_center, 550)
            
            if not self.game_started:
                self.canvas.moveto(
                    self.ball,
                    event.x - paddle_center + self.paddle_width/2 - self.ball_radius,
                    530
                )
    
    def start_game(self, event):
        self.game_started = True
    
    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)
        
        # Wall collisions
        if ball_pos[0] <= 0 or ball_pos[2] >= 600:
            self.ball_speed_x = -self.ball_speed_x
        if ball_pos[1] <= 0:
            self.ball_speed_y = -self.ball_speed_y
        
        # Paddle collision
        paddle_pos = self.canvas.coords(self.paddle)
        if (ball_pos[2] >= paddle_pos[0] and
            ball_pos[0] <= paddle_pos[2] and
            ball_pos[3] >= paddle_pos[1] and
            ball_pos[1] <= paddle_pos[3]):
            
            # Calculate bounce angle based on where ball hits paddle
            hit_pos = (ball_pos[0] + ball_pos[2])/2
            paddle_center = (paddle_pos[0] + paddle_pos[2])/2
            angle = (hit_pos - paddle_center) / (self.paddle_width/2) * 60
            
            speed = (self.ball_speed_x**2 + self.ball_speed_y**2)**0.5
            self.ball_speed_x = speed * math.sin(math.radians(angle))
            self.ball_speed_y = -speed * math.cos(math.radians(angle))
        
        # Brick collisions
        for brick in self.bricks[:]:
            brick_pos = self.canvas.coords(brick)
            if (ball_pos[2] >= brick_pos[0] and
                ball_pos[0] <= brick_pos[2] and
                ball_pos[3] >= brick_pos[1] and
                ball_pos[1] <= brick_pos[3]):
                
                self.ball_speed_y = -self.ball_speed_y
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                
                if not self.bricks:
                    self.game_over("You Win!")
                break
    
    def game_loop(self):
        if self.game_started:
            self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
            self.check_collision()
            
            # Check if ball is below paddle
            if self.canvas.coords(self.ball)[1] > 600:
                self.game_over("Game Over!")
                return
        
        self.window.after(16, self.game_loop)
    
    def game_over(self, message):
        self.game_started = False
        self.canvas.create_text(
            300, 300,
            text=message,
            font=("Arial", 30, "bold"),
            fill="white"
        )

class SlidingPuzzleGame:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Sliding Puzzle")
        self.window.geometry("400x500")
        self.window.configure(bg="#2c3e50")
        
        self.setup_game()
        
    def setup_game(self):
        # Control frame
        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=10)
        
        self.moves = 0
        self.moves_label = ttk.Label(
            control_frame,
            text=f"Moves: {self.moves}",
            font=("Arial", 14)
        )
        self.moves_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            control_frame,
            text="New Game",
            command=self.new_game
        ).pack(side=tk.LEFT, padx=10)
        
        # Game canvas
        self.tile_size = 90
        self.canvas = tk.Canvas(
            self.window,
            width=self.tile_size * 3,
            height=self.tile_size * 3,
            bg="#34495e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        self.canvas.bind('<Button-1>', self.click_tile)
        
        self.new_game()
        
    def new_game(self):
        self.moves = 0
        self.moves_label.config(text=f"Moves: {self.moves}")
        
        # Create tiles
        self.tiles = list(range(9))  # 0 represents empty tile
        random.shuffle(self.tiles)
        
        # Make sure puzzle is solvable
        while not self.is_solvable():
            random.shuffle(self.tiles)
        
        self.draw_board()
    
    def is_solvable(self):
        inversions = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if self.tiles[i] != 0 and self.tiles[j] != 0:
                    if self.tiles[i] > self.tiles[j]:
                        inversions += 1
        
        empty_row = self.tiles.index(0) // 3
        return (inversions + empty_row) % 2 == 0
    
    def draw_board(self):
        self.canvas.delete("all")
        for i in range(9):
            row = i // 3
            col = i % 3
            tile = self.tiles[i]
            
            if tile:  # Don't draw empty tile
                x1 = col * self.tile_size
                y1 = row * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#3498db",
                    outline="white"
                )
                
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=str(tile),
                    font=("Arial", 24, "bold"),
                    fill="white"
                )
    
    def click_tile(self, event):
        col = event.x // self.tile_size
        row = event.y // self.tile_size
        tile_index = row * 3 + col
        
        empty_index = self.tiles.index(0)
        empty_row = empty_index // 3
        empty_col = empty_index % 3
        
        # Check if clicked tile is adjacent to empty space
        if ((abs(row - empty_row) == 1 and col == empty_col) or
            (abs(col - empty_col) == 1 and row == empty_row)):
            # Swap tiles
            self.tiles[tile_index], self.tiles[empty_index] = \
                self.tiles[empty_index], self.tiles[tile_index]
            
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            
            self.draw_board()
            
            # Check for win
            if self.tiles == list(range(9)):
                self.canvas.create_text(
                    self.tile_size * 1.5,
                    self.tile_size * 1.5,
                    text="You Win!",
                    font=("Arial", 24, "bold"),
                    fill="#2ecc71"
                )
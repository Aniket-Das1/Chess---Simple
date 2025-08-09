import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import chess
import chess.engine
import pygame

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# --- Config ---
TILE_SIZE = 64
BOARD_COLOR = [ "white","darkgray"]
STOCKFISH_PATH = "D:/stockfish/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"
PIECE_FOLDER = "Pieces"

# Function to get the rating from the user
def get_rating(root):
    rating_window = tk.Toplevel(root)
    rating_window.title("Enter Rating")
   
    label_font = ("Arial", 14, "italic")
    entry_font = ("Arial", 12)
     # Replace with your image path
    

    # Calculate position to center the window
   

    # Set the position of the window
    rating_window.state("zoomed")
    screen_width = rating_window.winfo_screenwidth()
    screen_height = rating_window.winfo_screenheight()

# Load and resize background image
    bg_image = Image.open("D:\stockfish\Achess\wp11840974.png")  # Replace with your actual file
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_image1 = Image.open("D:\stockfish\Achess\wp11840974.png")  # Replace with your actual file
    bg_image1 = bg_image1.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo1 = ImageTk.PhotoImage(bg_image1)

# Place the background FIRSTC:\Users\DELL\Desktop\PROJECTS\Achess\wp11840974.png
    bg_label1 = tk.Label(root, image=bg_photo1)
    
    bg_label1.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label = tk.Label(rating_window, image=bg_photo)
    
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    rating_window.bind("<Escape>", lambda e: rating_window.attributes("-fullscreen", False))
    # Label for rating input
    rating_label = tk.Label(rating_window, text="Enter your rating (Minimum rating: 1320 Maximum rating: 3190):",font=label_font, bg="#f9f9f9", fg="#333")
    rating_label.pack(pady=10)

    rating_var = tk.StringVar()
    rating_entry = tk.Entry(rating_window, textvariable=rating_var,font=entry_font, bd=1, relief="solid", highlightthickness=1, highlightcolor="#555")
    rating_entry.pack(pady=5, ipadx=10, ipady=5)

    # Function to close the rating input window and start the game
    def submit_rating():
        rating = rating_var.get()
        try:
            rating = int(rating)
            if 1320 <= rating <= 3190:
                rating_window.destroy()  # Close the rating window
                start_game(root, rating)  # Start the game with the rating
            else:
                messagebox.showerror("Invalid Rating", "Rating must be between 1320 and 3190.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer rating.")

    # Submit button
    submit_button = tk.Button(rating_window, text="Submit", command=submit_rating)
    submit_button.pack(pady=20)

    rating_window.mainloop()


# Function to start the game after getting the rating
def start_game(root, rating):
    global engine
    board = chess.Board()
    pygame.init()
    pygame.mixer.init()

    # Load sounds
    move_sound = pygame.mixer.Sound('D:/stockfish/Achess/Chess_sound/mixkit-twig-breaking-2945.mp3')
    check_sound = pygame.mixer.Sound('D:/stockfish/Achess/Chess_sound/check_sound.mp3')

    # Load Pygame window (used only for promotion menu)
    #screen=""
   
    # Load piece images
    piece_images = {}
    for color in ["w", "b"]:
        for piece in ["P", "N", "B", "R", "Q", "K"]:
            img_path = f"{PIECE_FOLDER}/{color}{piece}.png"
            piece_images[color + piece] = pygame.image.load(img_path)

    # Start Stockfish
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": rating})

    class ChessGUI:
        
            


        def __init__(self, root):
            self.playing_as_white = True
            self.root = root
            self.root.title("Chess Game")
            self.board = chess.Board()
            self.canvas = tk.Canvas(root, width=8 * TILE_SIZE, height=8 * TILE_SIZE)
            self.canvas.place(relx=0.5, rely=0.5, anchor="center")
            #self.canvas.pack()
            self.play_as_black = False
            self.flip_board = False  #
            self.button_black = tk.Button(root, text="Play as black", command=self.start_as_black, bg="white", fg="red", font=("Tangerine", 14))
            #self.resign_button.pack(pady=10)
            self.button_black.place(relx=0.75, rely=0.3, anchor="center")
            # Resign button
            self.resign_button = tk.Button(root, text="Resign", command=self.on_resign, bg="white", fg="red", font=("Tangerine", 14))
            #self.resign_button.pack(pady=10)
            self.resign_button.place(relx=0.75, rely=0.5, anchor="center")
            self.restart_button = tk.Button(root, text="Restart", command=self.on_restart, bg="white", fg="red", font=("Tangerine", 14))
            #self.resign_button.pack(pady=10)
            self.restart_button.place(relx=0.75, rely=0.4, anchor="center")
            self.images = {}
            self.selected = None
            
            self.draw_board()
            
            self.canvas.bind("<Button-1>", self.on_click)


        def start_as_black(self):
            self.playing_as_white = False
            self.play_as_black = True
            self.flip_board = True  # Rotate the board for Black
            board.reset()
            
            self.make_engine_move() 
            self.canvas.bind("<Button-1>", self.on_clickb)
             # Engine plays first move as White
            

        def make_engine_move(self):
                  
                self.root.after(300, self.bot_move)
                
                
                 

        def update_board(self):
            self.canvas.delete("all")
            
            for row in range(8):
                for col in range(8):
                    # Determine square color: alternate based on row+col
                    color = BOARD_COLOR[(row + col) % 2]
                    
                    # Flip the row and column for Black's perspective
                    x1 = col * TILE_SIZE
                    y1 = row * TILE_SIZE
                    self.canvas.create_rectangle(x1, y1, x1 + TILE_SIZE, y1 + TILE_SIZE, fill=color)

                    # For Black's perspective, we need to reverse the ranks and files
                    flipped_row = 7 - row  # Flip the row for Black's view
                    flipped_col = 7 - col  # Flip the column for Black's view
                    
                    piece = board.piece_at(chess.square(flipped_col, flipped_row))  # Use flipped coordinates
                    if piece:
                        name = piece.symbol()
                        img_name = f"{'b' if name.isupper() else 'w'}{name.upper()}.png"
                        
                        # Check if the image for this piece is already loaded
                        if img_name not in self.images:
                            img = Image.open(f"{PIECE_FOLDER}/{img_name}")
                            img = img.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)
                            self.images[img_name] = ImageTk.PhotoImage(img)
                        
                        # Place the piece image on the board
                        self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.images[img_name])
                
        def draw_board(self):
            self.canvas.delete("all")
            for row in range(8):
                for col in range(8):
                    color = BOARD_COLOR[(row + col) % 2]
                    x1 = col * TILE_SIZE
                    y1 = row * TILE_SIZE
                    self.canvas.create_rectangle(x1, y1, x1 + TILE_SIZE, y1 + TILE_SIZE, fill=color)

                    piece = board.piece_at(chess.square(col, 7 - row))
                    if piece:
                        name = piece.symbol()
                        img_name = f"{'w' if name.isupper() else 'b'}{name.upper()}.png"
                        if img_name not in self.images:
                            img = Image.open(f"{PIECE_FOLDER}/{img_name}")
                            img = img.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)
                            self.images[img_name] = ImageTk.PhotoImage(img)
                        self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.images[img_name])

        def on_restart(self):
            board.reset() 
            self.draw_board()
        def on_resign(self):
            messagebox.showinfo( "","Game Over")
            self.root.quit()

        def show_promotion_menu(self, color):
            WIDTH, HEIGHT = 320, 320
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Promotion Menu")
            options = ["Q", "R", "B", "N"]
            selected_piece = None
            square_size = WIDTH // 8

            running = True
            while running:
                screen.fill((230, 230, 230))
                for i, piece_letter in enumerate(options):
                    piece_code = color + piece_letter
                    img = piece_images[piece_code]
                    rect = pygame.Rect(square_size * i + 64, 192, square_size, square_size)
                    screen.blit(pygame.transform.scale(img, (square_size, square_size)), rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for i in range(4):
                            rect = pygame.Rect(square_size * i + 64, 192, square_size, square_size)
                            if rect.collidepoint(x, y):
                                selected_piece = color + options[i]
                                running = False
                                break

            return selected_piece
        
        def on_clickb(self, event):
            # Don't allow user to move if it's the bot's turn
        

            col = event.x // TILE_SIZE
            row = 7 - (event.y // TILE_SIZE)
            square = chess.square(col, row)

            if self.selected is None:
                piece = board.piece_at(square)
                if piece and piece.color == chess.BLACK:
                    self.selected = square
            else:
                piece = board.piece_at(self.selected)

                if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                    selected_piece_code = self.show_promotion_menu("b" if board.turn == chess.BLACK else "w")
                    if selected_piece_code:
                        promotion_map = {'Q': chess.QUEEN, 'R': chess.ROOK, 'B': chess.BISHOP, 'N': chess.KNIGHT}
                        promo_type = promotion_map[selected_piece_code[1]]
                        move = chess.Move(self.selected, square, promotion=promo_type)
                    else:
                        move = chess.Move(self.selected, square)
                else:
                    move = chess.Move(self.selected, square)

                if move in board.legal_moves:
                    board.push(move)

                    if board.is_check():
                        check_sound.play()
                    else:
                        move_sound.play()

                    self.selected = None
                    self.draw_board()

                    # Call bot move only if game is not over
                    if not board.is_game_over():
                        self.root.after(200, self.bot_move)
                else:
                    self.selected = None

            if board.is_game_over():
                self.show_game_over_message()

        def on_click(self, event):
            col = event.x // TILE_SIZE
            row = 7 - (event.y // TILE_SIZE)
            square = chess.square(col, row)

            if self.selected is None:
                piece = board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    self.selected = square
            else:
                piece = board.piece_at(self.selected)

                # Check for promotion
                if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) == 7:
                    
                    selected_piece_code = self.show_promotion_menu("w")
                    if selected_piece_code:
                        promotion_map = {'Q': chess.QUEEN, 'R': chess.ROOK, 'B': chess.BISHOP, 'N': chess.KNIGHT}
                        promo_type = promotion_map[selected_piece_code[1]]
                        move = chess.Move(self.selected, square, promotion=promo_type)
                    else:
                        move = chess.Move(self.selected, square)
                else:
                    move = chess.Move(self.selected, square)

                if move in board.legal_moves:
                    board.push(move)

                    if board.is_check():
                        check_sound.play()
                    else:
                        move_sound.play()

                    self.selected = None
                    self.draw_board()
                    self.root.after(500, self.bot_move)
                else:
                    self.selected = None

            # Check for game over
            if board.is_game_over():
                self.show_game_over_message()

        def show_game_over_message(self):
            if board.is_checkmate():
                messagebox.showinfo("Game Over", "Checkmate!" if board.turn else "Checkmate! You won the game.")
            elif board.is_stalemate():
                messagebox.showinfo("Game Over", "Stalemate! ")
            elif board.is_insufficient_material():
                messagebox.showinfo("Game Over", "Insufficient material!")
            elif board.is_seventyfive_moves():
                messagebox.showinfo("Game Over", "75-move rule! The game is a draw.")
            elif board.is_variant_draw():
                messagebox.showinfo("Game Over", "Variant draw! The game is a draw.")
            else:
                messagebox.showinfo("Game Over", "Game Over! It's a draw.")

            self.root.quit()

        def bot_move(self):
            if board.is_game_over():
                return
            if self.play_as_black:
                board.turn == chess.BLACK
            result = engine.play(board, chess.engine.Limit(time=0.5))
            move = result.move

            # Handle bot promotion
            if board.piece_at(move.from_square).piece_type == chess.PAWN and chess.square_rank(move.to_square) == 0:
                move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)

            board.push(move)

            if board.is_check():
                check_sound.play()
            else:
                move_sound.play()
            
            self.draw_board()

            # Check for game over after bot move
            if board.is_game_over():
                self.show_game_over_message()


    # --- Launch GUI ---
    gui = ChessGUI(root)
    
    #win_width = 800
    #win_height = 800
    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()
    #x = (screen_width // 2) - (win_width // 2)
    #y = (screen_height // 2) - (win_height // 2)
    #root.geometry(f"{win_width}x{win_height}+{x}+{y}")
    root.state("zoomed")
    # --- Start the Tkinter main loop ---
    root.deiconify()  # Show the root window again
    root.mainloop()

    # --- Clean up ---
    engine.quit()


# Start rating input window (this is the first window to appear)
root = tk.Tk()
root.withdraw()  # Hide the root window while the rating window is open
get_rating(root)  # Start the rating window

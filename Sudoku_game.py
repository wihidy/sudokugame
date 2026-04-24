import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading

class SudokuEngine:
    
    @staticmethod
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num:
                return False
        for x in range(9):
            if board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(board, r, c, num):
                            board[r][c] = num
                            if self.solve(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    def generate_puzzle(self, difficulty='Easy'):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(board)
        
        clues_target = {'Easy': 40, 'Medium': 30, 'Hard': 24}.get(difficulty, 40)
        puzzle = [row[:] for row in board]
        attempts = 81 - clues_target
        
        while attempts > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if puzzle[r][c] != 0:
                puzzle[r][c] = 0
                attempts -= 1
        
        return puzzle, board

class SudokuGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Expert - Desktop Edition")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        
        self.engine = SudokuEngine()
        self.selected_cell = None
        self.is_solving_visual = False
        
        self.original_board = []
        self.current_board = []
        self.solution_board = []
        self.timer_seconds = 0
        self.move_count = 0
        self.timer_running = False
        
        self.setup_styles()
        self.create_widgets()
        self.new_game('Easy')
        self.update_timer_loop()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))

    def create_widgets(self):
        info_frame = tk.Frame(self.root, pady=10)
        info_frame.pack(fill='x')
        
        self.lbl_timer = tk.Label(info_frame, text="Time: 00:00", font=("Arial", 12))
        self.lbl_timer.pack(side='left', padx=20)
        
        self.lbl_moves = tk.Label(info_frame, text="Moves: 0", font=("Arial", 12))
        self.lbl_moves.pack(side='left', padx=20)
        
        self.diff_var = tk.StringVar(value='Easy')
        diff_menu = ttk.Combobox(info_frame, textvariable=self.diff_var, values=['Easy', 'Medium', 'Hard'], width=8, state='readonly')
        diff_menu.pack(side='right', padx=20)
        
        self.grid_frame = tk.Frame(self.root, bg="black", bd=2)
        self.grid_frame.pack(padx=20, pady=10)
        
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                padx = (3 if c % 3 == 0 and c != 0 else 1, 1)
                pady = (3 if r % 3 == 0 and r != 0 else 1, 1)
                
                cell_frame = tk.Frame(self.grid_frame, bg="white")
                cell_frame.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")
                
                lbl = tk.Label(cell_frame, text="", font=("Arial", 18, "bold"), 
                              width=2, height=1, bg="white", cursor="hand2")
                lbl.pack(expand=True, fill='both')
                lbl.bind("<Button-1>", lambda e, row=r, col=c: self.select_cell(row, col))
                self.cells[r][c] = lbl

        self.root.bind("<Key>", self.handle_keypress)

        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="New Game", command=lambda: self.new_game(self.diff_var.get()), width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Reset Board", command=self.reset_board, width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Check Solution", command=self.check_solution, width=12).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(btn_frame, text="Hint", command=self.give_hint, width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Visual Solve", command=self.start_visual_solve, width=12, bg="#e1f5fe").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear Cell", command=lambda: self.handle_keypress(type('obj', (object,), {'keysym': 'BackSpace'})), width=12).grid(row=1, column=2, padx=5, pady=5)

    def select_cell(self, r, c):
        if self.is_solving_visual: return
        
        if self.selected_cell:
            old_r, old_c = self.selected_cell
            self.update_cell_color(old_r, old_c)
            
        self.selected_cell = (r, c)
        self.cells[r][c].config(bg="#bbdefb")

    def handle_keypress(self, event):
        if not self.selected_cell or self.is_solving_visual: return
        r, c = self.selected_cell
        if self.original_board[r][c] != 0: return
        
        key = event.keysym
        if key in [str(i) for i in range(1, 10)]:
            val = int(key)
            self.current_board[r][c] = val
            self.cells[r][c].config(text=str(val), fg="#1a237e")
            self.move_count += 1
            self.lbl_moves.config(text=f"Moves: {self.move_count}")
            if not self.timer_running: self.timer_running = True
        elif key in ["BackSpace", "Delete", "0"]:
            self.current_board[r][c] = 0
            self.cells[r][c].config(text="")
        
        self.update_cell_color(r, c)

    def update_cell_color(self, r, c):
        if self.original_board[r][c] != 0:
            self.cells[r][c].config(bg="#f5f5f5", fg="black")
        elif (r, c) == self.selected_cell:
            self.cells[r][c].config(bg="#bbdefb")
        else:
            self.cells[r][c].config(bg="white")

    def new_game(self, difficulty):
        if self.is_solving_visual: return
        self.original_board, self.solution_board = self.engine.generate_puzzle(difficulty)
        self.current_board = [row[:] for row in self.original_board]
        self.selected_cell = None
        self.move_count = 0
        self.timer_seconds = 0
        self.timer_running = False
        self.lbl_moves.config(text="Moves: 0")
        self.lbl_timer.config(text="Time: 00:00")
        
        for r in range(9):
            for c in range(9):
                val = self.original_board[r][c]
                self.cells[r][c].config(text=str(val) if val != 0 else "", bg="white")
                self.update_cell_color(r, c)

    def reset_board(self):
        if self.is_solving_visual: return
        self.current_board = [row[:] for row in self.original_board]
        for r in range(9):
            for c in range(9):
                val = self.original_board[r][c]
                self.cells[r][c].config(text=str(val) if val != 0 else "", bg="white")
                self.update_cell_color(r, c)
        self.move_count = 0
        self.lbl_moves.config(text="Moves: 0")

    def check_solution(self):
        if self.is_solving_visual: return
        is_complete = True
        for r in range(9):
            for c in range(9):
                val = self.current_board[r][c]
                if val == 0:
                    is_complete = False
                    continue
                if val == self.solution_board[r][c]:
                    if self.original_board[r][c] == 0:
                        self.cells[r][c].config(bg="#c8e6c9")
                else:
                    self.cells[r][c].config(bg="#ffcdd2")
        
        if is_complete and self.current_board == self.solution_board:
            self.timer_running = False
            messagebox.showinfo("Sudoku", f"Congratulations! You solved it in {self.lbl_timer.cget('text')}!")

    def give_hint(self):
        if self.is_solving_visual: return
        empty_cells = [(r, c) for r in range(9) for c in range(9) if self.current_board[r][c] == 0]
        if not empty_cells: return
        
        r, c = random.choice(empty_cells)
        val = self.solution_board[r][c]
        self.current_board[r][c] = val
        self.cells[r][c].config(text=str(val), fg="#4caf50", bg="#e8f5e9")
        self.root.after(1000, lambda: self.update_cell_color(r, c))

    def update_timer_loop(self):
        if self.timer_running:
            self.timer_seconds += 1
            mins, secs = divmod(self.timer_seconds, 60)
            self.lbl_timer.config(text=f"Time: {mins:02d}:{secs:02d}")
        self.root.after(1000, self.update_timer_loop)

    def start_visual_solve(self):
        if self.is_solving_visual: return
        if not messagebox.askyesno("Visual Solve", "Watch the backtracking algorithm solve the puzzle?"):
            return
            
        self.is_solving_visual = True
        self.timer_running = False
        self.reset_board()
        
        threading.Thread(target=self.run_visual_solve, daemon=True).start()

    def run_visual_solve(self):
        temp_board = [row[:] for row in self.original_board]
        self._visual_backtrack(temp_board, 0, 0)
        self.is_solving_visual = False

    def _visual_backtrack(self, board, r, c):
        if c == 9:
            r += 1
            c = 0
            if r == 9: return True
            
        if board[r][c] != 0:
            return self._visual_backtrack(board, r, c + 1)
            
        for num in range(1, 10):
            if self.engine.is_valid(board, r, c, num):
                board[r][c] = num
                self.root.after(0, lambda r=r, c=c, n=num: self._gui_update_solve(r, c, n, "#fff9c4"))
                time.sleep(0.02)
                
                if self._visual_backtrack(board, r, c + 1):
                    return True
                
                board[r][c] = 0
                self.root.after(0, lambda r=r, c=c: self._gui_update_solve(r, c, "", "#ffcdd2"))
                time.sleep(0.01)
                
        return False

    def _gui_update_solve(self, r, c, val, color):
        self.cells[r][c].config(text=str(val), bg=color)
        if val == "":
            self.root.after(100, lambda: self.cells[r][c].config(bg="white"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

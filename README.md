# AI Sudoku Game

> A GUI-based Sudoku game with an integrated AI solver built using Python and Tkinter.

**Made by**
- Abdullah Mohamed Abdullah Mohamed Ibrahim (Section 5)
- Ahmed Assem Al-Waheidi (Section 1)

**Supervised by**
- Dr. Sara El-Sayed El-Metwally
- Eng. Mai Mohamed

---

## Project Overview

This project is a GUI-based Sudoku game built using Python and Tkinter. It allows users to play Sudoku interactively while integrating an AI solver based on backtracking. The system can generate puzzles, provide hints, check solutions, and visually demonstrate how the AI solves the puzzle.

---

## Algorithm — Backtracking

1. Find an empty cell in the grid.
2. Try numbers from 1 to 9 randomly.
3. Check if the number is valid (row, column, box).
4. If valid, place it and move to the next cell.
5. If no valid number works, backtrack and try another.

---

## Requirements

- Python 3.x installed on your system.
- Tkinter library (comes pre-installed with most Python versions).
- A computer capable of running Python GUI applications.

---

## How to Run

1. Install Python from [python.org](https://www.python.org) if not already installed.
2. Make sure Tkinter is available (included by default with Python).
3. Download or clone the project files.
4. Open a terminal or command prompt in the project folder.
5. Run the following command:

```bash
python sudoku.py
```

---

## How to Use

| Action | Description |
|---|---|
| **New Game** | Start a new puzzle |
| **Select a cell + keyboard** | Enter numbers manually |
| **Hint** | Fill in a correct value for the selected cell |
| **Check Solution** | Validate your current answers |
| **Visual Solve** | Watch the AI solve the puzzle step-by-step |
| **Reset Board** | Restart the current puzzle |

---

## References

- [Sudoku — Wikipedia](https://en.wikipedia.org/wiki/Sudoku)
- [Backtracking — Wikipedia](https://en.wikipedia.org/wiki/Backtracking)

'''Written by Austin O'Quinn'''
import tkinter as tk
import random

class RAM:
    def __init__(self, master, rows, cols, update_frequency, flip_probability=0, file=""):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.update_frequency = update_frequency
        self.flip_probability = flip_probability
        self.view_mode = tk.StringVar(value="binary")

        # Initialize the data and charges
        if(file==""):
            self.data = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
            self.charges = [[5 if bit == 1 else 0 for bit in row] for row in self.data]
        else:
            #read from file
            pass

        self.cells = []
        self.input_frames = []
        self.entry_widgets = []

        # Toggle button to switch view between binary and voltage
        self.toggle_button = tk.Button(self.master, text="Switch to Voltages", command=self.toggle_view)
        self.toggle_button.pack(side=tk.TOP, pady=10)

        for i in range(self.rows):
            row_frame = tk.Frame(self.master, pady=5)  # Padding for space between rows
            row_frame.pack(side=tk.TOP, fill=tk.X)

            # UI for each row's entry and submit button
            input_frame = tk.Frame(row_frame)
            input_frame.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=2)

            current_row_binary = ''.join(str(bit) for bit in self.data[i])
            entry = tk.Entry(input_frame, width=20)
            entry.insert(0, current_row_binary)
            entry.pack(side=tk.LEFT)

            submit_button = tk.Button(input_frame, text="Submit", command=lambda i=i, entry=entry: self.update_row(i, entry.get()))
            submit_button.pack(side=tk.LEFT)

            self.input_frames.append(input_frame)
            self.entry_widgets.append(entry)

            row = []
            for j in range(self.cols):
                cell_frame = tk.Frame(row_frame, bg="white", highlightbackground="black", highlightthickness=1, width=50, height=50)
                cell_frame.pack(side=tk.LEFT)
                cell_label = tk.Label(cell_frame, text=str(self.data[i][j]), font=("Helvetica", 16), bg="white", width=3, height=2)
                cell_label.pack()
                row.append(cell_label)
            self.cells.append(row)

        self.redraw()

    def toggle_view(self):
        """Toggle between binary and voltage view."""
        if self.view_mode.get() == "binary":
            self.view_mode.set("voltage")
            self.toggle_button.config(text="Switch to Binary")
        else:
            self.view_mode.set("binary")
            self.toggle_button.config(text="Switch to Voltages")
        self.redraw()

    def redraw(self):
        """Redraw the RAM cells based on self.data and self.charges."""
        for i in range(self.rows):
            for j in range(self.cols):
                cell_label = self.cells[i][j]

                if self.view_mode.get() == "binary":
                    cell_value = '1' if self.charges[i][j] > 2.5 else '0'
                    cell_label.config(text=cell_value, bg="white")
                else:
                    # Show the actual voltage value
                    cell_label.config(text=f"{self.charges[i][j]}V", bg="white")

                cell_label.config(bg="light green" if self.data[i][j] else "light blue")

    def update_row(self, row_index, binary_string):
        """Update a specific row with a new binary string."""
        if not binary_string:
            binary_string = ''.join(str(self.data[row_index][col]) for col in range(self.cols))

        if len(binary_string) != self.cols or any(c not in '01' for c in binary_string):
            print(f"Invalid input: {binary_string}. Please enter a binary string of length {self.cols}.")
            return

        # Update data and charge arrays based on the new string
        for col_index, bit in enumerate(binary_string):
            bit = int(bit)
            self.data[row_index][col_index] = bit
            self.charges[row_index][col_index] = 5 if bit == 1 else 0

        # Adjust the voltage of adjacent cells based on the new values.
        for col_index, bit in enumerate(binary_string):
            bit = int(bit)
            voltage_change = 1 if bit == 1 else -1

            # Apply voltage changes to adjacent cells in other rows
            adjacent_cells = [(row_index-1, col_index), (row_index+1, col_index)]
            for adj_row, adj_col in adjacent_cells:
                if 0 <= adj_row < self.rows:
                    self.charges[adj_row][adj_col] = max(0, min(5, self.charges[adj_row][adj_col] + voltage_change))
                    if self.charges[adj_row][adj_col] == 2.5:
                        self.data[adj_row][adj_col] = random.choice([0, 1])
                    else:
                        self.data[adj_row][adj_col] = 1 if self.charges[adj_row][adj_col] > 2.5 else 0

        self.redraw()

        # After updating and redrawing, set the current data as the new default value in the entry
        current_row_binary = ''.join(str(bit) for bit in self.data[row_index])
        entry_widget = self.entry_widgets[row_index]
        entry_widget.delete(0, tk.END)  # Remove old text
        entry_widget.insert(0, current_row_binary)  # Insert new default text

    def start_voltage_reset_loop(self):
        """Starts the loop that resets the voltage of the cells."""
        # Reset voltages based on the binary values currently interpreted
        self.reset_voltages()

        # Schedule the next reset after 'self.update_frequency' milliseconds
        self.master.after(self.update_frequency, self.start_voltage_reset_loop)

    def reset_voltages(self):
        """Reset the voltage in all cells based on the current binary interpretation."""
        for i in range(self.rows):
            for j in range(self.cols):
                # Reset voltage based on the current interpretation of the data (1 or 0)
                current_bit = 1 if self.charges[i][j] > 2.5 else 0
                self.charges[i][j] = 5 if current_bit == 1 else 0

        # Redraw the grid to reflect the changes
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RAM Simulator")

    # Set your desired 'update_frequency' for the voltage reset in milliseconds.
    # For example, 2000 milliseconds (or 2 seconds) would be:
    updateF=float(input("Enter update freq:"))
    fileToUse=input("Enter File to use or press enter for random ram values:")
    ram = RAM(root, 10, 8, 2000, updateF,fileToUse)

    # Start the voltage resetting loop
    ram.start_voltage_reset_loop()

    root.mainloop()


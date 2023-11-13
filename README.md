# RAM and Rowhammer Visualizer

This Python script provides an interactive visualization of RAM cells and demonstrates how a Rowhammer attack could affect them.

## Features

- Toggle between binary and voltage views.
- Initialize RAM state from a file.
- Set custom RAM refresh frequencies.

## Prerequisites

- Python 3.x

## Quick Start

1. Save the script as `ram_simulator.py`.
2. Run `python ram_simulator.py` in your terminal.
3. Set refresh frequency and optionally initialize from a file when prompted.

## Usage

- Use the "Switch to Voltages/Binary" button to change views.
- Use the "Submit" button next to each row to update RAM cells.
- Initialize RAM from a `.txt` file with binary strings, one per line.

## Customization

Edit the `RAM` instance in the script to change default settings:

```python
ram = RAM(root, num_rows, num_cols, refresh_frequency, bit_flip_prob, init_file=None)

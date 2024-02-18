import pygame
import sys
from tkinter import Tk, Label, Button, Text, Entry, END, messagebox
import re
import threading
import time

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("While Loop Simulator")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Function to visualize the while loop on the Pygame screen
def visualize_while_loop(variable_name, variable_value, comparison_operator, target_value):
    screen.fill(white)

    # Draw the while loop information on the screen
    not_finished = True 

    if variable_value -1 < target_value:
        not_finished = False

    font = pygame.font.Font(None, 96)
    while_loop_text = font.render(f"While {variable_name} {comparison_operator} {target_value}: {not_finished} " , True, (255,0,0))
    screen.blit(while_loop_text, (170, 40))

    # Draw the counter value under the while loop
    counter_text = font.render(f"print({variable_name}) = {variable_value}", True, (0,0,255))
    screen.blit(counter_text, (260, 130))

    # Draw the decrement statement under the while loop
    decrement_text = font.render(f"{variable_name} -= {increment_value}", True, (255,255,0))
    screen.blit(decrement_text, (260, 220))

    # Update display
    pygame.display.flip()

# Function to handle button click and run the while loop
def run_while_loop():
    initial_counter_input = initial_counter_entry.get()
    while_condition_str = while_text.get("1.0", END).strip()
    decrement_operator_str = decrement_entry.get("1.0", END).strip()

    # Validate the input format
    if not validate_input_format(while_condition_str):
        messagebox.showerror("Validation Error", "Invalid input format. Please use 'while counter > 10:' or 'while counter >= 10:' format.")
        return

    # Extract the input number and comparison operator from the while loop condition using regex
    match = re.search(r"counter\s*(>|>=|==|!=)\s*(\d+)", while_condition_str)
    if match:
        global comparison_operator, target_value
        comparison_operator = match.group(1)
        target_value = int(match.group(2))
    else:
        messagebox.showerror("Validation Error", "Invalid while loop condition. Please use 'while counter > 10:' or 'while counter >= 10:' format.")
        return

    # Validate the decrement operator format
    if not validate_decrement_format(decrement_operator_str):
        messagebox.showerror("Validation Error", "Invalid decrement operator format. Please use 'counter -= 1' or 'counter -= 2' format.")
        return

    # Extract the decrement value using regex
    match_decrement = re.search(r"counter\s*-=\s*(\d+)", decrement_operator_str)
    if match_decrement:
        global increment_value
        increment_value = int(match_decrement.group(1))
    else:
        messagebox.showerror("Validation Error", "Invalid decrement operator. Please use 'counter -= 1' or 'counter -= 2' format.")
        return

    # Initialize the counter variable
    variables = {}
    try:
        exec(initial_counter_input, None, variables)
    except Exception as e:
        messagebox.showerror("Validation Error", f"Invalid initial counter input: {str(e)}")
        return

    counter = variables.get("counter", 0)

    # Function to run the while loop in a separate thread
    def run_while_loop_thread():
        nonlocal counter
        visualize_while_loop("counter", counter, comparison_operator, target_value)
        time.sleep(1)  # Delay for one second before the first loop or increase
        while eval(f"counter {comparison_operator} target_value"):
            exec(decrement_operator_str, None, variables)
            counter = variables.get("counter", 0)
            visualize_while_loop("counter", counter, comparison_operator, target_value)
            time.sleep(2)
        

    # Create a thread and start the while loop
    thread = threading.Thread(target=run_while_loop_thread)
    thread.start()

    result_label.config(text="While loop executed successfully.", fg=blue)

# Function to validate the input format
def validate_input_format(input_str):
    pattern = re.compile(r"while\s+counter\s*(>|>=|==|!=)\s*\d+:")
    return bool(pattern.match(input_str))

# Function to validate the decrement operator format
def validate_decrement_format(decrement_str):
    pattern = re.compile(r"counter\s*-=\s*\d+")
    return bool(pattern.match(decrement_str))

# Create Tkinter window
root = Tk()
root.title("While Loop Simulator GUI")

# Label and input field for initial counter variable and value
initial_counter_label = Label(root, text="Initial Counter Input (e.g., counter = 10):", font=("Arial", 16))
initial_counter_label.pack()

initial_counter_entry = Entry(root, font=("Arial", 16), width=40)
initial_counter_entry.pack()

# Labels and input fields
while_label = Label(root, text="While loop condition (e.g., 'while counter > 10:'):", font=("Arial", 20))
while_label.pack()

# Use Text for multiline input
while_text = Text(root, font=("Arial", 16), width=40, height=3)
while_text.pack()

decrement_label = Label(root, text="Decrement operator (e.g., 'counter -= 1'):", font=("Arial", 20))
decrement_label.pack()

decrement_entry = Text(root, font=("Arial", 16), width=26, height=1)
decrement_entry.pack()

# Button to run the while loop
run_while_button = Button(root, text="Run While Loop", command=run_while_loop, font=("Arial", 16))
run_while_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window
root.geometry("800x400+350+350")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update Tkinter window
    root.update_idletasks()
    root.update()

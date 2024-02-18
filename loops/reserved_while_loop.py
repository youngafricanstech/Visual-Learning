import pygame
import sys
from tkinter import Tk, Label, Button, Text, END
import time

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("While Loop Simulator")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Function to handle button click and run the while loop
def run_while_loop():
    while_condition_str = while_text.get("1.0", END).strip()
    increment_operator_str = increment_entry.get("1.0", END).strip()

    # Initialize the counter variable
    counter = 0

    # Create a while loop code block
    code_block = f"counter = 0\nwhile {while_condition_str}:\n\t{increment_operator_str}"

    try:
        # Execute the while loop with the provided input
        exec(code_block, globals(), locals())
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg=red)
        return

    # Visualize the while loop on the Pygame screen
    visualize_while_loop(counter)

    result_label.config(text="While loop executed successfully.", fg=blue)

# Function to visualize the while loop on the Pygame screen
def visualize_while_loop(counter):
    screen.fill(white)

    # Draw the while loop information on the screen
    font = pygame.font.Font(None, 36)
    while_loop_text = font.render(f"While counter < 20:", True, (0, 0, 0))
    screen.blit(while_loop_text, (50, 100))

    # Draw the increment statement under the while loop
    increment_text = font.render("counter += 1", True, (0, 0, 0))
    screen.blit(increment_text, (50, 150))

    # Draw the counter value under the while loop
    counter_text = font.render(f"print(counter) = {counter}", True, (0, 0, 0))
    screen.blit(counter_text, (50, 200))

    # Update display
    pygame.display.flip()

# Create Tkinter window
root = Tk()
root.title("While Loop Simulator GUI")

# Labels and input fields
while_label = Label(root, text="While loop condition:", font=("Arial", 20))
while_label.pack()

# Use Text for multiline input
while_text = Text(root, font=("Arial", 16), width=40, height=3)
while_text.insert(END, "counter < 20")
while_text.pack()

increment_label = Label(root, text="Increment operator:", font=("Arial", 20))
increment_label.pack()

increment_entry = Text(root, font=("Arial", 16), width=40, height=1)
increment_entry.insert(END, "counter += 1")
increment_entry.pack()

# Button to run the while loop
run_while_button = Button(root, text="Run While Loop", command=run_while_loop, font=("Arial", 16))
run_while_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window
root.geometry("600x400+350+350")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update Tkinter window
    root.update_idletasks()
    root.update()

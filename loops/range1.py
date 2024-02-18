import pygame
import sys
import time
import tkinter as tk
from tkinter import Tk, Label, Entry, Button
import re 

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1100, 800
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Python Range")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 100)

# Animation control variables
start_time = time.time()
animation_duration = 2.0
loop_count = 0

# User input for range in for loop
root = Tk()
root.title("Input")
root.geometry("900x400")  # Set the size of the window

# Label for instructions
label = Label(root, text="Enter the for loop range (e.g., 'for number in range(20):'):", font=('Arial', 18))
label.pack()

# Entry widget for user input with increased width and height
entry = Entry(root, font=('Arial', 18), width=60, bd=5, relief=tk.GROOVE)
entry.pack()

# Function to get user input and close the window
def get_user_input():
    global user_input
    user_input = entry.get()
    root.destroy()

# Button to submit user input
submit_button = Button(root, text="Submit", command=get_user_input, font=('Arial', 18))
submit_button.pack()

root.mainloop()

# Extract variable name and range from user input using regular expressions
pattern = re.compile(r'for (\w+) in range\((\d+)\):')
match = pattern.match(user_input)

try:
    if match:
        groups = match.groups()
        variable_name = groups[0]
        loop_duration = int(groups[1])
    else:
        raise ValueError("Invalid input format.")
except Exception as e:
    print(f"Error parsing input: {e}")
    sys.exit()

# Main game loop
number = 0
stretch_factor = 1.0
stretch_direction = 1
running = True
delay_started = False

while running and loop_count < loop_duration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the animated "for" text with stretching
    text = f"for {variable_name} in range({number}, {loop_duration}):"
    text_render = bold_font.render(text, True, BLUE)
    screen.blit(text_render, (50, 50))

    # Draw the current number on the screen with color coding
    print_text = f"print({variable_name}) = {number}"
    print_text_render = bold_font.render(print_text, True, BLACK)

    # Split the print text into "print(variable)" and "number"
    variable_index = print_text.find(variable_name)
    screen.blit(print_text_render, (150, 150))
    # Render the "print(variable)" part in blue
    variable_render = bold_font.render(print_text[:7 + variable_index], True, BLUE)
    screen.blit(variable_render, (150, 150))
    # Render the "number" part in red
    number_render = bold_font.render(print_text[7 + variable_index:], True, RED)
    screen.blit(number_render, (150 + variable_render.get_width(), 150))

    # Update the display
    pygame.display.flip()

    # Check if two seconds have passed before updating animation and number
    elapsed_time = time.time() - start_time
    if elapsed_time >= animation_duration:
        start_time = time.time()

        if not delay_started and elapsed_time >= 1.0:
            delay_started = True
            continue

        # Increment the number and wrap around at the specified range limit
        if number < loop_duration:
            number += 1

        # Adjust the stretching factor for animation
        stretch_factor += 0.02 * stretch_direction
        if stretch_factor > 1.5 or stretch_factor < 1.0:
            stretch_direction *= -1

        # Check if the loop reached the specified range limit and stop the animation
        if number == loop_duration:
            stretch_factor = 1.0

        # Check if the loop has completed
        loop_count += 1

    # Control the frame rate
    clock.tick(FPS)

# Wait for a user to close the Pygame window manually
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame and exit the program
pygame.quit()
sys.exit()

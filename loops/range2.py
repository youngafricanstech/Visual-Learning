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
RED = (255, 0, 0)

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Python Range")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 90)

# Animation control variables
start_time = time.time()
animation_duration = 2.0
loop_count = 0
completed = False  # Flag to track if the loop has completed

# User input for range in for loop
root = Tk()
root.title("Input")
root.geometry("900x400")  # Set the size of the window

# Label for instructions
label = Label(root, text="Enter the for loop range (e.g.,'for number in range(2, 20):' or 'for number in range(0, 20, 5):'):", font=('Arial', 16))
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
pattern = re.compile(r'for (\w+) in range\((\d+)(?:, (\d+))?(?:, (\d+))?\):')
match = pattern.match(user_input)

try:
    if match:
        groups = match.groups()
        variable_name = groups[0]
        loop_start = int(groups[1])
        loop_end = int(groups[2]) if groups[2] else loop_start
        step = int(groups[3]) if groups[3] else 1
    else:
        raise ValueError("Invalid input format.")
except Exception as e:
    print(f"Error parsing input: {e}")
    sys.exit()

# Main game loop
number = loop_start
stretch_factor = 1.0
stretch_direction = 1
running = True
first_increase = False  # Flag to track the first increase
waiting_for_quit = False  # Flag to track if waiting for quit event

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting_for_quit = False  # Cancel waiting if quit event occurs
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            waiting_for_quit = True  # Set the flag to wait for quit event

    # Clear the screen
    screen.fill(WHITE)

    # Draw the animated "for" text with stretching for the first argument
    text1 = f"for {variable_name} in range({number}" + (f", {loop_end}" if loop_end != loop_start else "") + (f", {step}" if step != 1 else "") + "):"
    text_render1 = bold_font.render(text1, True, BLACK)
    screen.blit(text_render1, (50, 50))

    # Draw the animated "for" text with stretching for the second argument
    text2 = f"print({variable_name}) = {number}"
    text_render2 = bold_font.render(text2, True, BLACK)
    screen.blit(text_render2, (150, 200))

    # give print(variable_name) black color and give number red color
    variable_index = text2.find(variable_name)
    print_render = bold_font.render(text2[:7 + variable_index], True, BLACK)  # render "print(variable_name)"
    number_render = bold_font.render(text2[7 + variable_index:], True, RED)  # render number
    screen.blit(print_render, (150, 200))
    screen.blit(number_render, (150 + print_render.get_width(), 200))

    # Update the display
    pygame.display.flip()

    # Check if two seconds have passed before updating animation and number
    elapsed_time = time.time() - start_time
    if elapsed_time >= animation_duration:
        start_time = time.time()

        # If it's the first increase, wait for 1.5 seconds before starting the loop
        if not first_increase and elapsed_time >= 1.5:
            first_increase = True
            continue

        # Increment the number based on the step and wrap around at the specified range limit
        number += step
        if number >= loop_end:
            number = loop_start
            completed = True  # Set the completed flag when reaching the end

        # Adjust the stretching factor for animation
        stretch_factor += 0.02 * stretch_direction
        if stretch_factor > 1.5 or stretch_factor < 1.0:
            stretch_direction *= -1

        # Check if the loop reached the specified range limit and stop the animation
        if (number == loop_start or number == loop_end) and completed:
            stretch_factor = 1.0
            waiting_for_quit = True  # Set the flag to wait for quit event
            running = False  # Stop the loop if completed

        # Check if the loop has completed
        loop_count += 1

    # Control the frame rate
    clock.tick(FPS)

# If waiting for quit event, wait until a quit event occurs
while waiting_for_quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_quit = False

# Quit Pygame and exit the program
pygame.quit()
sys.exit()

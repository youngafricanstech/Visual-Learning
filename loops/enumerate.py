import pygame
import sys
import time
import tkinter as tk
from tkinter import Tk, Label, Entry, Button
import ast

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1100, 800
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Python Enumerate")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 60)

# Animation control variables
start_time = time.time()
animation_duration = 2.0
loop_count = 0

# User input for enumerate loop
root = Tk()
root.title("Input")
root.geometry("900x400")  # Set the size of the window

# Label for instructions
label = Label(root, text='Enter the enumerate loop (e.g., \'for index, a in enumerate(["Monday", "Tuesday"]):\', 2):', font=('Arial', 18))
label.pack()

# Entry widget for user input with increased width and height
entry = Entry(root, font=('Arial', 18), width=60, bd=5, relief=tk.GROOVE)
entry.pack()

# Function to get user input and close the window
def get_user_input():
    global user_input
    user_input = entry.get()

    # Extract variable name and sequence from user input using ast module
    try:
        _, for_statement = user_input.split("for", 1)
        _, enumerate_args = for_statement.split("enumerate(", 1)
        args, _ = enumerate_args.split("):", 1)
        args = args.strip().rstrip(',')

        # Check if there is a starting number specified
        if ',' in args:
            try:
                sequence, start = ast.literal_eval(args)
                start = int(start)
                text = f"for index, a in enumerate({sequence}, {start}):"
            except ValueError:
                sequence = ast.literal_eval(args)
                start = 0
                text = f"for index, a in enumerate({sequence}):"
        else:
            sequence = ast.literal_eval(args)
            start = 0
            text = f"for index, a in enumerate({sequence}):"

    except Exception as e:
        print(f"Error parsing input: {e}")
        root.destroy()
        return

    # Main game loop
    index = start
    stretch_factor = 1.0
    stretch_direction = 1
    running = True

    while index < len(sequence) + start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw the animated "for" text with stretching
        text_render = bold_font.render(text, True, BLACK)
        screen.blit(text_render, (50, 50))

        # Draw all indices and values with increased font size
        # Draw all indices and values with different colors
        for i, item in enumerate(sequence, start):
            index_text = pygame.font.Font(None, 48).render(f"{i} : ", True, BLACK)
            item_text = pygame.font.Font(None, 48).render(f"{item}", True, (255, 1, 35))

            screen.blit(index_text, (50, 150 + (i - start) * 60))
            screen.blit(item_text, (50 + index_text.get_width(), 150 + (i - start) * 60))

        # Update the display
        pygame.display.flip()

        # Check if two seconds have passed before updating animation and index
        elapsed_time = time.time() - start_time
        if elapsed_time >= animation_duration:
            start_time = time.time()

            # Increment the index and wrap around at the sequence length
            index += 1

            # Adjust the stretching factor for animation
            stretch_factor += 0.02 * stretch_direction
            if stretch_factor > 1.5 or stretch_factor < 1.0:
                stretch_direction *= -1

            # Check if the loop reached the sequence length and stop the animation
            if index == len(sequence) + start:
                stretch_factor = 1.0

            # Check if the loop has completed
            loop_count += 1

        # Control the frame rate
        clock.tick(FPS)

    # Keep the Tkinter main loop running until manually closed
    root.mainloop()

# Button to submit user input
submit_button = Button(root, text="Submit", command=get_user_input, font=('Arial', 18))
submit_button.pack()

# Start the Tkinter main loop
root.mainloop()

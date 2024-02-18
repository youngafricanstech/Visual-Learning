import pygame
import sys
import time
import ast
import re
import tkinter as tk
from tkinter import Tk, Label, Entry, Button

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
pygame.display.set_caption("Animated Python Range")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 60)

# Animation control variables
start_time = time.time()
animation_duration = 2.0
stretch_factor = 1.0

# User input for two lists
root = Tk()
root.title("Input")
root.geometry("900x400")  # Set the size of the window

# Label for instructions
label = Label(root, text="Enter the lists in the format 'for a, b in zip([item1, item2, ...], [item1, item2, ...]):'", font=('Arial', 18))
label.pack()

# Entry widget for user input with increased width and height
entry_input = Entry(root, font=('Arial', 18), width=60, bd=5, relief=tk.GROOVE)
entry_input.pack()

# Function to get user input and close the window
def get_user_input():
    global user_input
    user_input = entry_input.get()
    root.destroy()

# Button to submit user input
submit_button = Button(root, text="Submit", command=get_user_input, font=('Arial', 18))
submit_button.pack()

root.mainloop()

# Extract variables and lists using regular expressions
match = re.match(r'for\s+([^\s,]+),\s*([^\s,]+)\s+in\s+zip\s*\(\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\):', user_input)
if not match:
    print("Error parsing input. Please follow the correct format.")
    sys.exit()

for_var1, for_var2, list1_str, list2_str = match.groups()

try:
    list1 = ast.literal_eval(list1_str)
    list2 = ast.literal_eval(list2_str)
except Exception as e:
    print(f"Error parsing lists: {e}")
    sys.exit()

# Main game loop
running = True
index = 0
item_index = 0
item_font = pygame.font.Font(None, 48)  # Increased font size for items
item_surfaces = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the animated "for" text with stretching using zip
    elapsed_time = time.time() - start_time
    stretch_duration = 1.0  # Duration for stretching animation
    if elapsed_time < stretch_duration:
        # Stretch the "for" text during the animation duration
        stretch_factor = 1.0 + 0.05 * elapsed_time / stretch_duration
    else:
        stretch_factor = 1.05  # Reduced stretching factor after the animation duration

    text = f"for {for_var1}, {for_var2} in zip([{', '.join(map(str, list1))}], [{', '.join(map(str, list2))}]):"
    text_render = bold_font.render(text, True, (255, 1, 20))

    # Calculate the new width based on the stretch factor
    new_width = int(text_render.get_width() * stretch_factor)
    new_height = int(text_render.get_height())

    # Resize the text surface
    text_render = pygame.transform.scale(text_render, (new_width, new_height))

    # Draw the stretched "for" text
    screen.blit(text_render, (50, 50))

    # Draw the index
    # index_text = font.render(f"Index: {index}", True, BLACK)
    # screen.blit(index_text, (50, 150))

   # Increase the font size by 20
    item_font_size = 58 + 20
    item_font = pygame.font.Font(None, item_font_size)

    # Draw "a" and "b" above the items
    a_text = item_font.render(f"a", True, BLACK)
    b_text = item_font.render(f"b", True, BLACK)

    screen.blit(a_text, (340, 200))
    screen.blit(b_text, (610, 200))

    # Draw the items vertically one by one every two seconds
    if item_index < min(len(list1), len(list2)):
        if time.time() - start_time >= animation_duration:
            a_value = list1[item_index]
            b_value = list2[item_index]

            # Draw a and b values on the same line
            a_value_text = item_font.render(f"{a_value}", True, BLACK)
            b_value_text = item_font.render(f"{b_value}", True, BLACK)

            screen.blit(a_value_text, (50, 230))
            screen.blit(b_value_text, (190, 230))

            # Draw the item
            item_text = item_font.render(f"{a_value}     :{b_value}", True, (1, 9, 255))
            screen.blit(item_text, (50, 260))
            item_surfaces.append(item_text)

            item_index += 1
            start_time = time.time()

    # Draw the items that are already on the screen
    for i, item_surface in enumerate(item_surfaces):
        screen.blit(item_surface, (340, 260 + i * 50))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()

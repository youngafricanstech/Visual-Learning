import pygame
import sys
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
pygame.display.set_caption("Displayed Python Range")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 56)
bold_font = pygame.font.Font(None, 39)

# User input for two lists
root = Tk()
root.title("Input")
root.geometry("900x400")  # Set the size of the window

# Label for instructions
label = Label(root, text="Enter two lists separated by commas (e.g., 'Apple,Banana,Orange,Monday,Tuesday,Wednesday'):", font=('Arial', 18))
label.pack()

# Entry widget for user input with increased width and height
entry_lists = Entry(root, font=('Arial', 18), width=60, bd=5, relief=tk.GROOVE)
entry_lists.pack()

# Function to get user input and close the window
def get_user_input():
    global user_input_lists
    user_input_lists = entry_lists.get().split(',') 
    # can you validate that the users input is in this form for index (a, b) in zip( ["Apple", "Orange"], ["Monday", "Tuesday"]):
    
    root.destroy()

# Button to submit user input
submit_button = Button(root, text="Submit", command=get_user_input, font=('Arial', 18))
submit_button.pack()

root.mainloop()

# dont change from here
import re

# Join the elements with commas
formatted_input = ', '.join(user_input_lists)

# Use regular expression to extract lists
matches = re.findall(r'\[.*?\]', formatted_input)
# Main game loop
running = True
list1, list2 = matches[0], matches[1]


# Draw the "for" text with user input
text = f"for index, (a, b) in enumerate(zip({list1}, {list2})):"
text_render = bold_font.render(text, True, BLACK)
# to here



# Determine the maximum length of the lists
max_length = max(len(list1), len(list2))

# Calculate the starting y-coordinate for display
start_y = 50

# Calculate the space between each line
line_spacing = 50

# Clear the screen
screen.fill(WHITE)

# Draw the "for" text
screen.blit(text_render, (13, start_y))

# Draw the index and corresponding list items for list1 (a) and list2 (b)
x_coordinate_A = 350
x_coordinate_B = 500

y_coordinate_A = 200
y_coordinate_B  = 200

x_index = 290
y_index = 200

new_list1 = eval(list1)
new_list2 = eval(list2)

for index, (a, b) in enumerate(zip(new_list1, new_list2)):
    # Calculate the y-coordinate for the current line

    # Draw index 
   # Draw index 
    list_items_text_a = font.render(f"{index}  ", True, (255, 255, 0))
    screen.blit(list_items_text_a, (x_index,  y_index))
    y_index += 35
    # Draw list1 (a) item if available
    list_items_text_a = font.render(f"{a}  ", True, (255, 0, 23))
    screen.blit(list_items_text_a, (x_coordinate_A, y_coordinate_A))

    # Draw list2 (b) item if available
    list_items_text_b = font.render(f"  {b}", True, (255, 0, 23))
    screen.blit(list_items_text_b, (x_coordinate_B, y_coordinate_A))
    y_coordinate_A += 35

# Update the display
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()

import pygame
import sys
import re
from tkinter import Tk, Label, Entry, Button

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Find Index of Fruits")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Fruits class
class Fruits:
    def __init__(self, names):
        self.original_fruits = [Fruit(name) for name in names]
        self.fruits = list(self.original_fruits)

class Fruit:
    def __init__(self, name):
        self.name = name
        self.found = False

    def draw(self, x, y, index):
        color = yellow if self.found else red
        pygame.draw.rect(screen, color, (x, y, 170, 33))  # Increased width and height
        font = pygame.font.Font(None, 32)
        text = font.render(f"{index}: {self.name}", True, white)
        screen.blit(text, (x + 10, y + 5))

# New function to draw the last found item at the middle of the screen
def draw_found_item_center():
    # Find the last marked item
    last_found_index = None
    for i, fruit in enumerate(fruits_data.fruits):
        if fruit.found:
            last_found_index = i

    # Draw only the last marked item
    if last_found_index is not None:
        x = (width - 170) // 6  # Center x-coordinate
        y = (height - 33) // 4  # Center y-coordinate

        # Unmark the previously found item
        for fruit in fruits_data.fruits:
            fruit.found = False

        # Mark the last found item with yellow color
        fruits_data.fruits[last_found_index].found = True

        # Draw a colored rectangle as the background
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 170, 33))

        # Draw the last marked item with yellow color and index number
        font = pygame.font.Font(None, 48)  # Increased font size
        text = font.render(f"Found Item: {fruits_data.fruits[last_found_index].name} (Index: {last_found_index})", True, yellow)

        # Draw the background color behind the text
        pygame.draw.rect(screen, (30, 30, 30), (x, y, text.get_width() + 20, text.get_height() + 10))

        screen.blit(text, (x + 10, y + 5))


# Initial list of fruits
fruits_data = Fruits(["Apple", "Banana", "Orange"])

# Function to handle button click and find the index
def find_fruit_index():
    index_str = index_entry.get()

    if not re.match(r'^my_list\.index\(".+"\)$', index_str):
        result_label.config(text='Error: Invalid index statement. Please enter in the format my_list.index("item").', fg=red)
        return

    item_name = re.match(r'my_list\.index\("(.+)"\)', index_str).group(1)

    try:
        index = [i for i, fruit in enumerate(fruits_data.fruits) if fruit.name == item_name][0]
        result_label.config(text=f"Index of '{item_name}': {index}", fg="#00FF00")

        # Mark the found item with yellow color
        fruits_data.fruits[index].found = True

    except IndexError:
        result_label.config(text=f"'{item_name}' not found in the list.", fg=red)


# Create Tkinter window
root = Tk()
root.title("Find Index of Fruits GUI")

# Labels and input fields
index_label = Label(root, text="Enter my_list.index(\"item\"):", font=("Arial", 16))
index_label.pack()

index_entry = Entry(root, font=("Arial", 16))
index_entry.pack()

# Button to find fruit index
index_button = Button(root, text="Find Index", command=find_fruit_index, font=("Arial", 16))
index_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window
root.geometry("400x250+350+330")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Draw all fruits in a horizontal line with five items per row
    for i, fruit in enumerate(fruits_data.fruits):
        row = i // 5
        col = i % 5
        fruit.draw(20 + col * 200, 20 + row * 80, i)  # Adjusted spacing

    # Draw the last found item at the middle of the screen
    draw_found_item_center()

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)  # Fix: Added parentheses and a value

    # Update Tkinter window
    root.update_idletasks()
    root.update()

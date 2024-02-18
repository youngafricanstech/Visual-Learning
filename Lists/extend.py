import pygame
import sys
from tkinter import Tk, Label, Button, Text
import re

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Extend List")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Item class
class Fruit:
    def __init__(self, name, is_text=False):
        self.name = name
        self.is_text = is_text
        self.is_new = False

    def draw(self, x, y, index, items_per_row):
        color = red if self.is_new else green
        col = index % items_per_row
        row = index // items_per_row
        padding = 10
        rect_width = 200
        rect_height = 40
        rect_x = x + col * (rect_width + padding)
        rect_y = y + row * (rect_height + padding)

        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(screen, color, rect)

        font_size = 40
        font = pygame.font.Font(None, font_size)
        display_name = self.name if self.is_text else str(self.name)
        text = font.render(f"{index}: {display_name}", True, white, None)
        text_rect = text.get_rect()
        text_rect.x = rect.x + (rect.width - text_rect.width) // 2
        text_rect.y = rect.y + (rect.height - text_rect.height) // 2
        screen.blit(text, text_rect.topleft)


# Initial list of fruits
initial_fruits = ["Apple", "Banana", "Orange", "Grapes", "Mango", "Pineapple", "Watermelon", "Strawberry"]
my_list = [Fruit(fruit) for fruit in initial_fruits]

# Function to handle button click and extend the list
def extend_items():
    extend_str = new_items_entry.get("1.0", "end-1c")

    if "my_list.extend" not in extend_str:
        result_label.config(text='Error: You must type my_list.extend(["item1", "item2"])', fg=red)
        return

    match = re.match(r"my_list\.extend\((.*?)\)", extend_str)
    if not match:
        result_label.config(text='Error: Invalid extend statement', fg=red)
        return

    arguments = match.group(1).strip()

    try:
        # Evaluate the arguments as a list
        new_elements = eval(arguments)

        if not isinstance(new_elements, (list, tuple)):
            raise ValueError()

        # Reset is_new to False for all existing items
        for existing_item in my_list:
            existing_item.is_new = False

        # Extend the current list with the new items
        my_list.extend([Fruit(element) for element in new_elements])

        # Set is_new to True for all newly added items
        for new_item in my_list[-len(new_elements):]:
            new_item.is_new = True

        # Clear the input field
        new_items_entry.delete("1.0", "end")
        result_label.config(text="Items extended successfully.", fg=green)

    except ValueError:
        result_label.config(text="Error: Invalid argument for extend", fg=red)

# Create Tkinter window
root = Tk()
root.title("Extend List GUI")

# Adjust Tkinter window size
root.geometry("500x200+350+350")  # Adjusted size

# Labels and input fields
new_items_label = Label(root, text="Enter new items (comma-separated):", font=("Helvetica", 20, "bold"))
new_items_label.pack()

# Use the Text widget for multiline input
new_items_entry = Text(root, font=("Helvetica", 18), width=40, height=1)
new_items_entry.pack()

# Button to extend items list
extend_button = Button(root, text="Extend Items", command=extend_items, font=("Helvetica", 18, "bold"))
extend_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Helvetica", 18, "bold"))
result_label.pack()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Draw a bar to wrap the list
    # pygame.draw.rect(screen, blue, (10, height - 50, width - 20, 50))

    # Draw all items
    for i, item in enumerate(my_list):
        item.draw(20, 10, i, 5)  # Pass items_per_row as 5

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

    # Update Tkinter window
    root.update_idletasks()
    root.update()

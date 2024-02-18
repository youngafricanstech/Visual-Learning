import pygame
import sys
import re
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Remove Fruits List")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fruits class
class Fruits:
    def __init__(self, names):
        self.original_fruits = [Fruit(name) for name in names]
        self.fruits = list(self.original_fruits)

class Fruit:
    def __init__(self, name):
        self.name = name

    def draw(self, x, y, index):
        pygame.draw.rect(screen, red, (x, y, 170, 33))  # Increased width and height
        font = pygame.font.Font(None, 32)
        text = font.render(f"{index}: {self.name}", True, white)
        screen.blit(text, (x + 10, y + 5))

# Initial list of fruits
fruits_data = Fruits(["Apple", "Banana", "Orange"])

# Function to handle button click and remove from the list
def remove_fruit():
    remove_str = pop_fruit_entry.get()

    if not re.match(r'^my_list\.remove\(".+"\)$', remove_str):
        result_label.config(text='Error: Invalid remove statement. Please enter in the format my_list.remove("item").', fg=red)
        return

    item_name = re.match(r'my_list\.remove\("(.+)"\)', remove_str).group(1)

    # Remove the fruit with the specified name if it exists
    removed = False
    for fruit in fruits_data.fruits:
        if fruit.name == item_name:
            fruits_data.fruits.remove(fruit)
            removed = True
            break

    if removed:
        result_label.config(text=f"{item_name} removed successfully.", fg=blue)
    else:
        result_label.config(text=f"Error: {item_name} not found in the list.", fg=red)

    # update_listbox()
    pop_fruit_entry.delete(0, "end")

# Function to reload the original items
def reload_items():
    fruits_data.fruits = list(fruits_data.original_fruits)
    # update_listbox()
    result_label.config(text="Items reloaded successfully.", fg=blue)

# Function to update the listbox
# def update_listbox():
#     listbox.delete(0, "end")
#     for i, fruit in enumerate(fruits_data.fruits):
#         listbox.insert("end", f"{i}: {fruit.name}")

# Create Tkinter window
root = Tk()
root.title("Remove Fruits List GUI")

# Labels and input fields
pop_fruit_label = Label(root, text="Enter remove statement (my_list.remove(\"item\")):", font=("Arial", 16))
pop_fruit_label.pack()

pop_fruit_entry = Entry(root, font=("Arial", 16), width=30)
pop_fruit_entry.pack()

# Button to remove fruit from the list
pop_button = Button(root, text="Remove Fruit", command=remove_fruit, font=("Arial", 16))
pop_button.pack()

# Button to reload original items
reload_button = Button(root, text="Reload Items", command=reload_items, font=("Arial", 16))
reload_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# # Listbox to display fruits
# listbox = Listbox(root, selectmode="single", height=1, width=30, font=("Arial", 16))
# listbox.pack()

# # Scrollbar for the listbox
# scrollbar = Scrollbar(root, command=listbox.yview, orient="horizontal")
# scrollbar.pack()

# Set the geometry of the Tkinter window
root.geometry("700x250+350+330")
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Draw a bar to wrap the list
    pygame.draw.rect(screen, blue, (10, 10, width - 20, 190))

    # Draw all fruits in a horizontal line with five items per row
    for i, fruit in enumerate(fruits_data.fruits):
        row = i // 5
        col = i % 5
        fruit.draw(20 + col * 200, 20 + row * 80, i)  # Adjusted spacing

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

    # Update Tkinter window
    root.update_idletasks()
    root.update()

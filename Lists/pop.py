import pygame
import sys
import re  # Import the 're' module
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pop Fruits List")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fruit class
class Fruit:
    def __init__(self, name):
        self.name = name

    def draw(self, x, y, index):
        pygame.draw.rect(screen, red, (x, y, 170, 33))  # Increased width and height
        font = pygame.font.Font(None, 32)
        text = font.render(f"{index}: {self.name}", True, white)
        screen.blit(text, (x + 10, y + 5))

# Original list of fruits
original_fruits = [
    Fruit("Apple"),
    Fruit("Banana"),
    Fruit("Orange"),
]

# Dictionary to store lists
lists = {'my_list': {
    'fruits': original_fruits.copy(),  # Copy the original list
}}

# Function to handle button click and pop from the list
def pop_fruit():
    pop_str = pop_fruit_entry.get()

    # Use regex to match the desired format: my_list.pop() or my_list.pop(index)
    match = re.match(r'^(\w+)\.pop(?:\((\d*)\))$', pop_str)

    if not match:
        result_label.config(text='Error: Invalid pop statement', fg=red)
        return

    list_name = match.group(1)
    index_str = match.group(2)

    # Check if the list exists
    if list_name not in lists or 'fruits' not in lists[list_name]:
        result_label.config(text=f'Error: List "{list_name}" not found.', fg=red)
        return

    my_list = lists[list_name]['fruits']

    # Pop the last fruit if no index is specified or if the index is empty
    if not index_str:
        if my_list:
            popped_element = my_list.pop()
            result_label.config(text=f"Last fruit ({popped_element.name}) popped successfully from {list_name}.", fg=blue)
        else:
            result_label.config(text=f"Error: List is empty, cannot pop from {list_name}.", fg=red)
    else:
        index = int(index_str)
        # Pop the fruit at the specified index if it is valid
        if 0 <= index < len(my_list):
            popped_element = my_list.pop(index)
            result_label.config(text=f"Fruit at index {index} ({popped_element.name}) popped successfully from {list_name}.", fg=blue)
        else:
            result_label.config(text=f"Error: Index {index} is out of range for {list_name}.", fg=red)

    update_listbox()
    pop_fruit_entry.delete(0, "end")

# Function to reload the original list
def reload_list():
    lists['my_list']['fruits'] = original_fruits.copy()
    result_label.config(text="Original list reloaded successfully.", fg=blue)
    update_listbox()

# Function to update the listbox
def update_listbox():
    listbox.delete(0, "end")
    for i, fruit in enumerate(lists['my_list']['fruits']):
        listbox.insert("end", f"{i}: {fruit.name}")

# Create Tkinter window
root = Tk()
root.title("Pop Fruits List GUI")

# Labels and input fields
pop_fruit_label = Label(root, text="Enter pop statement (my_list.pop() or my_list.pop(index)):", font=("Arial", 16))
pop_fruit_label.pack()

pop_fruit_entry = Entry(root, font=("Arial", 16))
pop_fruit_entry.pack()

# Button to pop fruit from the list
pop_button = Button(root, text="Pop Fruit", command=pop_fruit, font=("Arial", 16))
pop_button.pack()

# Button to reload the original list
reload_button = Button(root, text="Reload", command=reload_list, font=("Arial", 16))
reload_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Listbox to display fruits
listbox = Listbox(root, selectmode="single", height=1, width=30, font=("Arial", 16))
listbox.pack()

# Scrollbar for the listbox
scrollbar = Scrollbar(root, command=listbox.yview, orient="horizontal")
scrollbar.pack()

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
    for i, fruit in enumerate(lists['my_list']['fruits']):
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

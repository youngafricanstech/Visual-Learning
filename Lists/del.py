import pygame
import sys
import re
from tkinter import Tk, Label, Entry, Button

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
        self.fruits = [Fruit(name) for name in names]

class Fruit:
    def __init__(self, name):
        self.name = name

    def draw(self, x, y, index):
        pygame.draw.rect(screen, red, (x, y, 170, 33))  # Increased width and height
        font = pygame.font.Font(None, 32)
        text = font.render(f"{index}: {self.name}", True, white)
        screen.blit(text, (x + 10, y + 5))

# Initial list of fruits
fruits_data = Fruits(["Apple", "Banana", "Orange", "Grapes", "Mango", "Pineapple", "Watermelon", "Strawberry"])

# Function to handle button click and remove from the list
def remove_fruit():
    remove_str = pop_fruit_entry.get()

    if not re.match(r'^del\s+my_list(\s*\[\d+:\d+\]\s*|\s*\[\d+\]\s*|\s*|\s*\[-?\d+\]\s*|\s*\[:\d+\]\s*|\s*\[-?\d+:\]\s*|\s*\[::\d+\]\s*)$', remove_str):
        result_label.config(text='Error: Invalid del statement. Please enter in the format del my_list[index], del my_list[:stop], del my_list[start:], del my_list[::step], or del my_list.', fg=red)
        return

    index_match = re.search(r'\[(-?\d+)\]', remove_str)
    start_stop_match = re.search(r'\[(\d+):(\d+)\]', remove_str)
    start_match = re.search(r'\[:(\d+)\]', remove_str)
    stop_match = re.search(r'\[(-?\d+):]', remove_str)
    step_match = re.search(r'\[::(\d+)\]', remove_str)

    if '[' in remove_str:
        if index_match:
            # Delete a specific index
            index = int(index_match.group(1))
            try:
                del fruits_data.fruits[index]
                result_label.config(text=f"Item at index {index} removed successfully.", fg=blue)
            except (ValueError, IndexError):
                result_label.config(text=f"Error: Invalid index {index}.", fg=red)
        elif start_stop_match:
            # Delete items within a range
            start = int(start_stop_match.group(1))
            stop = int(start_stop_match.group(2))
            del fruits_data.fruits[start:stop]
            result_label.config(text=f"Items in range {start}:{stop} removed successfully.", fg=blue)
        elif start_match:
            # Delete items up to the specified stop index
            stop = int(start_match.group(1))
            del fruits_data.fruits[:stop]
            result_label.config(text=f"Items up to index {stop} removed successfully.", fg=blue)
        elif stop_match:
            # Delete items starting from the specified start index
            start = int(stop_match.group(1))
            del fruits_data.fruits[start:]
            result_label.config(text=f"Items starting from index {start} removed successfully.", fg=blue)
        elif step_match:
            # Delete items with a specified step
            step = int(step_match.group(1))
            del fruits_data.fruits[::step]
            result_label.config(text=f"Items with step {step} removed successfully.", fg=blue)
    else:
        # Clear the entire list
        fruits_data.fruits.clear()
        result_label.config(text="List cleared successfully.", fg=blue)

    pop_fruit_entry.delete(0, "end")

# Function to reload items
def reload_items():
    global fruits_data
    fruits_data = Fruits(["Apple", "Banana", "Orange", "Grapes", "Mango", "Pineapple", "Watermelon", "Strawberry"])
    result_label.config(text="Items reloaded successfully.", fg=blue)

# Create Tkinter window
root = Tk()
root.title("Remove Fruits List GUI")

# Labels and input fields
pop_fruit_label = Label(root, text="Enter del statement (del my_list[index], del my_list[:stop], del my_list[start:], del my_list[::step], or del my_list):", font=("Arial", 16))
pop_fruit_label.pack()

pop_fruit_entry = Entry(root, font=("Arial", 16))
pop_fruit_entry.pack()

# Button to remove fruit from the list
pop_button = Button(root, text="Remove Fruit", command=remove_fruit, font=("Arial", 16))
pop_button.pack()

# Button to reload items
reload_button = Button(root, text="Reload Items", command=reload_items, font=("Arial", 16))
reload_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window
window_width = 1100
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

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

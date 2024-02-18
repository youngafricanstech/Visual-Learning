import pygame
import sys
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar
import re

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slice Fruits List")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 203)
yellow = (255, 255, 0)

# Fruits class
class Fruits:
    def __init__(self, names):
        self.fruits = [Fruit(name) for name in names]
        self.last_highlighted_indices = []

    # def draw_highlighted_items(self):
    #     for index in self.last_highlighted_indices:
    #         self.fruits[index].draw_highlighted(index)

class Fruit:
    def __init__(self, name):
        self.name = name
        self.selected_color = None

    def draw(self, x, y, index):
        color = self.selected_color if self.selected_color else blue  # Set transparent color if no selected_color
        pygame.draw.rect(screen, color, (x, y, 170, 33))  # Increased width and height

        # Draw the text without a background
        font = pygame.font.Font(None, 32)
        text = font.render(f"{index}: {self.name}", True, white)
        screen.blit(text, (x + 10, y + 5))

    def draw_highlighted(self, index, row, col):

        font = pygame.font.Font(None, 34)
        text = font.render(f"{index}: {self.name}", True, white)
        text_rect = text.get_rect(topleft=(20 + col * 200, 220 + row * 50))
        pygame.draw.rect(screen, red, (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        screen.blit(text, text_rect.topleft)

# Initial list of fruits
my_list = Fruits(["Apple", "Banana", "Orange", "Grapes", "Mango", "Pineapple", "Watermelon", "Strawberry"])

# Function to handle button click and remove from the list
def remove_fruit():
    remove_str = pop_fruit_entry.get()

    if not re.match(r'^my_list(\s*\[\d+:\d+\]\s*|\s*\[\d+\]\s*|\s*|\s*\[-?\d+\]\s*|\s*\[:\d+\]\s*|\s*\[-?\d+:\]\s*|\s*\[::\d+\]\s*)$', remove_str):
        result_label.config(text='Error: Invalid statement. Please enter in the format my_list[index], my_list[:stop], my_list[start:], my_list[::step].', fg=red)
        return

    index_match = re.search(r'\[(-?\d+)\]', remove_str)
    start_stop_match = re.search(r'\[(\d+):(\d+)\]', remove_str)
    start_match = re.search(r'\[:(\d+)\]', remove_str)
    stop_match = re.search(r'\[(-?\d+):]', remove_str)
    step_match = re.search(r'\[::(\d+)\]', remove_str)

    # Reset color for previously highlighted items
    for index in my_list.last_highlighted_indices:
        my_list.fruits[index].selected_color = None

    my_list.last_highlighted_indices = []

    if '[' in remove_str:
        if index_match:
            # Highlight a specific index
            index = int(index_match.group(1))
            try:
                my_list.fruits[index].selected_color = yellow
                my_list.last_highlighted_indices.append(index)
                result_label.config(text=f"Slice operation at index {index} highlighted successfully.", fg=blue)
            except (ValueError, IndexError):
                result_label.config(text=f"Error: Invalid index {index}.", fg=red)
        elif start_stop_match:
            # Highlight items within a range
            start = int(start_stop_match.group(1))
            stop = int(start_stop_match.group(2))
            for i in range(start, stop):
                my_list.fruits[i].selected_color = yellow
                my_list.last_highlighted_indices.append(i)
            result_label.config(text=f"Slice operation in range {start}:{stop} highlighted successfully.", fg=blue)
        elif start_match:
            # Highlight items up to the specified stop index
            stop = int(start_match.group(1))
            for i in range(stop):
                my_list.fruits[i].selected_color = yellow
                my_list.last_highlighted_indices.append(i)
            result_label.config(text=f"Slice operation up to index {stop} highlighted successfully.", fg=blue)
        elif stop_match:
            # Highlight items starting from the specified start index
            start = int(stop_match.group(1))
            for i in range(start, len(my_list.fruits)):
                my_list.fruits[i].selected_color = yellow
                my_list.last_highlighted_indices.append(i)
            result_label.config(text=f"Slice operation starting from index {start} highlighted successfully.", fg=blue)
        elif step_match:
            # Highlight items with a specified step
            step = int(step_match.group(1))
            for i in range(0, len(my_list.fruits), step):
                my_list.fruits[i].selected_color = yellow
                my_list.last_highlighted_indices.append(i)
            result_label.config(text=f"Slice operation with step {step} highlighted successfully.", fg=blue)
        
    else:
        # Highlight the entire list
        for i, fruit in enumerate(my_list.fruits):
            fruit.selected_color = yellow
            my_list.last_highlighted_indices.append(i)
        result_label.config(text="Slice operation on the entire list highlighted successfully.", fg=blue)
    pop_fruit_entry.delete(0, "end")


# Create Tkinter window
root = Tk()
root.title("Slice Fruits List GUI")

# Labels and input fields
pop_fruit_label = Label(root, text="Enter statement (my_list[index], my_list[start:stop] my_list[:stop], my_list[start:], my_list[::step]):", font=("Arial", 16))
pop_fruit_label.pack()

pop_fruit_entry = Entry(root, font=("Arial", 16))
pop_fruit_entry.pack()

# Button to remove fruit from the list
pop_button = Button(root, text="Slice Operation", command=remove_fruit, font=("Arial", 16))
pop_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()


# Set the geometry of the Tkinter window
window_width = 1100
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height // 4}+{x_position}+{y_position + 320}")

# Main game loop
# ...

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Draw a bar to wrap the list
    # pygame.draw.rect(screen, blue, (10, 10, width - 20, 190))

    # Draw all fruits in a horizontal line with five items per row
    for i, fruit in enumerate(my_list.fruits):
        row = i // 5
        col = i % 5
        fruit.draw(20 + col * 200, 20 + row * 80, i)  # Adjusted spacing

    # Draw highlighted items
    for i, index in enumerate(my_list.last_highlighted_indices):
        row = index // 5
        col = index % 5
        my_list.fruits[index].draw_highlighted(index, row, col)

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

    # Update Tkinter window
    root.update_idletasks()
    root.update()

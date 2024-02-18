import pygame
import sys
import re
from tkinter import Tk, Label, Button, Listbox, Scrollbar
from tkinter.scrolledtext import ScrolledText

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Append Fruits List")

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

# Initial list of fruits
fruits = [
    Fruit("Apple"),
    Fruit("Banana"),
    Fruit("Orange"),
]

# Function to handle button click and append to the list
def append_fruit():
    append_str = new_fruit_entry.get("1.0", "end-1c")

    if "my_list.append" not in append_str:
        result_label.config(text='Error: You must type my_list.append("item")', fg=red)
        return

    match = re.match(r"my_list\.append\((.*?)\)", append_str)
    if not match:
        result_label.config(text='Error: Invalid append statement', fg=red)
        return

    argument = match.group(1).strip()

    try:
        if argument == "True":
            argument_value = True
        elif argument == "False":
            argument_value = False
        else:
            argument_value = eval(argument)
            if not isinstance(argument_value, (str, int, float, bool)):
                raise ValueError()
    except ValueError:
        result_label.config(text="Error: Argument must be a string, number, True, or False", fg=red)
        return

    fruits.append(Fruit(argument_value))
    new_fruit_entry.delete("1.0", "end")
    result_label.config(text="Fruit appended successfully.", fg=blue)


# Create Tkinter window
root = Tk()
root.title("Append Fruits List GUI")

# Labels and input fields
instruction_label = Label(root, text="You must type my_list.append(\"item\")", font=("Arial", 16), fg="blue")
instruction_label.pack()

new_fruit_label = Label(root, text="Enter append statement:", font=("Arial", 20))
new_fruit_label.pack()

# Use ScrolledText for multiline input with scrollbar
new_fruit_entry = ScrolledText(root, font=("Arial", 16), width=40, height=1)  # Increased width and height
new_fruit_entry.pack()

# Button to append fruit to the list
append_button = Button(root, text="Append Fruit", command=append_fruit, font=("Arial", 16))
append_button.pack()

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window to move the list items to the top
root.geometry("500x200+350+350")  # Adjusted size

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
    for i, fruit in enumerate(fruits):
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

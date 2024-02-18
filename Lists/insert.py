import pygame
import sys
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, font

# Initialize pygame
pygame.init()

# Set up display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Insert Fruits")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Fruit class
class Fruit:
    def __init__(self, name, is_text=False):
        self.name = name
        self.is_new = False
        self.is_text = is_text

    def draw(self, x, y, index, items_per_row):
        color = yellow if self.is_new else red
        col = index % items_per_row
        row = index // items_per_row
        padding = 10  # Adjust the padding between rectangles
        rect_width = 180  # Adjusted the width of the rectangle
        rect_height = 40  # Adjusted the height of the rectangle
        rect_x = x + col * (rect_width + padding)
        rect_y = y + row * (rect_height + padding)

        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(screen, color, rect)

        font_size = 32  # Adjust the font size
        font = pygame.font.Font(None, font_size)
        display_name = self.name if self.is_text else str(self.name)  # Convert to string if not text
        text = font.render(f"{index}: {display_name}", True, white, None)
        text_rect = text.get_rect()
        text_rect.x = rect.x + (rect.width - text_rect.width) // 2
        text_rect.y = rect.y + (rect.height - text_rect.height) // 2
        screen.blit(text, text_rect.topleft)

# Fruits class to store multiple fruits
class Fruits:
    def __init__(self, fruit_names):
        self.fruits = [Fruit(name) for name in fruit_names]

    def insert(self, index, name):
        new_fruit = Fruit(name)
        self.fruits.insert(index, new_fruit)

        # Set the is_new flag to True only for the last inserted item
        for fruit in self.fruits:
            fruit.is_new = False
        new_fruit.is_new = True

    def get_list(self):
        return self.fruits

# Single Fruits object to store fruits
fruits = Fruits(['"Apple"', '"Banana"', '"Orange"'])


# Function to handle button click
def insert_fruit():
    try:
        index = int(input_entry.get())
        name = input_entry2.get()

        # Validate the input for the item
        validate_input(name)

        fruits.insert(index, name)

        # Update the listbox
        update_listbox()

        # Clear the input fields
        input_entry.delete(0, "end")
        input_entry2.delete(0, "end")
        result_label.config(text="")
    except ValueError as e:
        result_label.config(text=str(e))

# Function to validate the input for the item
def validate_input(name):
    try:
        # Check if the input is a boolean value
        if name.lower() == 'false' or name.lower() == 'true':
            return
        # Check if the input is a number
        float(name)
    except ValueError:
        # Check if the input is a string enclosed in quotes
        if not ((name.startswith('"') and name.endswith('"')) or (name.startswith("'") and name.endswith("'"))):
            raise ValueError("Invalid input for item. Please enter a valid number, 'True', 'False', or enclose the string in single or double quotes.")


# Function to update the listbox
def update_listbox():
    listbox.delete(0, "end")
    for i, fruit in enumerate(fruits.get_list()):
        listbox.insert("end", f"{i}: {fruit.name}")
    listbox.config(font=("Helvetica", 14))  # Adjust the font size as needed
    # Set a bold font for the list items
    bold_font = font.Font(weight="bold")
    listbox.config(font=bold_font, height=5)  # Adjust the height if needed

# ... (rest of the code remains unchanged)


# Function to calculate the number of rows and columns
def calculate_rows_columns(num_items, items_per_row):
    num_rows = (num_items + items_per_row - 1) // items_per_row
    num_columns = min(items_per_row, num_items)
    return num_rows, num_columns

# Create Tkinter window
root = Tk()
root.title("Insert Fruits GUI")

# Label and input fields
label_input = Label(root, text="my_list.insert(", font=("Helvetica", 16, "bold"))  # Increased font size, bold
label_input.pack(side="left")

input_entry = Entry(root, width=5, font=("Helvetica", 16))  # Increased input field size and font size
input_entry.pack(side="left")

comma_label = Label(root, text=",", font=("Helvetica", 16))  # Increased label font size
comma_label.pack(side="left")

input_entry2 = Entry(root, width=15, font=("Helvetica", 16))  # Increased input field size and font size
input_entry2.pack(side="left")

closing_bracket_label = Label(root, text=")", font=("Helvetica", 16))  # Increased label font size
closing_bracket_label.pack(side="left")

insert_button = Button(root, text="Insert Fruit", command=insert_fruit, font=("Helvetica", 16))  # Increased button font size
insert_button.pack()

# Label to display result or error messages
result_label = Label(root, text="")
result_label.pack()

# Listbox to display fruits
listbox = Listbox(root, selectmode="single", height=5, width=30)
listbox.pack()

# Populate the listbox with the initial fruits
update_listbox()

# Scrollbar for the listbox
scrollbar = Scrollbar(root, command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Calculate the number of rows and columns
    num_rows, num_columns = calculate_rows_columns(len(fruits.get_list()), 5)  # Change the number of columns to 5

    # Draw all fruits in columns and rows
    for i, fruit in enumerate(fruits.get_list()):
        fruit.draw(50, 50, i, num_columns)

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

    # Update Tkinter window
    root.update_idletasks()
    root.update()

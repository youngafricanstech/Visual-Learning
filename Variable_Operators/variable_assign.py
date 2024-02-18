import pygame
import sys
from tkinter import Tk, Label, Entry, Button

# Initialize pygame
pygame.init()

# Set up Pygame display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Find Variable Data")

# Colors
white = (255, 255, 255)
blue = "blue"  # Tkinter color name
yellow = "yellow"  # Tkinter color name
red = "red"  # Tkinter color name

# Variable class
class Variable:
    def __init__(self):
        self.name = ""
        self.data_value = ""
        self.equal_sign = ""
        self.selected_color = None
        self.target_x = 0
        self.move_speed = 2

    def draw(self, x, y):
        # color = self.selected_color if self.selected_color else blue
        pygame.draw.rect(screen, (255, 255, 255), (x + 410, y - 380, 250, 30))
        font = pygame.font.Font(None, 62, bold=True)  # Larger and bold font for variable name
        text = font.render(f"{self.name} {self.equal_sign}  {self.data_value}", True, blue)
        screen.blit(text, (x + 350, y - 380))


    def draw_data_value(self, x, y, box_size=150):
        font = pygame.font.Font(None, 50)  # Larger font size for data value
        text = font.render(f"{self.data_value}", True, white)

        # Calculate the position to center the text inside the box
        text_x = x - text.get_width() // 2
        text_y = y - 230

        screen.blit(text, (text_x, text_y))

    def draw_info_box(self, x, y, box_size=250):
        pygame.draw.rect(screen, red, (x - box_size // 2, y - 330, box_size, box_size))  # Centered square with a red background
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}", True, blue)
        text_rect = text.get_rect(center=(x, y - 350))  # Place above the top center
        screen.blit(text, text_rect.topleft)

    def animate_data_value(self):
        if self.target_x > 0:
            self.target_x -= self.move_speed
            self.target_x = max(self.target_x, 0)  # Minimum value to stop the animation
            return True
        return False
    

import re

def validate_input(variable_name, value, equal):
    if not variable_name or not equal:
        return False  # Variable name or equal sign is empty, return False
    
    # Check if equal is the equal sign "="
    if equal != "=":
        return False  # Invalid equal sign, return False

    # Check if variable_name is a valid combination of letters, numbers, and an optional underscore
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*[a-zA-Z0-9]$', variable_name):
        return False  # Invalid variable name, return False

    # Check if the value is a boolean (True or False)
    if value in ['True', 'False']:
        return True

    try:
        # Check if the value is a number
        float(value)
        return True
    except ValueError:
        return value.startswith('"') and value.endswith('"') or value.startswith("'") and value.endswith("'")

# Example usage:
variable_name = "_valid_name_123"
boolean_value = "True"
numeric_value = "42"
equal_sign = "="

if validate_input(variable_name, boolean_value, equal_sign):
    print("Validation successful for boolean value.")
else:
    print("Validation failed for boolean value.")

if validate_input(variable_name, numeric_value, equal_sign):
    print("Validation successful for numeric value.")
else:
    print("Validation failed for numeric value.")


# Create Tkinter window
root = Tk()
root.title("Find Variable Data GUI")

# Labels and input fields for variable name, equal sign, and data value
variable_name_label = Label(root, text="Variable Name:", font=("Helvetica", 16))  # Increase font size
variable_name_label.pack(side="left")

variable_name_entry = Entry(root, font=("Helvetica", 16))  # Adjust font size here
variable_name_entry.pack(side="left")

equal_label = Label(root, text=" Equal Sign:", font=("Helvetica", 16))  # Increase font size
equal_label.pack(side="left")

equal_entry = Entry(root, font=("Helvetica", 16))  # Adjust font size here
equal_entry.pack(side="left")

data_value_label = Label(root, text=" Data Value:", font=("Helvetica", 16))  # Increase font size
data_value_label.pack(side="left")

data_value_entry = Entry(root, font=("Helvetica", 16))  # Adjust font size here
data_value_entry.pack(side="left")


# Label to display validation error message
validation_error_label = Label(root, text="", fg=red)
validation_error_label.pack()

# Button to update variable data
def update_variable_data():
    variable.name = variable_name_entry.get()
    variable.equal_sign = equal_entry.get()
    variable.data_value = data_value_entry.get()

    # Validate input for data value
    if not validate_input(variable.name, variable.data_value, variable.equal_sign):
        validation_error_label.config(text="Error: Variable name, equal sign, or data value is empty.")
        result_label.config(text="")
        variable.name = ""  # Clear variable name
        variable.data_value = ""  # Clear data value
        equal_label.config(text="")  # Hide equal sign
        return

    validation_error_label.config(text="")  # Clear validation error message
    equal_label.config(text=" Equal Sign:")  # Show equal sign
    variable.target_x = width // 2  # Set the target_x to the center of the box
    result_label.config(text=f"Updated {variable.name} data to: {variable.data_value}")
    variable.selected_color = yellow
    animate_data_value()

update_button = Button(root, text="Update Data", command=update_variable_data)
update_button.pack(side="left")

# Label to display result or error messages
result_label = Label(root, text="")
result_label.pack()

# Create a single instance of the Variable class
variable = Variable()

# Function to animate data value
def animate_data_value():
    while variable.animate_data_value():
        # Update Pygame screen
        screen.fill(white)

        # Draw a bar to display the variable data
        pygame.draw.rect(screen, blue, (10, height - 80, width - 20, 80))

        # Draw the variable with optional highlighting
        variable.draw(20, height - 80)

        # Draw a box around the variable name in the Pygame window
        variable.draw_info_box(width // 2, height // 2)  # Centered box without animation

        # Draw the moving data value inside the box
        variable.draw_data_value(width // 2, height // 2)

        # Update Pygame display
        pygame.display.flip()

        # Update Tkinter window
        root.update_idletasks()
        root.update()

root.geometry("1300x100+130+520")  # Adjusted size

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update Pygame screen
    screen.fill(white)

    # Draw a bar to display the variable data
    pygame.draw.rect(screen, blue, (10, height - 80, width - 20, 80))

    # Draw the variable with optional highlighting
    variable.draw(20, height - 80)

    # Draw a box around the variable name in the Pygame window
    variable.draw_info_box(width // 2, height // 2)  # Centered box without animation

    # Draw the moving data value inside the box
    variable.draw_data_value(width // 2, height // 2)

    # Update Pygame display
    pygame.display.flip()

    # Update Tkinter window
    root.update_idletasks()
    root.update()

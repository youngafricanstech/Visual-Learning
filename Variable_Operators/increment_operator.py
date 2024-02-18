import pygame
import sys
from tkinter import Tk, Label, Entry, Button

# Initialize pygame
pygame.init()

# Set up Pygame display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Increment and Addition Operations")

# Colors
white = (255, 255, 255)
blue = "blue"  # Tkinter color name
red = "red"  # Tkinter color name

# Variable class
class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.prev_value = value
        self.increment = 0
        self.selected_color = None

    def draw(self, x, y):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 350, 30))
        font = pygame.font.Font(None, 100, bold=True)
        input_text = input_entry.get()
        try:
            if '+=' in input_text:
                operation, operand = input_text.split('+=')
                self.increment = int(operand.strip()) if operand.strip().isdigit() else 0
                text = font.render(f"{input_text} = {self.value}", True, blue)
            elif '+' in input_text:
                operation, operand = input_text.split('+')
                result = eval(operand.strip(), {'number': self.value})
                text = font.render(f"{input_text} = {result}", True, blue)
            else:
                text = font.render(f"{input_text} = {self.value}", True, blue)
        except Exception as e:
            text = font.render(f"Error: {e}", True, red)
        screen.blit(text, (x - 120, y-350))

# Create Tkinter window
root = Tk()
root.title("Increment and Addition Operations GUI")

# Input for user to type "number += 1" or "number + 2"
input_label = Label(root, text="Operation: ", font=("Helvetica", 22, "bold"))
input_label.pack(side="left")

input_entry = Entry(root, font=("Helvetica", 30))
input_entry.insert(0, "number += 0")  # Set default value
input_entry.pack(side="left", pady=10)  # Increased height with pady

# Label to display result or error messages
result_label = Label(root, text="", font=("Helvetica", 18, "bold"))
result_label.pack()

# Buttons to perform the operation (Increment or Add)
def perform_increment():
    try:
        input_text = input_entry.get()
        variable.value += variable.increment  # Keep incrementing the value
        result_label.config(text=f"Number incremented by {variable.increment}. New value: {variable.value}", font=("Helvetica", 12, "bold"))
    except Exception as e:
        result_label.config(text=f"Error: {e}", font=("Helvetica", 12, "bold"))

increment_button = Button(root, text="Increment", command=perform_increment, font=("Helvetica", 14, "bold"), padx=10, pady=5)
increment_button.pack()

def perform_addition():
    try:
        input_text = input_entry.get()
        variable.increment = 0  # Reset the increment to default
        variable.value = variable.prev_value  # Reset the variable value to the previous value
        result_label.config(text="")  # Reset result label
        if '+' in input_text:
            operation, operand = input_text.split('+')
            result = eval(operand.strip(), {'number': variable.value})
            result_label.config(text=f"Result of addition: {result}. Number value remains: {variable.value}", font=("Helvetica", 12, "bold"))
        else:
            result_label.config(text="Error: Please use '+' for addition operation.", font=("Helvetica", 12, "bold"))
    except Exception as e:
        result_label.config(text=f"Error: {e}")

addition_button = Button(root, text="Addition", command=perform_addition, font=("Helvetica", 14, "bold"), padx=10, pady=5)
addition_button.pack()

# Create a single instance of the Variable class
variable = Variable("number", 0)

root.geometry("1000x120+180+400")  # Adjusted size


# Function to draw the variable
def draw_variable():
    variable.draw(width // 2 - 175, height // 2 - 15)
    pygame.font.init()
    my_font = pygame.font.Font(None, 100, bold=True)
    text_surface = my_font.render(f"print({variable.name}) = {variable.value}", True, red)
    screen.blit(text_surface, (230, height // 2 - 270))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)
    draw_variable()
    pygame.display.flip()
    root.update_idletasks()
    root.update()

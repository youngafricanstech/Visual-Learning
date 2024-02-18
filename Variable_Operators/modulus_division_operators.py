import pygame
import sys
from tkinter import Tk, Label, Entry, Button

# Initialize pygame
pygame.init()

# Set up Pygame display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modulus and Division Operations")

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
        self.decrement = 0
        self.selected_color = None

    def draw(self, x, y):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 350, 30))
        font = pygame.font.Font(None, 100, bold=True)
        input_text = input_entry.get()
        try:
            if '%' in input_text:
                operation, operand = input_text.split('%')
                result = self.value % int(operand.strip()) if operand.strip().isdigit() else 0
                text = font.render(f"{input_text} = {result}", True, blue)
            elif '/' in input_text:
                operation, operand = input_text.split('/')
                result = self.value / int(operand.strip()) if operand.strip().isdigit() else 0
                text = font.render(f"{input_text} = {result}", True, blue)
            else:
                text = font.render(f"{input_text} = {self.value}", True, blue)
        except Exception as e:
            text = font.render(f"Error: {e}", True, red)
        screen.blit(text, (x - 120, y-350))

# Create Tkinter window
root = Tk()
root.title("Modulus and Division Operations GUI")

# Input for the user to type "number % 2" or "number / 2"
input_label = Label(root, text="Operation: ", font=("Helvetica", 22, "bold"))
input_label.pack(side="left")

input_entry = Entry(root, font=("Helvetica", 30))
input_entry.insert(0, "number % 2")  # Set default value
input_entry.pack(side="left", pady=10)  # Increased height with pady

# Label to display the result or error messages
result_label = Label(root, text="", font=("Helvetica", 18, "bold"))
result_label.pack()

# Buttons to perform the operation (Modulus, Division, Decrement, and Subtraction)
def perform_modulus():
    try:
        input_text = input_entry.get()
        operation, operand = input_text.split('%')
        result = variable.value % int(operand.strip()) if operand.strip().isdigit() else 0
        result_label.config(text=f"Result of modulus operation: {result}. Number value remains: {variable.value}", font=("Helvetica", 12, "bold"))
    except Exception as e:
        result_label.config(text=f"Error: {e}", font=("Helvetica", 12, "bold"))

modulus_button = Button(root, text="Modulus", command=perform_modulus, font=("Helvetica", 14, "bold"), padx=10, pady=5)
modulus_button.pack()

def perform_division():
    try:
        input_text = input_entry.get()
        operation, operand = input_text.split('/')
        result = variable.value / int(operand.strip()) if operand.strip().isdigit() else 0
        result_label.config(text=f"Result of division operation: {result}. Number value remains: {variable.value}", font=("Helvetica", 12, "bold"))
    except Exception as e:
        result_label.config(text=f"Error: {e}", font=("Helvetica", 12, "bold"))

division_button = Button(root, text="Division", command=perform_division, font=("Helvetica", 14, "bold"), padx=10, pady=5)
division_button.pack()

# Create a single instance of the Variable class
variable = Variable("number", 50)  # Updated initial value to 50

root.geometry("1000x120+180+400")  # Adjusted size

# Function to draw the variable
def draw_variable():
    pygame.font.init()
    my_font = pygame.font.Font(None, 90, bold=True)
    text_surface = my_font.render(f"{variable.name} = {variable.value}", True, red)
    screen.blit(text_surface, (340, height // 2 - 370))

    variable.draw(width // 2 - 175, height // 2  + 50)
    # my_font = pygame.font.Font(None, 100, bold=True)
    # text_surface = my_font.render(f"print({variable.name}) = {variable.value}", True, red)
    # screen.blit(text_surface, (230, height // 2 - 270))

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

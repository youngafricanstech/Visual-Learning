import pygame
import sys
from tkinter import Tk, Label, Button, Listbox, Scrollbar

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reverse Fruits List")

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

# Initial unordered list of fruits
unordered_fruits = ["Orange", "Apple", "Banana", "Grapes", "Pineapple", "Mango", "Cherry", "Kiwi", "Watermelon", "Strawberry", "Peach"]
fruits_data = Fruits(unordered_fruits)

# Function to update the listbox
# def update_listbox():
#     listbox.delete(0, "end")
#     for i, fruit in enumerate(fruits_data.fruits):
#         listbox.insert("end", f"{i}: {fruit.name}")

# Function to reverse the list
def reverse_list():
    fruits_data.fruits = list(reversed(fruits_data.fruits))
    # update_listbox()

# Create Tkinter window
root = Tk()
root.title("Reverse Fruits List GUI")

# Button to reverse the list
reverse_button = Button(root, text="Reverse List", command=reverse_list, font=("Arial", 16))
reverse_button.pack()

# # Listbox to display fruits
# listbox = Listbox(root, selectmode="single", height=1, width=30, font=("Arial", 16))
# listbox.pack()

# # Scrollbar for the listbox
# scrollbar = Scrollbar(root, command=listbox.yview, orient="horizontal")
# scrollbar.pack()

# Set the geometry of the Tkinter window
root.geometry("400x250+350+330")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)

    # Draw a bar to wrap the list
    pygame.draw.rect(screen, blue, (10, 10, width - 20, 100))

    # Draw all fruits in horizontal columns of five
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

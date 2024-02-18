import pygame
import sys
import ast  # Import the ast module for literal_eval
from tkinter import Tk, Label, Button, Entry, Scrollbar, Listbox

# Initialize pygame
pygame.init()

# Set up display
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Person Information Dictionary")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Person class
class Person:
    def __init__(self, first_name, last_name, age, location, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.location = location
        self.gender = gender

    def display_info(self):
        return f"First Name: {self.first_name}, Last Name: {self.last_name}, Age: {self.age}, Location: {self.location}, Gender: {self.gender}"

# Initial dictionary of persons
persons = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 20,
    "location": "Los Angeles"
}

# Function to handle update button click
def update_command():
    command = update_entry.get().strip()
    try:
        # Use ast.literal_eval to safely evaluate the input as a dictionary literal
        update_dict = ast.literal_eval(command)
        
        # Check if the input is a dictionary
        if not isinstance(update_dict, dict):
            raise ValueError("Invalid input. Please provide a valid dictionary.")

        persons.update(update_dict)
        result_label.config(text="Dictionary updated with the provided key-value pairs.", fg=blue)
        update_listbox()
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")

def update_listbox():
    person_listbox.delete(0, "end")
    person_info = Person(
        persons["first_name"],
        persons["last_name"],
        persons["age"],
        persons["location"],
        persons.get("Gender", "N/A")  # Handle the case where "Gender" may not exist in the dictionary
    ).display_info()
    person_listbox.insert("end", person_info)

# Create Tkinter window
root = Tk()
root.title("Person Information Dictionary GUI")

# Entry for update command
update_entry_label = Label(root, text="Enter key-value pairs enclosed in curly braces (e.g., {'new_key': 'new_value'}):", font=("Arial", 16), fg="blue")
update_entry_label.pack()
update_entry = Entry(root, font=("Arial", 16))
update_entry.pack()

# Button to execute update command
update_button = Button(root, text="Execute update", command=update_command, font=("Arial", 16))
update_button.pack()

# Listbox to display persons
person_listbox = Listbox(root, font=("Arial", 16), width=60, height=10)
person_listbox.pack()

# Set up scrollbar for the listbox
scrollbar = Scrollbar(root, command=person_listbox.yview)
scrollbar.pack(side="right", fill="y")
person_listbox.config(yscrollcommand=scrollbar.set)

# Label to display result or error messages
result_label = Label(root, text="", fg="black", font=("Arial", 16))
result_label.pack()

# Set the geometry of the Tkinter window
root.geometry("700x400+350+350")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update screen
    screen.fill(white)
    pygame.draw.rect(screen, blue, (10, 10, width - 20, 190))

    # Draw the person information in a vertical list
    font = pygame.font.Font(None, 32)
    person_info = Person(
        persons["first_name"],
        persons["last_name"],
        persons["age"],
        persons["location"],
        persons.get("Gender", "N/A")  # Handle the case where "Gender" may not exist in the dictionary
    ).display_info()
    text = font.render(person_info, True, white)
    screen.blit(text, (20, 20))

    # Update display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

    # Update Tkinter window
    root.update_idletasks()
    root.update()

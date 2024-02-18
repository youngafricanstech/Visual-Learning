import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1100, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Static F")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up colors
red = (255, 0, 0)
# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)


# Set up colors
red = (255, 0, 0)



# Define the dimensions of the red rectangular box
box_width, box_height = 560, 70  # Adjusted box width to occupy 60% of the screen width
box_rect = pygame.Rect(width - box_width - 80, 110, box_width, box_height)  # Moved forward to almost touch the right edge

# List of fruit items
fruits = ["Apple", "Banana", "Orange", "Grapes", "Cherry"]

# Font setup
font = pygame.font.Font(None, 36)

# Function to draw a red rectangular box
def draw_red_box():
    pygame.draw.rect(window, red, box_rect)

# Function to draw a jumping object with the current item
def draw_jumping_object(x, y, current_item):
    square_size = 40
    pygame.draw.rect(window, (0, 34, 251), (x - square_size // 2 - 10, y - square_size // 2, square_size + 33   , square_size - 15))

    # Draw the word "fruit" on top of the square
    font = pygame.font.Font(None, 45)  # Change 30 to your desired font size
    font.set_bold(True)  # Make the font bolder

    text_surface = font.render("fruit", True, (255, 243, 0))
    text_rect = text_surface.get_rect(center=(x, y - 30))
    window.blit(text_surface, text_rect)
    

    bold_font = pygame.font.Font(pygame.font.get_default_font(), 18, bold=True)
    text = bold_font.render(current_item, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y - 10))
    window.blit(text, text_rect)


def draw_printing_object(x, y, current_item):
    square_size = 40
    # pygame.draw.rect(window, (0, 34, 251), (x - square_size // 2 - 10, y - square_size // 2, square_size + 33   , square_size - 15))

    # Draw the word "fruit" on top of the square
    font = pygame.font.Font(None, 35)  # Change 30 to your desired font size
    font.set_bold(True)  # Make the font bolder

    text_surface = font.render("print", True, (0,0,255))
    text_rect = text_surface.get_rect(center=(x  + 80, y + 180))
    window.blit(text_surface, text_rect)
    
    text_surface = font.render("(fruit)", True, (255,255,0))
    text_rect = text_surface.get_rect(center=(x + 153, y + 180))
    window.blit(text_surface, text_rect)
    

    bold_font = pygame.font.Font(pygame.font.get_default_font(), 18, bold=True)
    text = bold_font.render(current_item, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x + 160, y + 160))
    window.blit(text, text_rect)


# Main game loop
x_position = box_rect.left + box_width // len(fruits) * 0.3  # Start at the position of the first item
y_position = box_rect.centery - 50  # Adjusted y_position higher
speed = 2
jump_height = 50
current_fruit_index = 0
current_item_displayed = fruits[current_fruit_index]

jumping = False
target_x = 0

last_jump_time = time.time()

# Initial dimensions of the F
f_width = 20
f_height = 200
f_x = 50
f_y = 100

# Animation parameters
stretch_factor = 5
animation_speed = 2  # seconds per stretch

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)


loop_counter = 0
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill(white)


     # Draw the red rectangular box
    draw_red_box()

    # Draw fruit items inside the box horizontally
    item_spacing = box_width // len(fruits)  # Adjusted calculation
    for i, fruit in enumerate(fruits):
        text = font.render(fruit, True, (0, 0, 0))
        text_rect = text.get_rect(center=(box_rect.left + item_spacing * (i + 0.5), box_rect.centery))
        window.blit(text, text_rect)

    # Jump to the next item every 2 seconds
    if time.time() - last_jump_time > 4 and current_fruit_index < len(fruits) - 1:
        last_jump_time = time.time()
        current_fruit_index += 1
        current_item_displayed = fruits[current_fruit_index]
        jumping = True
        target_x = box_rect.left + item_spacing * (current_fruit_index + 0.3)

    # Update the x-position during the jump
    if jumping:
        if x_position < target_x:
            x_position += speed
            if x_position >= target_x:
                x_position = target_x
                jumping = False
        elif x_position > target_x:
            x_position -= speed
            if x_position <= target_x:
                x_position = target_x
                jumping = False

   

        current_time = time.time() % animation_speed
        current_width = f_width + 300 + (current_time / animation_speed) * (stretch_factor - 1) * f_width
        # Draw animated F line
        pygame.draw.rect(window, black, (f_x, f_y, int(current_width), 20))  # Horizontal line 2
        
    bold_font = pygame.font.Font(pygame.font.get_default_font(), 30, bold=True)
    bold_text = bold_font.render(f"Loop: {current_fruit_index + 1}", True, black)
    window.blit(bold_text, (70, 70))


    pygame.draw.rect(window, black, (f_x, f_y, int(100), 20))  # Horizontal line 1
    pygame.draw.rect(window, black, (f_x, f_y, 20, f_height))  # Vertical line
    pygame.draw.line(window, black, (50, 186), (120, 186), 20) 
        


    # Draw the jumping object with the current item
    draw_jumping_object(int(x_position), y_position, current_item_displayed)
    draw_printing_object(180, y_position, current_item_displayed)



    bold_font = pygame.font.Font(pygame.font.get_default_font(), 86, bold=True)

    bold_text = bold_font.render("O", True, black)
    window.blit(bold_text, (110, 116))

    bold_font = pygame.font.Font(pygame.font.get_default_font(), 116, bold=True)

    bold_text = bold_font.render("r", True, black)
    window.blit(bold_text, (170, 90))
    yellow = (255, 243, 0)


    # Fruit variable
    font_size = 60
    bold_font = pygame.font.Font(pygame.font.get_default_font(), font_size, bold=True)

    # Render text with black outline
    text_surface_outline = bold_font.render("fruit", True, black)
    text_rect_outline = text_surface_outline.get_rect(topleft=(250 - 2, 130 - 2))
    window.blit(text_surface_outline, text_rect_outline)

    # Render actual text
    bold_text = bold_font.render("fruit", True, yellow)
    text_rect = bold_text.get_rect(topleft=(250, 130))
    window.blit(bold_text, text_rect)
    # fruit variable ends here

    # draw a vertical line downwards here
    vertical_line_start = (305, 100)
    vertical_line_end = (305, 135)  # Adjust the end position as needed
    vertical_line_width = 8  # Adjust the width of the line
    pygame.draw.line(window, (0,255,0), vertical_line_start, vertical_line_end, vertical_line_width)


    # draw a second vertical line downwards here
    vertical_line_start = (305, 180)
    vertical_line_end = (305, 264)  # Adjust the end position as needed
    vertical_line_width = 8  # Adjust the width of the line
    pygame.draw.line(window, (0,255,0), vertical_line_start, vertical_line_end, vertical_line_width)



   # make this line to stretch to the location of the draw_jumping_object each time it moves
    horizontal_line_start = (304, 100)  # Adjusted the start position for alignment
    horizontal_line_end = (int(x_position), 100)  # Adjusted the end position for length based on x_position
    horizontal_line_height = 8 # Adjust the height of the line
    pygame.draw.line(window, black, horizontal_line_start, horizontal_line_end, horizontal_line_height)



    bold_font = pygame.font.Font(pygame.font.get_default_font(), 46, bold=True)
    bold_text = bold_font.render("in", True, black)
    window.blit(bold_text, (415, 130))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()


import pygame
import joblib
import numpy as np
from math import sin, cos

# Load the trained machine learning model
model = joblib.load("Rotation_Model.pkl")

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
neon_blue = (0, 255, 255)  # Neon Blue

WIDTH, HEIGHT = 800, 600  # Screen dimensions

# Button settings (Top Right Corner)
button_width, button_height = 150, 40
button_x, button_y = WIDTH - button_width - 20, 20  # Top Right Position

# Pygame settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rotating ASCII Donut with ML')
font = pygame.font.SysFont('Arial', 18, bold=True)
button_font = pygame.font.SysFont('Arial', 20, bold=True)
speed_font = pygame.font.SysFont('Arial', 14, bold=True)  # Font for speed display

# ASCII Donut settings
x_sep, y_sep = 10, 20
rows = HEIGHT // y_sep
columns = WIDTH // x_sep
screen_size = rows * columns

x_offset = columns // 2
y_offset = rows // 2

A, B = 0, 0  # Rotation angles
theta_step, phi_step = 10, 1

chars = '.,-~:;=!*#$@'  # ASCII luminance characters

# Default values for user interaction
default_speed = 1.5
default_luminance = 3
speed_input, luminance_input = default_speed, default_luminance

# Track whether the reset button is clicked
reset_pressed = False

# Function to display text at specified coordinates
def text_display(letter, x, y):
    text = font.render(str(letter), True, white)
    screen.blit(text, (x, y))

# Function to draw a neon blue reset button in the top right corner
def draw_button():
    pygame.draw.rect(screen, neon_blue, (button_x, button_y, button_width, button_height), border_radius=10)
    text = button_font.render("Reset Speed", True, black)  # Black text for contrast
    screen.blit(text, (button_x + 15, button_y + 10))

# Function to display the current speeds in the bottom left corner
def display_speed(A_step, B_step):
    speed_text = f"Angular Speed: A = {A_step:.3f}, B = {B_step:.3f}"
    text = speed_font.render(speed_text, True, white)
    screen.blit(text, (10, HEIGHT - 20))  # Bottom left corner position

run = True
dragging = False
last_mouse_pos = (0, 0)

while run:
    screen.fill(black)

    # Predict rotation speed adjustments using the ML model
    prediction = model.predict(np.array([[speed_input, luminance_input]]))
    A_step, B_step = prediction[0]

    # Z-buffer and background buffer
    z = [0] * screen_size
    b = [' '] * screen_size

    # Generate the 3D donut and project it to 2D
    for j in range(0, 628, theta_step):
        for i in range(0, 628, phi_step):
            sinA, cosA = sin(A), cos(A)
            sinB, cosB = sin(B), cos(B)
            sini, cosi = sin(i), cos(i)
            sinj, cosj = sin(j), cos(j)

            h = cosj + 2  # Distance to donut center
            D = 1 / (sini * h * sinA + sinj * cosA + 5)  # Depth calculation
            t = sini * h * cosA - sinj * sinA

            x = int(x_offset + 40 * D * (cosi * h * cosB - t * sinB))
            y = int(y_offset + 20 * D * (cosi * h * sinB + t * cosB))

            o = int(x + columns * y)  # 1D index for 2D screen buffer
            N = int(8 * ((sinj * sinA - sini * cosj * cosA) * cosB - sini * cosj * sinA - sinj * cosA - cosi * cosj * sinB))

            if 0 <= y < rows and 0 <= x < columns and D > z[o]:
                z[o] = D
                b[o] = chars[max(0, min(N, len(chars) - 1))]

    # Render each character to the screen
    x_start, y_start = 0, 0
    for i in range(len(b)):
        if i % columns == 0 and i != 0:  # Move to next line
            y_start += y_sep
            x_start = 0
        text_display(b[i], x_start, y_start)
        x_start += x_sep

    # Update rotation angles using ML-predicted values
    A += A_step
    B += B_step

    # Draw reset button
    draw_button()

    # Display the current speeds in the bottom left corner
    display_speed(A_step, B_step)

    pygame.display.update()

    # Event handling (mouse interaction)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                mouse_x, mouse_y = event.pos

                # Check if reset button was clicked (but don't reset yet)
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    reset_pressed = True  # Mark the button as pressed

                dragging = True  # Allow dragging regardless of where clicked
                last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left-click release
                mouse_x, mouse_y = event.pos

                # If mouse is released over the reset button, reset the speed
                if reset_pressed and button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    speed_input, luminance_input = default_speed, default_luminance
                    print("🔄 Reset Speed to Default!")

                reset_pressed = False  # Reset the button state
                dragging = False  # Stop dragging

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                x, y = event.pos
                dx = x - last_mouse_pos[0]
                dy = y - last_mouse_pos[1]
                speed_input += dx * 0.01
                luminance_input += dy * 0.01
                last_mouse_pos = event.pos

pygame.quit()

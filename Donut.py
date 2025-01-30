import pygame 
import asyncio
from math import sin, cos

pygame.init()

# Colors and display settings
white = (255, 255, 255)
black = (0, 0, 0)

WIDTH = 800  # Screen width
HEIGHT = 600  # Screen height

x_sep = 10  # Horizontal character spacing
y_sep = 20  # Vertical character spacing

rows = HEIGHT // y_sep
columns = WIDTH // x_sep
screen_size = rows * columns

x_offset = columns // 2
y_offset = rows // 2

A, B = 0, 0  # Rotation angles

theta_step = 10
phi_step = 1

chars = '.,-~:;=!*#$@'  # Luminance characters

# Pygame screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rotating ASCII Donut')
font = pygame.font.SysFont('Arial', 18, bold=True)

# Function to display text at specified coordinates
def text_display(letter, x, y):
    text = font.render(str(letter), True, white)
    screen.blit(text, (x, y))

# Main loop
run = True
dragging = False
last_mouse_pos = (0,0)

async def main():
    global run, dragging, last_mouse_pos, A, B

    while run:
        screen.fill(black)

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

        # Update rotation angles
        A += 0.04
        B += 0.02

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left-click
                    dragging = True
                    last_mouse_pos =  event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Left-click
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    x, y = event.pos
                    dx = x - last_mouse_pos[0]
                    dy = y - last_mouse_pos[1]
                    A += dx * 0.01
                    B += dy * 0.01
                    last_mouse_pos = event.pos

    await asyncio.sleep(0)                 

asyncio.run(main())

pygame.quit()
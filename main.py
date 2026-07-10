import json

import pygame

pygame.init()

running = True
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Raycaster")
clock = pygame.time.Clock()


def load_map(map_name):
    with open(map_name, "r") as f:
        return json.load(f)


class Wall:
    def __init__(self, color, grid_x, grid_y) -> None:
        self.rect_var = self.rect(grid_x, grid_y)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color

    def rect(self, grid_x, grid_y):
        rect = pygame.Rect(grid_x, grid_y, 50, 50)

        return rect


x = 0
y = 0
walls = []

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                grid = load_map("map.json")
                for row_index, row in enumerate(grid):
                    for col_index, value in enumerate(row):
                        x = col_index * 50
                        y = row_index * 50

                        if value == 1:
                            print(f"Wall found at X: {x}, Y: {y}")
                            walls.append(Wall((255, 255, 255), x, y))

    window.fill((40, 40, 40))

    for wall in walls:
        rect = wall.rect_var
        pygame.draw.rect(window, wall.color, rect)

    pygame.display.flip()

pygame.quit()

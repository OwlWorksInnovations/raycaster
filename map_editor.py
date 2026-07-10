import json

import pygame

pygame.init()

running = True
width = 800
height = 600
grid_size = 50
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raycaster Map Editor")
clock = pygame.time.Clock()


class Wall:
    def __init__(self, id, grid_x, grid_y, color) -> None:
        self.id = id
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color


class Cell:
    def __init__(self, grid_x, grid_y, rect_x, rect_y, cell_size) -> None:
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_rect = self.make_rect(rect_x, rect_y, cell_size)
        self.has_wall = False
        self.draw(self.cell_rect)

    def make_rect(self, rect_x, rect_y, cell_size):
        rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
        return rect

    def draw(self, cell_rect):
        pygame.draw.rect(window, (100, 100, 100), cell_rect, 1)


lines = []
cells = []


def get_mouse_pos():
    mouse_pos = pygame.mouse.get_pos()
    end_pos = (mouse_pos[0] + grid_size, mouse_pos[1])
    return mouse_pos, end_pos


def draw_grid():
    block_size = grid_size
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            cell = Cell(x, y, x, y, block_size)
            cells.append(cell)


while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            grid = []
            GRID_HEIGHT = width // grid_size
            GRID_WIDTH = height // grid_size

            for y in range(GRID_HEIGHT):
                row = []
                for x in range(GRID_WIDTH):
                    cell = cells[y * GRID_WIDTH + x]
                    row.append(1 if cell.has_wall else 0)
                grid.append(row)

            with open("map.json", "w") as f:
                json.dump(grid, f, indent=4)

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            id = len(lines) + 1
            start_pos, end_pos = get_mouse_pos()
            wall_cell_x = 0
            wall_cell_y = 0
            has_wall = False
            for cell in cells:
                if cell.cell_rect.collidepoint(pygame.mouse.get_pos()):
                    if not cell.has_wall:
                        wall_cell_x = cell.grid_x
                        wall_cell_y = cell.grid_y
                        cell.has_wall = True
                    else:
                        has_wall = True

            if not has_wall:
                wall = Wall(str(id), wall_cell_x, wall_cell_y, (255, 0, 0))
                lines.append(wall)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if len(lines) > 0:
                    lines.pop()

    window.fill((40, 40, 40))

    draw_grid()

    for wall in lines:
        x_pos = 0
        y_pos = 0

        for x in range(wall.grid_x):
            for y in range(wall.grid_y):
                x_pos = x
                y_pos = y

        rect = pygame.Rect(x_pos, y_pos, 50, 50)
        pygame.draw.rect(window, wall.color, rect)

    pygame.display.flip()

pygame.quit()

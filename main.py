import pygame
import sys
from enum import Enum
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
DARK_BLUE = (4, 2, 115)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (75, 0, 110)
RED = (255, 0, 0)

FPS = 60
TILESIZE = 16
WIDTH = 10
HEIGHT = 20

start_x = 20
start_y = 20
offset = 2
move_interval = 5

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface([TILESIZE, TILESIZE]) 
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
        self.color = color
        self.image.fill(color)

    def set_color(self, color):
        self.color = color

    def update(self):
        self.image.fill(self.color)

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect.topleft)

class Block():
    def initialize_i(self):
        self.color = CYAN
        
        self.locations = []
        self.origin = (WIDTH / 2, 0)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0] - 1, self.origin[1]))
        self.locations.append((self.origin[0] + 1, self.origin[1]))
        self.locations.append((self.origin[0] + 2, self.origin[1]))

    def initialize_j(self):
        self.color = DARK_BLUE
        
        self.locations = []
        self.origin = (WIDTH / 2, 1)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0] - 1, self.origin[1]))
        self.locations.append((self.origin[0] + 1, self.origin[1]))
        self.locations.append((self.origin[0] - 1, self.origin[1] - 1))

    def initialize_l(self):
        self.color = ORANGE
        
        self.locations = []
        self.origin = (WIDTH / 2, 1)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0] - 1, self.origin[1]))
        self.locations.append((self.origin[0] + 1, self.origin[1]))
        self.locations.append((self.origin[0] + 1, self.origin[1] - 1))

    def initialize_o(self):
        self.color = YELLOW
        
        self.locations = []
        self.origin = (WIDTH / 2, 0)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0] - 1, self.origin[1]))
        self.locations.append((self.origin[0] - 1, self.origin[1] + 1))
        self.locations.append((self.origin[0], self.origin[1] + 1))

    def initialize_s(self):
        self.color = GREEN
        
        self.locations = []
        self.origin = (WIDTH / 2, 0)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0] + 1, self.origin[1]))
        self.locations.append((self.origin[0], self.origin[1] + 1))
        self.locations.append((self.origin[0] - 1, self.origin[1] + 1))

    def initialize_t(self):
        self.color = PURPLE
        
        self.locations = []
        self.origin = (WIDTH / 2, 1)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0], self.origin[1] - 1))
        self.locations.append((self.origin[0] + 1, self.origin[1]))
        self.locations.append((self.origin[0] - 1, self.origin[1]))

    def initialize_z(self):
        self.color = RED
        
        self.locations = []
        self.origin = (WIDTH / 2, 0)
        
        self.locations.append(self.origin)
        self.locations.append((self.origin[0], self.origin[1] + 1))
        self.locations.append((self.origin[0] - 1, self.origin[1]))
        self.locations.append((self.origin[0] + 1, self.origin[1] + 1))
    
   
    
    def __init__(self, type, grid, speed):
        self.initialize_dict = {
            'I': self.initialize_i,
            'J': self.initialize_j,
            'L': self.initialize_l,
            'O': self.initialize_o,
            'S': self.initialize_s,
            'T': self.initialize_t,
            'Z': self.initialize_z,
        }

        if type in self.initialize_dict:
            self.initialize_dict[type]()

        self.grid = grid
        self.stopped = False
        self.initial_speed = speed
        self.speed = speed

        self.can_fall = True
        self.fall_time = pygame.time.get_ticks()

        self.game_over = False
        for i in self.locations:
            if self.grid.data[int(i[1])][int(i[0])].color != WHITE:
                self.game_over = True

    def valid_block(self, locations):
        for i in locations:
            if i[0] < 0 or i[0] > WIDTH - 1:
                return False
            if i[1] < 0 or i[1] > HEIGHT - 1:
                return False
            if self.grid.data[int(i[1])][int(i[0])].color != WHITE and not i in self.locations:
                return False
        return True
            
    def reset_colors(self):
        for i in self.locations:
            self.grid.data[int(i[1])][int(i[0])].color = WHITE

    def move_down(self):
        updated_locations = []
        for i in self.locations:
            updated_locations.append((i[0], i[1] + 1))
        if not self.valid_block(updated_locations):
            self.stopped = True
            return
        self.reset_colors()
        self.locations = updated_locations
        self.origin = (self.origin[0], self.origin[1] + 1)

    def move_horizontal(self, right):
        updated_locations = []
        for i in self.locations:
            if right == True:
                updated_locations.append((i[0] + 1, i[1]))
            else:
                updated_locations.append((i[0] - 1, i[1]))
        if not self.valid_block(updated_locations):
            return
        self.reset_colors()
        self.locations = updated_locations
        if right == True:
            self.origin = (self.origin[0] + 1, self.origin[1])
        else:
            self.origin = (self.origin[0] - 1, self.origin[1])

    def rotate(self, clockwise):
        updated_locations = []
        for i in self.locations:
            if clockwise:
                x2 = i[1] + self.origin[0] - self.origin[1]
                y2 = self.origin[0] + self.origin[1] - i[0]
            else:
                x2 = self.origin[0] + self.origin[1] - i[1]
                y2 = i[0] + self.origin[1] - self.origin[0]
            updated_locations.append((x2, y2))
        if not self.valid_block(updated_locations):
            return
        self.reset_colors()
        self.locations = updated_locations

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.speed = 250
        else:
            self.speed = self.initial_speed
        
    def cool_downs(self):
        current_time = pygame.time.get_ticks()
        elapsed_fall_time = current_time - self.fall_time
        if elapsed_fall_time >= self.speed:
            self.can_fall = True

    def line_clear(self):
        line_clear_rows = []
        potential_rows = [i[1] for i in self.locations]
        for row in potential_rows:
            is_line_clear = True
            for tile in self.grid.data[int(row)]:
                if tile.color == WHITE:
                    is_line_clear = False
                    break
            if is_line_clear == True:
                line_clear_rows.append(row)
        
        for row in line_clear_rows:
            for tile in self.grid.data[int(row)]:
                tile.color = WHITE
        
        if not line_clear_rows:
            return
        
        row_falling = min(line_clear_rows) - 1
        while row_falling != -1:
            self.fall_down(row_falling)
            row_falling -= 1

    def fall_down(self, row):
        for index in range(WIDTH):
            current_row = row
            row_below = row + 1
            while row_below < HEIGHT and self.grid.data[int(row_below)][index].color == WHITE:
                # Move the tile down
                self.grid.data[int(row_below)][index].color = self.grid.data[int(current_row)][index].color
                self.grid.data[int(current_row)][index].color = WHITE
                current_row = row_below  # Update row to the new position
                row_below += 1  # Check the next row below
            
    def update(self):
        for i in self.locations:
            self.grid.data[int(i[1])][int(i[0])].color = self.color
        
        self.input()
        if self.can_fall:
            self.move_down()
            self.fall_time = pygame.time.get_ticks()
            self.can_fall = False

        self.cool_downs()

class Grid:
    def __init__(self):
        self.data = []
        current_x = start_x
        current_y = start_y
        for i in range(HEIGHT):
            row = []
            current_x = start_x
            current_y += TILESIZE + offset
            for j in range(WIDTH):
                tile = Tile((current_x, current_y), WHITE)
                row.append(tile)
                current_x += TILESIZE + offset
            self.data.append(row)

    def draw(self, surface):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                self.data[i][j].draw(surface)

def get_next_block():
    rand = random.randint(0, 6)
    if rand == 0:
        return 'I'
    elif rand == 1:
        return 'J'
    elif rand == 2:
        return 'L'
    elif rand == 3:
        return 'O'
    elif rand == 4:
        return 'S'
    elif rand == 5:
        return 'T'
    elif rand == 6:
        return 'Z'

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 400, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tetris")
    grid = Grid()
    block = Block('I', grid, 1000)
    next_block = 'I'

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    block.move_horizontal(True)
                if event.key == pygame.K_LEFT:
                    block.move_horizontal(False)
                if event.key == pygame.K_x:
                    block.rotate(True)
                if event.key == pygame.K_z:
                    block.rotate(False)
                
        screen.fill(BLACK)
        
        grid.draw(screen)
        block.update()

        if block.stopped == True:
            block.line_clear()
            block = Block(next_block, grid, 1000)
            if block.game_over == True:
                running = False
                print("game over")
            next_block = get_next_block()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

        
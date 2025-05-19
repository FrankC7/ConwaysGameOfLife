import pygame as pg

dead_color = (0, 0, 0)
alive_color = (255, 255, 255)
window_width = 0
window_height = 0
number_columns = 50
number_rows = 50

#frequency at which generations are simulated in ms
update_interval = 200
last_update_time = 0

pausedState = True
generation_number = 0

def main():

    #initializing pygame
    pg.init()

    #window icon and title setup
    activeIcon = pg.image.load("assets/CellularBlock.png")
    pausedIcon = pg.image.load("assets/Barrier.png")
    pg.display.set_icon(pausedIcon)
    pg.display.set_caption("Conway's Game of Life")

    #window screen setup
    screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
    screen.fill(dead_color)

    #clock setup
    clock = pg.time.Clock()
    clock.tick(60)

    #grid setup
    grid = [[0 for _ in range(number_columns)] for _ in range(number_rows)]

    #main game code
    quit = False
    while not quit:

        #determining how many cells should be on the screen
        window_width, window_height = screen.get_size()
        cell_width = window_width // number_columns
        cell_height = window_height // number_rows
        cell_size = min(cell_width, cell_height)

        #setting grid offsets
        x_offset = (window_width - number_columns * cell_size) // 2
        y_offset = (window_height - number_rows * cell_size) // 2

        #define for generation cycles
        current_time = pg.time.get_ticks()

        #statistics
        population_count = 0

        #events handling
        for event in pg.event.get():
                    
                    #checking if the window gets resized
                    if event.type == pg.VIDEORESIZE:
                        screen = pg.display.set_mode(event.size, pg.RESIZABLE)

                    #checking for mouse clicks or drag
                    elif event.type == pg.MOUSEMOTION:
                         if event.buttons[0]:
                              mouse_x, mouse_y = event.pos
                              column = (mouse_x - x_offset) // cell_size
                              row = (mouse_y - y_offset) // cell_size

                                #flips cells when mouse is dragging over them
                              if 0 <= row < number_rows and 0 <= column < number_columns:
                                   grid[row][column] = 1

                    elif event.type == pg.MOUSEBUTTONDOWN:
                         mouse_x, mouse_y = event.pos
                         column = (mouse_x - x_offset) // cell_size
                         row = (mouse_y - y_offset) // cell_size

                        #toggles between alive and dead
                         if 0 <= row < number_rows and 0 <= column < number_columns:
                              grid[row][column] = 1 - grid[row][column] 

                    #toggle paused state
                    elif event.type == pg.KEYDOWN:
                         if event.key == pg.K_SPACE:
                            global pausedState
                            pausedState = not pausedState
                            if pausedState == True:
                                pg.display.set_icon(pausedIcon)
                            else:
                                pg.display.set_icon(activeIcon)

                    #checking if the window is quit
                    elif event.type == pg.QUIT:
                        quit = True

        #simulate the next generation
        global last_update_time
        global generation_number
        if not pausedState and current_time - last_update_time > update_interval:
            grid = simulateNextGeneration(grid)
            last_update_time = current_time
            generation_number += 1
            population_count = sum(sum(row) for row in grid)
            print("Generation " + str(generation_number))
            print("Population: " + str(population_count) + " / " + str(number_rows * number_columns))
            print("")
            

        #setting the number of rows and columns of cells in the screen
        for row in range(number_rows):
            for column in range(number_columns):
                x = x_offset + column * cell_size
                y = y_offset + row * cell_size
                rect = pg.Rect(x, y, cell_size, cell_size)

                #coloring the cells alive or dead
                if grid[row][column] == 1:
                     color = alive_color
                else:
                     color = dead_color
                pg.draw.rect(screen, color, rect)

                #drawing grid lines
                #pg.draw.rect(screen, (255, 165, 0), rect, 1)
                
        pg.display.flip()

    pg.quit()

def countAliveNeighbors(grid, row, column):
     #finding numbers of rows and columns
     rows = len(grid)
     columns = len(grid[0])
     count = 0

     for i in range(-1, 2):
          for j in range(-1, 2):
               if i == 0 and j == 0:
                    continue
               
               #setting the neighbor rows and columns
               neighbor_row = row + i
               neighbor_column = column + j

               if 0 <= neighbor_row < rows and 0 <= neighbor_column < columns:
                    count += grid[neighbor_row][neighbor_column]
     return count

def simulateNextGeneration(grid):
     rows = len(grid)
     columns = len(grid[0])
     next_grid = [[0 for _ in range(columns)] for _ in range(rows)]

     for row in range(rows):
          for column in range(columns):
               alive = grid[row][column]
               neighbors = countAliveNeighbors(grid, row, column)

               if alive:
                    #stays alive
                    if neighbors in (2, 3):
                         next_grid[row][column] = 1
                    #dies
                    else:
                         next_grid[row][column] = 0
               else:
                    #turns alive
                    if neighbors == 3:
                         next_grid[row][column] = 1
     return next_grid



main()
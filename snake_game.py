# import pygame,sys #import pygame module

# pygame.init()# effectively start entirerty of pygame 
# # create display surface 
# screen = pygame.display.set_mode((400, 500)) #set width of the screen 
# clock = pygame.time.Clock()
# # test_surface = pygame.Surface((100,200))
# # test_surface.fill(pygame.Color("blue"))
# # test_rect = test_surface.get_rect(center = (200,250))
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     # draw all our elements 
#     screen.fill((175,215,70)) #can use rgb or Color()
#     # pygame.draw.rect(screen, pygame.Color("red"),test_rect)
#     # screen.blit(test_surface,test_rect)#position of the surface. specifies top left of the surface. The origin of our display surafce is on the top left. up down left right , same like graph , negative positive axis etc. 
#     pygame.display.update()
#     clock.tick(60) #framerate 60fps
# # how to draw somthing in pygame
#     # surfaces and rectangles 
#     # dsiplay surface: is big canvas the entire game is gonna run on , this is displayed by default. There is only one
#     # VS
#     # Surfaces: Alayer that can display graphics . there can be multiple. not displayed by default. create surafe then put it on screen - import an image, write text or create an empty space. display the surface.

#     # rect: a rectangle that cna be used for drawing, placement, movement, and collisions


# The above is practice code for notes etc. Below is the game code 

# -------------------------------------------------------------------------------

import pygame,sys,random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        """Define all images/parts of the snake"""
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #create a list of 3 vector2 objects - makes it one body for snake 
        self.direction = Vector2(0,0)#initialize direction before player presses key, so snake is stationary
        self.new_block = False #flag to control whether new block should be added 

        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
        
        # add sound below
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')#must use pygame.mixer.Sound >> all of the methods like Sound, Rect etc must be capitalized


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body): #index is the index we are on and block is the block we are going to look at
            # 1.we still need a rect for the positioning 
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            # create a rect and draw a rect
            block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)

            # 2. what direction is the face heading 
            if index == 0:
                screen.blit(self.head,block_rect)#draws head if first block
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)#draws tail if last block
            else:
                # for the parts between head and tail
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:#if both aligned , straight vertical body graphic
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:#if alignied horizontally, horizontal body graphic 
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    # everthing here checks for corners 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)#top left
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)#bottom left
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)#top right
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)#bottom right

    def update_head_graphics(self):
    # subtract one vector by the other 
    # changes head graphics based on movement up, down, left, right 
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        if head_relation == Vector2(-1,0): self.head = self.head_right
        if head_relation == Vector2(0,1): self.head = self.head_up
        if head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        # changes tail graphics based on movement, tail up , down side etc
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        if tail_relation == Vector2(-1,0): self.tail = self.tail_right
        if tail_relation == Vector2(0,1): self.tail = self.tail_up
        if tail_relation == Vector2(0,-1): self.tail = self.tail_down

            
    def move_snake(self):
        if self.new_block == True:
            # adds new block to snake 
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction) # body_copy.insert(0, body_copy[0] + direction). move head forward by dir
            self.body =body_copy[:]
            self.new_block = False #reset flag after adding block
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction) # body_copy.insert(0, body_copy[0] + direction)
            self.body =body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()#play sound

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)#stationary body placement

class FRUIT:
    def __init__(self):
        # create an x and y position
        # draw a square
        self.x = random.randint(0,cell_number - 1)#from x to y , inclusive of y, so we minus 1
        self.y = random.randint(0,cell_number - 1)
        # An easy way to store 2d data - vector. getting values from a vector is always gonna be a float
        self.pos = Vector2(self.x, self.y)# creating a vector
        
    def draw_fruit(self):
        # create rectangle , then draw the rectangle
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x, self.y)
   
class MAIN:
    # initialise objects
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()#move snake forward based on direction
        self.check_collision()#check if ate fruit
        self.check_fail()#check if hit wall

    def draw_elements(self):
        # draws elements , snake , grass , fruit etc
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()


    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit , and add anotehr block to the snake
            self.fruit.randomize() #random fruit placement 
            self.snake.add_block() #sets self.new_block to true if it collides with fruit
            self.snake.play_crunch_sound()#plays crunch sound 

        for block in self.snake.body[1:]:
            # Prevents fruit from spawning on snake body by redoing the randomize function if there is a collision
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # check if snake is outside of the screen and check if snake hits itself
        # if either condition is true it calls game over , and ends the game
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: #only check left and right with ".x"
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        # resets snake position by calling reset() method
        self.snake.reset()

    def draw_grass(self):
        # draws grass in checkerboard pattern
        grass_color = (167,209,61)
        # loop through each row on the grid 
        for row in range(cell_number):
            # checks for even rows
            if row % 2 == 0:
                # loop through each column
                for col in range(cell_number):
                    # draw on evemn columns only to create pattern
                    if col % 2 == 0:
                        # create rectangle with size of one cell
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        # draw rect on screen
                        pygame.draw.rect(screen,grass_color,grass_rect)

            else:
                # for odd rows
                for col in range(cell_number):
                    # only colors odd numbered columns in the row
                    if col % 2 != 0:
                        # calculate position and size of the grass cell
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        # draw on screen
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        # calculate score by subtracting first snake length from current length
        score_text = str(len(self.snake.body) - 3)
        # put score on surface
        score_surface = game_font.render(score_text,True,(56,74,12))#game_font.render(text,aa,color)
        # set position for score
        score_x = int(cell_size *  cell_number - 60)
        score_y = int(cell_size *  cell_number - 40)
        # create rect for score 
        score_rect = score_surface.get_rect(center = (score_x,score_y)) #where we want to place it
        # create apple icon
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        # create background surface
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)#(x,y,w,h)

        # draw rect
        pygame.draw.rect(screen, (167,209,61), bg_rect)
        screen.blit(score_surface,score_rect)#screen.blit(score_surface,position). draw score on screen
        screen.blit(apple,apple_rect)#draw apple on screen
        pygame.draw.rect(screen, (56,74,12), bg_rect,2)#the number you pass in determines the line-width


pygame.mixer.pre_init(44100,-16,2,512)#pre-init for better sound playback, so that it can activate when collision happens without the delay if it wasn't here
pygame.init()
cell_size = 40#size of cells in grid
cell_number = 20#number of cells in a row
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))#creates main game window
clock = pygame.time.Clock()#create clock- controls fps
apple = pygame.image.load("Graphics/apple.png").convert_alpha()#get image and convert_alpha() Converts to format so pyth can work with it better
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)#load font 

SCREEN_UPDATE = pygame.USEREVENT#custom user event
pygame.time.set_timer(SCREEN_UPDATE, 150) #in milliseconds. timer to trigger update

main_game = MAIN()

# main loop, runs until we close game
while True:
    for event in pygame.event.get():#handle all events
        if event.type == pygame.QUIT:#if we click close it exits game
            pygame.quit()
            sys.exit()
        # custom timer
        if event.type == SCREEN_UPDATE:
            main_game.update()#check collisions and updates game state
        # handle keys for snake movement
        if event.type == pygame.KEYDOWN:
            """Key movements and actions"""
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)  
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
             


    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

import pygame,sys,random
from pygame.math import Vector2
pygame.init()

title_font= pygame.font.Font(None,60)
score_font =pygame.font.Font(None,40)
cell_size=30
cell_number=25
GREEN = (173,204,96)
DARK_GREEN = (43,51,24)
offset = 35

class Food:
    def __init__(self,snake_body):
        self.position = self.generate_random_position(snake_body)
    def draw(self):
        food_rect = pygame.Rect(offset+self.position.x*cell_size,offset+self.position.y*cell_size,cell_size,cell_size)
        screen.blit(food_surface,food_rect)
    def generate_random_cell(self):
        x= random.randint(0,cell_number-1)
        y = random.randint(0,cell_number-1)
        return Vector2(x,y)
        
    def generate_random_position(self , snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment= False
        self.wall = pygame.mixer.Sound('assets/Stomach Thumps.mp3')
        self.eat_sound =pygame.mixer.Sound('assets/Cartoon Cowbell.mp3')
    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(offset+segment.x*cell_size,offset+segment.y*cell_size,cell_size,cell_size)
            pygame.draw.ellipse(screen,DARK_GREEN,segment_rect)
    def update(self):
        self.body.insert(0,self.body[0]+self.direction)
        if(self.add_segment==True): 
            self.add_segment = False
        else:
            self.body= self.body[:-1]
    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)

            

class Game:
    def __init__(self):
        self.snake= Snake()
        self.food= Food(self.snake.body)
        self.state = 'running'
        self.score = 0
    def draw(self):
        self.snake.draw()
        self.food.draw()
    def update(self):
        if self.state == 'running':
            self.snake.update()
            self.eat()
            self.check_collision()
            self.check_collison_with_self()
    def eat(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_position(self.snake.body)
            self.snake.add_segment = True  
            self.score+=1
            self.snake.eat_sound.play()
    def check_collision(self):
        if self.snake.body[0].x>=cell_number or self.snake.body[0].x<0 or self.snake.body[0].y>=cell_number or self.snake.body[0].y<0:
            self.game_over()
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_position(self.snake.body)
        self.state = 'stopped'
        self.snake.wall.play()
        self.score=0
    def check_collison_with_self(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

screen = pygame.display.set_mode((2*offset + cell_size*cell_number, 2*offset + cell_size*cell_number))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game = Game()
big_food_surface = pygame.image.load('assets/peach.svg')
food_surface = pygame.transform.scale(big_food_surface,(cell_size,cell_size))
SNAKE_UPDATE= pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,200)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.state == 'stopped':
                game.state = 'running'
            if event.key == pygame.K_UP and game.snake.direction!=Vector2(0,1):
                game.snake.direction = Vector2(0,-1)
                
            if event.key == pygame.K_DOWN and game.snake.direction!=Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
                
            if event.key == pygame.K_RIGHT and game.snake.direction!=Vector2(-1,0):
                game.snake.direction = Vector2(1,0)
                
            if event.key == pygame.K_LEFT and game.snake.direction!=Vector2(1,0):
                game.snake.direction = Vector2(-1,0)
                
            

    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (offset-5,offset-5,cell_size*cell_number+10,cell_size*cell_number+10), 5)
    game.draw()
    title_surface = title_font.render('Snake Game',False,DARK_GREEN)
    score_surface = score_font.render('Score:'+str(game.score),False,DARK_GREEN)
    screen.blit(title_surface,(offset-10,0))
    screen.blit(score_surface,(offset+cell_size*cell_number-100,0))
    pygame.display.update()
    clock.tick(60)

#  bug - if left key and down key are pressed at the same time while snake is moving in upward direction it will
#     change the direction to down which should not happen.
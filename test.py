import pygame, sys, random

def resetball():
    global ball_speed_x ,ball_speed_y
    ball.x = screen_width/2
    ball.y = random.randint(0,screen_height)
    ball_speed_x *= random.choice((1,-1))

def points(winner):
    global cpu_points, player_points, ball_speed_x
    if winner == 'player':
        player_points += 1
    if winner == 'cpu':
        cpu_points += 1
    ball_speed_x*=-1
    

def ball_animation():
        #Change position of the game object
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <=0 or ball.bottom >= screen_height:
        ball_speed_y*= -1
    if ball.left <=0:
        points('player')
        resetball()
    if ball.right>= screen_width:
        points('cpu')
        resetball()
        
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1

def player_animation(event):
    global player_speed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            player_speed = 6
            if player.bottom >= screen_height:
                player_speed = 0
        if event.key == pygame.K_UP:
            player_speed = -6
            if player.top <= 0:
                player_speed = 0

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            player_speed = 0
        if event.key == pygame.K_UP:
            player_speed = 0

def cpu_animation():
    global cpu_speed
    cpu.y += cpu_speed
    if ball.centery >= cpu.centery:
        cpu_speed = 5.7
    if ball.centery <= cpu.centery:
        cpu_speed = -5.7
    
    if cpu.top <=0:
        cpu_top =0
    if cpu.bottom >= screen_height:
        cpu_bottom = screen_height

pygame.init()
info = pygame.display.Info()
# screen_width= info.current_w
# screen_height= info.current_h
screen_width= 1200
screen_height= 800
# pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Pong Wong')
clock = pygame.time.Clock()

#game object
ball= pygame.Rect(0,0,30,30)
ball.center= screen.get_rect().center

cpu = pygame.Rect(0,0,20,100)
cpu.centery= screen.get_rect().centery

player = pygame.Rect(0,0,20,100)
player.midright = screen.get_rect().midright

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 6
cpu_points , player_points = 0,0
score_font = pygame.font.Font(None, 100)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    ball_animation()
    player_animation(event)
    cpu_animation()

    
    #Draw the game object (screen, color , object)
    screen.fill('black')
    cpu_score_surface = score_font.render(str(cpu_points), True, 'red')
    player_score_surface = score_font.render(str(player_points), True, 'red')
    screen.blit(cpu_score_surface, (screen_width/4 ,20))
    screen.blit(player_score_surface, (3*screen_width/4 ,20))
    player.y += player_speed
    pygame.draw.ellipse(screen,'cyan',ball)
    pygame.draw.rect(screen,'white',cpu)
    pygame.draw.rect(screen,'white',player)
    pygame.draw.aaline(screen,'white',screen.get_rect().midtop,screen.get_rect().midbottom)
    
    pygame.display.update()
    clock.tick(60)
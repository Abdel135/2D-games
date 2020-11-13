import pygame
import sys ,random



def exit():    
    pygame.QUIT
    sys.exit()

def draw_floor():
    screen.blit(floor,(floor_pos,H-100))
    screen.blit(floor,(floor_pos+W,H-100))

def creat_pipe():
    height=random.choice(heights)
    top_pipe=pipe.get_rect(midbottom =(W,height-200))
    bottom_pipe=pipe.get_rect(midtop =(W,height))
    #spawn_pipe=pipe.get_rect(center=(W,600))
    return top_pipe,bottom_pipe 

def draw_pipes(pipes):

    for rect in pipes:
        if rect.bottom > H:
            screen.blit(pipe,rect)
        else:
            top_pipe=pygame.transform.flip(pipe,False,True)
            screen.blit(top_pipe,rect)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=5

def collision(pipes):
    for rect in pipes:
        if rect.colliderect(bird_rect) :
            return False 
        if  bird_rect.bottom >= H-100 or  bird_rect.top <=0:
            return False
    return True
            
def rotate(bird):
    rotated=pygame.transform.rotozoom(bird,-falling_speed*1.7,1)
    return rotated

def display_score():
    SCORE_SURFACE=game_font.render(f"SCORE {int(score)}",True,black)
    BEST_SCORE=game_font.render(f"Best Score {int(best_score)}",True,white)
    SCORE_RECT=SCORE_SURFACE.get_rect(center=(100,30))
    BEST_SCORE_RECT=BEST_SCORE.get_rect(center=(270,50))
    if running:
        screen.blit(SCORE_SURFACE,SCORE_RECT)
    else: 
        screen.blit(BEST_SCORE,BEST_SCORE_RECT)
        screen.blit(SCORE_SURFACE,(200,90))
        screen.blit(game_over_surface,game_over_rect)
W=576
H=800

black=(0,0,0)
white=(255,255,255)

gravity=0.5
falling_speed=0
floor_pos=0   

score=0
current_score=0    
best_score=0



pygame.mixer.pre_init(frequency=44100, size= -16, channels=2, buffer=512)
pygame.init()



sound=pygame.mixer.Sound("sound/sfx_wing.wav")
game_font=pygame.font.Font("04B_19.TTF",35)


screen=pygame.display.set_mode((W,H))
clock=pygame.time.Clock()

background=pygame.image.load("assets/background-day.png").convert_alpha()
background=pygame.transform.scale2x(background)

game_over_surface=pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect=game_over_surface.get_rect(center =(W/2,H/2))

floor=pygame.image.load("assets/base.png").convert_alpha()
floor=pygame.transform.scale2x(floor)

bird=pygame.image.load("assets/redbird-midflap.png").convert_alpha()
bird=pygame.transform.scale2x(bird)
bird_rect=bird.get_rect(center = (70,450))
tmp=bird

bird_downflap=pygame.transform.scale2x(pygame.image.load("assets/redbird-downflap.png").convert_alpha())

bird_upflap=pygame.transform.scale2x(pygame.image.load("assets/redbird-upflap.png").convert_alpha())

pipe=pygame.image.load("assets/pipe-green.png")
pipe=pygame.transform.scale2x(pipe)
pipe_rect=pipe.get_rect(center =(W,0))

pipes=[]
heights=[550  ,610,560,400,500,450,510, 300]
 
pipe_generate= pygame.USEREVENT 
score_event=pygame.USEREVENT
pygame.time.set_timer(score_event,2500)
pygame.time.set_timer(pipe_generate,1300)


running=True


while True:
    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not running:
                    running=True
                    bird_rect=bird.get_rect(center = (70,450))
                    pipes.clear()
                    falling_speed=-11
                    score=0
                else:
                    falling_speed=0
                    falling_speed-=11 
                    bird=bird_upflap
                    sound.play()
        if event.type == pipe_generate:
            pipes.extend(creat_pipe())
        
            
        
            
            
    
    screen.blit(background,(0,0))
    if running:
        draw_pipes(pipes)
        move_pipes(pipes)
        rotated_bird=rotate(bird)
        screen.blit(rotated_bird,bird_rect)
        running=collision(pipes)
        score+=0.011
        current_score=score
        if(score > best_score):
            best_score=score
        


    falling_speed+=gravity
    if falling_speed == 0:
        bird=tmp
    if falling_speed > 0 :
        bird=bird_downflap
    bird_rect.centery+=falling_speed
    
    
    draw_floor()
    floor_pos-=3
    if (floor_pos <= -W):
        floor_pos=0

    
    
    display_score()
    pygame.display.update()
    clock.tick(60)
"""Pygame is a set of Python modules designed for writing games.
It is written on top of the excellent SDL library. This allows you
to create fully featured games and multimedia programs in the python
language. The package is highly portable, with games running on
Windows, MacOS, OS X, BeOS, FreeBSD, IRIX, and Linux."""

###########################initialisation code###########################

import pygame
from tkinter import messagebox
import random

pygame.init()#initialising pygame

#creatng game window
window_width=800
window_height=600
window=pygame.display.set_mode((window_width,window_height))#.display method allows you to create game window as per your custom choice
#we pass width and height s co-ordinate form==>(width,height)=(x,y)
pygame.display.set_caption("Snake game by KP")#adding name of window


#showing window, just ike we use root.mainloop() in tkinter
game_over=False

green=(0,255,0)
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
#creating variables 
x1=window_width/2
y1=window_height/2
x1_change=0
y1_change=0
food_x=round(random.randrange(0,window_width-20)/10)*10.0   #-10 as width of snake is 10
food_y=round(random.randrange(0,window_height-20)/10)*10.0
snake_body=[]
length_snake=1
score=0

clock=pygame.time.Clock()   #clock is object of pygame's class ,Clock, is used to control frame rate or speed

########################### main game ###########################



while not game_over:    #while loop for checking if game_over=False
    for event in pygame.event.get():    #for loop for checking event in pygame.event.get()
        if event.type==pygame.QUIT:       
            game_over=True
        #checking for arrow key presse
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x1_change != 10:  
                x1_change = -10
                y1_change = 0
            elif event.key == pygame.K_RIGHT and x1_change != -10:  
                x1_change = 10
                y1_change = 0
            elif event.key == pygame.K_UP and y1_change != 10:  
                x1_change = 0
                y1_change = -10
            elif event.key == pygame.K_DOWN and y1_change != -10: 
                x1_change = 0
                y1_change = 10
    #updating dynamic coordinate
    x1=x1+x1_change
    y1=y1+y1_change
    #restraining snake from going out of window, it should it and game should be over
    if x1>=window_width or x1<0 or y1>=window_height or y1<0:
        messagebox.showinfo("Game Over!","Snake hit the wall!!")
        game_over=True

    window.fill(black)#to avoid white rctange behind the path of snake object  
    
    snake_head=[]
    snake_head.append(x1)
    snake_head.append(y1)

    snake_body.append(snake_head)

    if len(snake_body)>length_snake:
        del snake_body[0]
    #checking if snake hit itself ie, snake_head=anypoint on snake body
    for segment in snake_body[:-1]:
            
            
            if segment==snake_head:
                 messagebox.showinfo("Game Over!","Snake hit its own body!!")
                 game_over=True

    font_style=pygame.font.SysFont(None,50)
    score_text=font_style.render("Score : " +str(score),True,white)
    window.blit(score_text,(10,10))

    #after snake eat food, it should be at another place
    if x1==food_x and y1==food_y:
        #adding randomness to snake's food
        food_x=round(random.randrange(0,window_width-20)/10)*10.0   #-10 as width of snake is 10
        food_y=round(random.randrange(0,window_height-20)/10)*10.0  
        #increasng length of snake
        length_snake+=1
        score+=1
    #adding food item
    pygame.draw.rect(window,red,rect=[food_x,food_y,10,10])     
    pygame.draw.rect(window,green,rect=[x1,y1,10,10])
    """ surface: Surface,
    color: ColorValue,
    rect: RectValue,
    width: int = 0,
    border_radius: int = -1,                paramters of rect 
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
    
    and rect=[x-axis,yaxis,height,width]
    """
    for segment in snake_body:
        pygame.draw.rect(window,green,rect=[segment[0],segment[1],10,10])
    pygame.display.update() #adding changes to game window
    clock.tick(15)  #20 is 20 fps and tick is used for getting frame rates

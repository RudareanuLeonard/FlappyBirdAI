import pygame
import neat
import time
import os
import random

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
    ]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))


BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))



def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

class Bird:
    MAX_ROTATION = 25 #degrees that the bird rotates
    ROT_VEL = 20 #velocity
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        #coordinates
        self.x = x
        self.y = y

        self.tilt = 0 #how much the bird it tilting - 0 because bird is "flat"
        self.tick_count = 0
        self.velocity = 0 #0 bc not moving
        self.height = self.y
        self.img_count = 0
        self.img = BIRD_IMAGES[0] #we always start with the first image, the bird is "flat"


    def jump(self):
        self.velocity = -10
        #this value is negative because our game is an xOy coordinates system, and the top left (0,0) is the Origin. 
        # So, going up is negative velocity, while going down is positive because we are under Ox

        self.tick_count = 0 #how many seconds we've been moving for before change direction
        self.height = self.y

    
    def move(self):
        self.tick_count = self.tick_count + 1 #because we move
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2 #how many pixels we move up/down per frame, s = d/t
        print("DISPLACEMENT =", displacement)
        if displacement > 20: #we can jump maxx of 20 pixels
            displacement = 20
        else:
            displacement = displacement - 2 #going down

        
        #now we modify the position of the bird
        self.y = self.y + displacement

        #tilt the bird
        if displacement > 0:
            self.tilt = -self.MAX_ROTATION
        elif displacement == 0:
            self.tilt = 0
        else:
            self.tilt = self.MAX_ROTATION


    def draw(self, window):
        self.img_count =  self.img_count + 1

        #now we decide what bird image we display
        if self.img_count <= self.ANIMATION_TIME:
            self.img = BIRD_IMAGES[0]
        elif self.img_count >= self.ANIMATION_TIME and self.img_count < self.ANIMATION_TIME * 2:
            self.img = BIRD_IMAGES[1]
        else:
            self.img = BIRD_IMAGES[2]
            self.img_count = 0

        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt)



class Pipe:

    def __init__(self, x):
        self.x = x
        self.y = 0
        self.velocity = 3
        self.BOTTOM_PIPE = PIPE_IMAGE
        self.TOP_PIPE = pygame.transform.rotate(PIPE_IMAGE, 180) #rotate 180 degrees

        self.gap = 80 

        self.bottom_pipe_height = random.randint(30, 250)
        self.top_pipe_height =  WINDOW_HEIGHT - self.bottom_pipe_height - self.gap



    def move(self):
        self.x = self.x - self.velocity

    def collision(self, bird):
        #if bird touch pipe -> collision
        #if bird x == pipe x (but what about pipe width?) then we can check the y axis

        if bird.x == self.x:
            if bird.y in [0, self.bottom_pipe_height] or bird.y in [self.top_pipe_height, WINDOW_HEIGHT]:#collision happens
                return True
        
        return False
        
        
    def draw(self, window):
        window.blit(self.BOTTOM_PIPE, (self.x, self.y))
        window.blit(self.TOP_PIPE, (self.x, self.y))
        






def draw_window(window, bird, pipe):
    window.blit(BG_IMAGE, (0,0))
    bird.draw(window)
    pygame.display.update()
    pipe.draw(window)
    pygame.display.update()

def main():
    START_POS_BIRD_X = 100
    START_POS_BIRD_Y = 100
    
    window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

    bird = Bird(START_POS_BIRD_X, START_POS_BIRD_Y)
    pipe = Pipe(50)


    clock_for_frame = pygame.time.Clock()
    while True:
        clock_for_frame.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
        #bird.move()
        draw_window(window, bird, pipe)


main()
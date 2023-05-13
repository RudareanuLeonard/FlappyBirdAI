import pygame
import neat
import time
import os
import random

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500


PIPE_WIDTH = 50

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
    ]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))


BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

SCORE = 0


CONFIG_FILE_PATH = "./config_file.txt"

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

    
    # def move(self):
    #     self.tick_count = self.tick_count + 1 #because we move
    #     displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2 #how many pixels we move up/down per frame, s = d/t
        
    #     # print("DISPLACEMENT =", displacement)
    #     if displacement > 20: #we can jump maxx of 20 pixels
    #         displacement = 20
    #     else:
    #         displacement = displacement - 2 #going down

        
    #     #now we modify the position of the bird
    #     self.y = self.y + displacement

    #     #tilt the bird
    #     if displacement > 0:
    #         self.tilt = -self.MAX_ROTATION
    #     elif displacement == 0:
    #         self.tilt = 0
    #     else:
    #         self.tilt = self.MAX_ROTATION



    
    def move(self):
        self.tick_count += 1  # Increase the tick count

        # Set displacement and velocity to zero
        displacement = 0
        self.velocity = 0

        # Update the bird's position and tilt
        self.y = self.y + displacement

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
        self.gap = 80
        self.velocity = 3


        bottom_pipe_image_before_resize =  PIPE_IMAGE
        self.bottom_pipe_height = random.randint(10,320) + BASE_IMAGE.get_height()
        # print("BOTTOM = " + str(self.bottom_pipe_height))
        self.bottom_pipe = pygame.transform.scale(bottom_pipe_image_before_resize, (PIPE_WIDTH, self.bottom_pipe_height))


        top_pipe_image_before_resize = pygame.transform.rotate(PIPE_IMAGE, 180)
        self.top_pipe_height = WINDOW_HEIGHT - self.bottom_pipe_height - self.gap
        #print("TOP = " + str(self.top_pipe_height)) 
        self.top_pipe = pygame.transform.scale(top_pipe_image_before_resize, (PIPE_WIDTH, self.top_pipe_height))

    def move(self):
        self.x = self.x - self.velocity

    def draw(self, window, bird):
        window.blit(self.bottom_pipe, (self.x + 2.3*bird.x, WINDOW_HEIGHT - self.bottom_pipe_height))

        pygame.display.update()


        window.blit(self.top_pipe, (self.x + 2.3*bird.x, 0 - self.gap))
        
        pygame.display.update()

        # print("PIPE DRAW")

    def collision(self, bird): # have to work on it
        #if bird touch pipe -> collision
        #if bird x == pipe x (but what about pipe width?) then we can check the y axis
        
        if bird.x >= self.x and bird.x <= self.x + PIPE_WIDTH:
            # print("COLLISION PART1")
            if bird.y <= self.bottom_pipe_height or bird.y >= self.top_pipe_height:
                # print("COLLISION PART2")
                return True
        
        return False



class Base:
    
    def __init__(self, pipe):
        self.velocity = pipe.velocity
        self.image = BASE_IMAGE
        self.width = BASE_IMAGE.get_width()

        #starting pos x
        self.x = 0
        
        #now we are making a circular list of images
        #we'll have 2 images that slowly replace each other for an infinite amount of time, that's why we use x2 for
        self.x2 = self.width

    def move(self):
        self.x = self.x - self.velocity #move first image
        self.x2 = self.x2 - self.velocity #move second image

        if self.x == -self.width: #if first image is gone
            self.x = self.width #we put it to the end
            # print("First image gone")
        
        if self.x2 == -self.width: #if second image is gone
            self.x2 = self.width #we put it to the end
            # print("Second image gone")

        # print("BASE MOVED")

    def draw(self, window):
        window.blit(self.image, (self.x, WINDOW_HEIGHT - self.image.get_height()/2.5))
        pygame.display.update()

        window.blit(self.image, (self.x2, WINDOW_HEIGHT - self.image.get_height()/2.5))
        pygame.display.update()




def draw_window(window, bird, pipes, base):
    window.blit(BG_IMAGE, (0,0))
    bird.draw(window)
    pygame.display.update()
    for pipe in pipes:
        pipe.draw(window, bird)
    pygame.display.update()
    base.draw(window)
    pygame.display.update




def main():

  
    

    START_POS_BIRD_X = 0
    START_POS_PIPE = START_POS_BIRD_X + 300
    pipe = Pipe(START_POS_PIPE)
    START_POS_BIRD_Y = pipe.top_pipe_height - pipe.gap/2 #start bird from gap
    
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    bird = Bird(START_POS_BIRD_X, START_POS_BIRD_Y)

    base = Base(pipe)

    score = 0

    pipe2 = Pipe(START_POS_PIPE + START_POS_PIPE * 0.9)

    pipe3 = Pipe(pipe2.x + START_POS_PIPE * 0.9)

    print("PIPE1 = " + str(pipe.x))
    print("PIPE2 = " + str(pipe2.x))


    pipes = [pipe, pipe2]


    clock_for_frame = pygame.time.Clock()

    #### NEED TO MAKE PIPES COMING CONTINUOUS AND SMOOTHLY ####
    while True:
        clock_for_frame.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
        bird.move()
        # pipe.move()
        base.move()
        for pipe in pipes:
            pipe.move()
            #if bird went through the pipe, we have to create another one and put it in the list
            if pipe.x < 0:
                print("ENTERED HERE")
                pipe = pipe2
                pipe2 = pipe3
                pipe3 = Pipe(pipe2.x + START_POS_PIPE * 0.9)
                pipes = [pipe, pipe2, pipe3]
                
                print("PIPES X'es = " + str(pipe.x) + " " + str(pipe2.x) + " " + str(pipe3.x))

 
        draw_window(window, bird, pipes, base)
        
       






main()



def run():
    values_from_headers = neat.config.Config(neat.DefaultGenome, neat.DefaultSpeciesSet, neat.DefaultStagnation, neat.DefaultReproduction)

    population = neat.Population(values_from_headers)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter() #get the statistics
    population.add_reporter(stats) #dispaly the statistics

    winner = population.run(main, 50)
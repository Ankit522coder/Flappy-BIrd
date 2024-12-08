import pygame 
import sys #to exit the game
import random

pygame.init()
#all variable are insialize in pygame

width = 1100
heigth = 618
screen = pygame.display.set_mode((width,heigth))
clock = pygame.time.Clock()
fps = 40 #frames per second it describe the rendering speed of the game graphics

# images
background = pygame.image.load("background.png").convert_alpha()
bird = pygame.image.load("sprites.png ").convert_alpha()
pipe = pygame.image.load("pipe.jpg").convert_alpha()
rotatedPipe = pygame.image.load("_pipe.jpg").convert_alpha()

# sounds
point = pygame.mixer.Sound("point.mp3")
hit = pygame.mixer.Sound("hit.mp3")
pygame.mixer.music.load("backgroundsong.mp3")
pygame.mixer.music.play(-1)

# Game Caption - to show the game name
pygame.display.set_caption("Flappy Bird by Ankit Nain")  

class Game:
    def __init__(self):
        self.gameOn = True #game start
        self.birdX = 100 #bird coordinate
        self.birdY = 100
        self.pipesX = [width, width+200, width+400, width+600, width+800, width+1000, width+1200]
        self.lowerPipeY = [self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),
            self.randomPipe(),self.randomPipe(),self.randomPipe()]
        self.upperPipeY = [self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),
            self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe()]
        self.gravity = 0
        self.pipeVel = 0
        self.flap = 0
        self.score = 0
        #to rotate the bird when gravity pull the bird
        self.rotateAngle = 0  
        self.isGameOver = False
        self.playSound = True

    def movingPipe(self):
        for i in range(0,7):
            #-ve for to move left side
            self.pipesX[i] += -self.pipeVel 
        
        for i in range(0,7):
            if(self.pipesX[i] < -50):
                self.pipesX[i] = width + 100
                #to generate random pipe who are not visible
                self.lowerPipeY[i] = self.randomPipe() 
                self.upperPipeY[i] = self.randomRotatedPipe()

    def randomPipe(self):
        return random.randrange(int(heigth/2)+50, heigth-200)
    
    def randomRotatedPipe(self):
        return random.randrange(-int(heigth/2)+100, -100)

    def flapping(self):
        self.birdY += self.gravity
        if(self.isGameOver == False):
            self.flap -= 1 #-ve to go up
            self.birdY -= self.flap
    
    def isCollide(self):
        for i in range(0,7): #the seven pipes are touch or not 
            #x coordinate of pipe is grater than or equal to bird x and less than or equal to pipe x + pipe width
            if(self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i]+pipe.get_width()) 
                and ((self.birdY+bird.get_height()-15) >= self.lowerPipeY[i] or 
                (self.birdY) <= self.upperPipeY[i]+rotatedPipe.get_height()-15)):
                    return True
             #bird is in the center of the pipes does not collide   
            elif(self.birdX == self.pipesX[i] and (self.birdY <= self.lowerPipeY[i] and self.birdY >= self.upperPipeY[i])):
                if(self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)
        
        if(self.birdY <= 0):
            return True
        
        elif(self.birdY+bird.get_height() >= heigth):
            self.gravity = 0
            return True
 
        return False

    def gameOver(self):
        if(self.isCollide()):
            self.isGameOver = True
            self.screenText("Game Over!", (255,255,255), 450, 250, 84, "Fixedsys", bold=True)
            self.screenText("Press Enter To Play Again", (255,255,255), 400, 500, 48, "Fixedsys", bold=True)
            self.pipeVel = 0
            self.flap = 0
            self.rotateAngle = -90
            if(self.playSound): #for play sound
                pygame.mixer.Sound.play(hit)
                self.playSound =False

    def screenText(self, text, color, x,y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x,y))
    
    def mainGame(self):
        while self.gameOn:  #infinite loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #for to stop the game when game over
                        if(self.isGameOver == False): 
                            self.pipeVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15
                    #for start new game
                    if event.key == pygame.K_RETURN:
                        newGame = Game()
                        newGame.mainGame()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotateAngle = 0

            # blitting images
            screen.blit(background, (0,0))

            for i in range(0,7):
                # lower Pipe
                screen.blit(pipe, (self.pipesX[i], self.lowerPipeY[i]))
                # upper pipe
                screen.blit(rotatedPipe, (self.pipesX[i], self.upperPipeY[i]))

            screen.blit(pygame.transform.rotozoom(bird, self.rotateAngle, 1), (self.birdX, self.birdY))

            # moving pipe
            self.movingPipe()
            # flapping
            self.flapping()
            # game over
            self.gameOver()
            # displaying score
            self.screenText(str(self.score), (255,255,255), 600, 50, 68, "Fixedsys", bold=True)

            pygame.display.update()
            clock.tick(fps)

falppyBird = Game() #made object 
falppyBird.mainGame() #call the object

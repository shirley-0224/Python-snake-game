import pygame
from pygame.locals import *
import time
import random
SIZE = 40
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        # create a surface
        self.surface = pygame.display.set_mode((1000,800)) #initializing the game window
        self.surface.fill('#765285')
        self.snake = Snake(self.surface,1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()
    def play(self):
        
        self.snake.walk()
        self.apple.draw()
        self.score_Display()
        pygame.display.flip()
        if self.is_collision(self.snake.xdir[0], self.snake.ydir[0],self.apple.xdir, self.apple.ydir):
            sound = pygame.mixer.Sound('apple.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()
        
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.xdir[0],self.snake.ydir[0],self.snake.xdir[i],self.snake.ydir[i]):
                sound = pygame.mixer.Sound('crash.mp3')
                pygame.mixer.Sound.play(sound)
                raise "GAME OVER" 
        
    def play_background_music(self):
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05)

   
    def is_collision(self, x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
        return False
    
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
    
    def run(self):
        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN or event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:   
                        if event.key == K_UP:
                            self.snake.direction = 'up'
                            
                        if event.key == K_DOWN:
                            self.snake.direction = 'down'
                            
                        if event.key == K_RIGHT:
                            self.snake.direction = 'right'
                            
                        if event.key == K_LEFT:
                            self.snake.direction = 'left'
                        
                    
                elif (event.type == QUIT):
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_gameOver()
                self.reset()
                
            time.sleep(0.2)
    def score_Display(self):
        font = pygame.font.SysFont('Lucida Calligraphy', 30)
        score = font.render(f"Score: {self.snake.length}", True, (49,13,57))
        self.surface.blit(score, (800,10))
    
    def show_gameOver(self):
        self.surface.fill('#765285')
        font = pygame.font.SysFont('Cambria', 20)
        end = font.render(f"Game Over! Your Score is: {self.snake.length}", True, (49,13,57))
        self.surface.blit(end, (200,300))
        replay = font.render(f"To play again, press ENTER or SPACE.To exit press ESC", True, (49,13,57))
        self.surface.blit(replay, (200,350))
        pygame.mixer.music.pause()
        pygame.display.flip()
        
        


class Snake:
    def __init__(self, parent_screen, length):

        # loading an image
        self.parent_screen = parent_screen
        self.block = pygame.image.load('body.png').convert()
        self.length = length
        self.xdir = [40]*length
        self.ydir = [40]*length
        self.direction = 'right'
    def draw(self):
        self.parent_screen.fill('#765285')
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.xdir[i], self.ydir[i]))
        pygame.display.flip()
    def increase_length(self):
        self.length += 1
        self.xdir.append(-1)
        self.ydir.append(-1)
    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.xdir[i] = self.xdir[i-1]
            self.ydir[i] = self.ydir[i-1]

        if self.direction == 'up':
            self.move_up()
        elif self.direction == 'down':
            self.move_down()
        elif self.direction == 'left':
            self.move_left()
        elif self.direction == 'right':
            self.move_right()

        self.draw()
    def move_up(self):
        self.ydir[0] -= SIZE
        
    def move_down(self):
        self.ydir[0] += SIZE
        
    def move_left(self):
        self.xdir[0] -= SIZE
        
    def move_right(self):
        self.xdir[0] += SIZE
        
class Apple:
    def __init__(self, parent_screen):
        self.food = pygame.image.load('foods.png').convert()
        self.parent_screen = parent_screen
        self.xdir = SIZE*3
        self.ydir = SIZE*3
    
    def draw(self):
        self.parent_screen.blit(self.food,(self.xdir, self.ydir))
        pygame.display.flip()

    def move(self):
        self.xdir = random.randint(0, 20)*SIZE
        self.ydir = random.randint(0, 15)*SIZE


if __name__ == "__main__":

    game = Game()
    game.run()
    
    

    
    


import pygame
from pygame.sprite import Sprite
import random
from time import sleep

def check_quit(game,event):
    if event.type == pygame.QUIT :
        game.quit = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if game.paused == True :
                game.paused = False
            elif game.paused == False :
                game.paused = True

def check_fire(game,event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE :
            if game.settings.ammo > 0 :
                    bullet = Bullet(game)
                    game.bullets.add(bullet)
                    game.settings.ammo -= 1
                    if game.points >= 5 :
                        game.points -= 5
                        
def throw_rock(game):
    rock = Rock(game)
    game.rocks.add(rock)
                                   
def display(game,title,text,x,y):
    disp = game.font.render(f"{title} - {str(text)}",True,(255,255,255))
    game.screen.blit(disp,(x,y))


class Settings :
    
    def __init__(self):
        self.bgcolour = (0,0,0)
        self.screen_w = 1000
        self.screen_h = 600
        self.ship_health = 3
        self.bullet_speed = 1
        self.bullet_w = 3
        self.bullet_h = 15
        self.bullet_colour = (233,233,233)
        self.ammo = 5
        self.max_ammo = 10
        self.rock_w = (20,100)
        self.rock_h = (20,100)
        self.rock_speed_range = (25,75)
        self.rock_colour = (100,100,100)
        self.cracked_rock_colour = (0,100,100)
        self.special_rock_colour = (0,0,100)

        
class Ship :
    
    def __init__(self,game):
        self.speed = 0.5
        self.img = pygame.image.load('images/ship2_02.bmp')
        self.rect = self.img.get_rect()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.rect.center = self.screen_rect.center
        self.mov_r = False
        self.mov_l = False
        self.mov_u = False
        self.mov_d = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def check_move(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT :
                self.mov_r = True
            if event.key == pygame.K_LEFT :
                self.mov_l = True
            if event.key == pygame.K_UP :
                self.mov_u = True
            if event.key == pygame.K_DOWN :
                self.mov_d = True
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_RIGHT :
                self.mov_r = False
            if event.key == pygame.K_LEFT :
                self.mov_l = False
            if event.key == pygame.K_UP :
                self.mov_u = False
            if event.key == pygame.K_DOWN :
                self.mov_d = False        

    def move(self):
        if self.mov_r == True and self.rect.right < self.screen_rect.right:
            self.x += self.speed
        if self.mov_l == True and self.rect.left > self.screen_rect.left :
            self.x -= self.speed
        if self.mov_u == True and self.rect.top > self.screen_rect.top:
            self.y -= self.speed
        if self.mov_d == True and self.rect.bottom < self.screen_rect.bottom :
            self.y += self.speed 
        self.rect.x , self.rect.y = self.x,self.y
        
        
    def place(self):
        self.screen.blit(self.img,self.rect)
 
       
class Bullet(Sprite):
    def __init__(self,game):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.rect = pygame.Rect(0,0,self.settings.bullet_w,self.settings.bullet_h)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.colour = game.settings.bullet_colour

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        if self.y <0 :
            self.kill()

    def place(self):
        pygame.draw.rect(self.screen,self.colour,self.rect)

       
class Rock(Sprite):
    def __init__(self,game):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.w = random.randint(self.settings.rock_w[0],self.settings.rock_w[1])
        self.h = random.randint(self.settings.rock_h[0],self.settings.rock_h[1])
        self.rect = pygame.Rect(0,0,self.w,self.h)
        self.rect.midtop = game.ship.rect.midtop
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.x = random.randint(0,game.settings.screen_w)
        self.rect.center = (self.x,0)
        self.y = float(self.rect.y)
        self.colour = game.settings.rock_colour
        self.speed = random.randint(self.settings.rock_speed_range[0],self.settings.rock_speed_range[1])
        self.speed = self.speed / 100
        self.health = 2
        self.value = 40000 // (self.w * self.h)

    def update(self,game):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > self.settings.screen_h :
            self.kill()


    def place(self):
        pygame.draw.rect(self.screen,self.colour,self.rect)



class SpaceShooter:
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_w,self.settings.screen_h))
        pygame.display.set_caption("Space shooter")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.cracked_rocks = pygame.sprite.Group()
        self.count_1 = 2000
        self.count_2 = 10000
        self.count_3 = 2000
        self.past_1 , self.past_2 , self.past_3  = 0,0,0
        self.font = pygame.font.Font('Numberlin.ttf',32)
        self.points = 0
        self.coins = 0
        self.flag_01 = 0
        self.paused = False
        self.quit = False
        self.stats = []
        
    def ret(self):
        return[self.points,self.coins]

    def run(self):
        while True :
            for event in pygame.event.get() :
                check_quit(self,event)
                self.ship.check_move(event)
                check_fire(self,event)
            if self.quit == True:
                pygame.quit()
                break
            self.now = pygame.time.get_ticks()
            if self.now - self.past_1  > self.count_1 :
                self.past_1 = self.now
                throw_rock(self)
            if self.now - self.past_2 > self.count_2 :
                if self.flag_01 > 2:
                    self.settings.rock_speed_range = (self.settings.rock_speed_range[0] + 15 ,self.settings.rock_speed_range[1] + 15 )
                    self.ship.speed += 0.25 
                    self.settings.bullet_speed += 0.25
                    self.flag_01 += 1   
                elif self.count_1 > 300 :
                    self.count_1 -= 300
                    self.flag_01 += 1
                self.past_2 = self.now
                if self.flag_01 == 4:
                    self.flag_01 = 0
            if self.now - self.past_3 > self.count_3 :
                self.points += 5
                self.past_3 = self.now
                if self.settings.ammo <self.settings.max_ammo :
                    self.settings.ammo += 1
            try :
                self.screen.fill(self.settings.bgcolour)
            except pygame.error :
                pass
            self.ship.move()
            self.ship.place()
            self.bullets.update()
            self.rocks.update(self)
            collisions = pygame.sprite.groupcollide(self.rocks,self.bullets,False,True)
            for rock in collisions :
                rock.health -= 1  
                if rock.health == 0 :
                    self.coins += rock.value
                    rock.kill()
                r = random.randint(0,4)
                if r == 4 :
                    rock.colour = self.settings.special_rock_colour
                    rock.value += random.randint(25,100)
                else:
                    rock.colour = self.settings.cracked_rock_colour
            for bullet in self.bullets:
                bullet.place()
            for rock in self.rocks :
                rock.place()
            for rock in self.rocks :
                if pygame.Rect.colliderect(self.ship.rect,rock.rect):
                    self.settings.ship_health -= 1
                    rock.kill()
                    sleep(1)
                    for rock in self.rocks :
                        if rock.rect.x + rock.w > self.ship.x and rock.rect.x - rock.w < self.ship.x + 64 :
                            rock.kill()
                        
            if self.settings.ship_health == 0:
                self.quit = True
                 
            display(self,'Ammo',self.settings.ammo,10,10)
            display(self,'Points',self.points,10,40)
            display(self,'Coins',self.coins,10,70)
            display(self,'Lives',self.settings.ship_health,10,100)
              
                
            pygame.display.flip()
                

if __name__ == '__main__' :
    ss = SpaceShooter()
    ss.run()
    a = ss.ret()
    print(a)

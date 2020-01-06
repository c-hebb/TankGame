import pygame

##Class Setup##

#Player Class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, color): 
    super().__init__() 
    if color == 1:
      self.image = pygame.image.load("tank.png")    #SETS PLAYER IMAGE
    elif color == 2:
      self.image = pygame.image.load("tank2.png")    #SETS PLAYER IMAGE

    self.rect = self.image.get_rect()                   #SETS PLAYER BOUNDARY
    self.angle_speed = 0
    self.speed = 0
    self.current_angle = 0
    self.current_image = self.image                    #Created as a copy when rotating the image
    self.position = pygame.math.Vector2(x, y)      #Initial Position of Player
    self.direction = pygame.math.Vector2(0, -1)        #Initial Direction of Player (Facing North)
    self.score = 0
    self.text = font.render("Score: " + str(self.score), 1, pygame.Color("white"))
    self.colliding = 0
    self.lastpos = self.position
    self.startx = x   ##for player reposition
    self.starty = y

  def update(self):
    if self.angle_speed != 0:                          #Checks to see if key is being pressed to move player
      self.direction.rotate_ip(self.angle_speed)       #Changes direction based on angle
      self.current_angle += self.angle_speed           #Changes current angle to align with direction
      
      #Rotates Player Sprite
      orig_rect = self.current_image.get_rect()        #Grabs Original rect and next line rotates it
      rot_image = pygame.transform.rotate(self.current_image, -self.current_angle)
      rot_rect = orig_rect.copy()                      #Creates rotated rect
      rot_rect.center = rot_image.get_rect().center    #Sets center of rotated rect
      rot_image = rot_image.subsurface(rot_rect).copy()#Sets rotated image
      self.image = rot_image                           #Sets image to rotated image
      
    self.text = font.render("Score: " + str(self.score), 1, pygame.Color("white"))

    self.position += self.direction * self.speed 
    self.rect.center = self.position
    
    for wall in walls:                            #checks if collides w lava, if so explodes and respawn
      if self.rect.colliderect(wall.rect):
        expl = Explosion(self.rect.center)
        bullet_list.add(expl)
        self.position = pygame.math.Vector2(self.startx, self.starty)
    
      
class Bullet(pygame.sprite.Sprite):
  def __init__(self, position, direction, angle):
    super().__init__()
    
    self.bulletimg = pygame.image.load("bullet3.png")
    self.image = pygame.transform.rotate(self.bulletimg, -angle) #Creates Bullet Image based on Player Angle
    self.rect = self.image.get_rect(center=position)
    
    offset = pygame.math.Vector2(0, -60).rotate(angle)           #Offset vector added to bullet position for spacing
    
    self.position = pygame.math.Vector2(self.rect.center) + offset #Initial Position
    self.direction = direction
    self.richochet = 0;                                          #Initial ricochet counter
    
    
  def update(self):
    self.position += self.direction * 3               #Moves bullet
    self.rect.center = self.position

    
    for wall in walls:                                #Checking for wall collision
      if self.rect.colliderect(wall.rect):
        self.direction.rotate_ip(90)                  #If collides, rotates direction 90 degrees
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect(center=self.position)
        self.richochet += 1                           #Adds to richochet counter
        
    for spawn in spawn_list:                        #created a spawn so players cant be spam killed
      if self.rect.colliderect(spawn.rect):
        self.kill()

    if self.richochet == 3:                           #When richochet counter hits 3, kills bullet
      self.kill()
      
    for player in player_list:                        #Score System
      if self.rect.colliderect(player.rect):
        self.kill()                                   #Kill bullet if hits player
        if player == player_1:
          player_2.score += 1                         #Add score if hit other player
          expl = Explosion(player.rect.center)
          bullet_list.add(expl)
          player.position = pygame.math.Vector2(95, 240)
        if player == player_2:
          player_1.score += 1
          player.position = pygame.math.Vector2(545, 240)

class Wall(object):
  def __init__(self, pos):
    walls.append(self)
    self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
    self.image = pygame.image.load("lava.png")       #Sets image for the walls
    
class Spawn(pygame.sprite.Sprite):                       #spawn spot to create safezone
  def __init__(self, pos):
    super().__init__()
    self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
    self.rect = self.image.get_rect()
    self.rect.center = (pos[0], pos[1])
    
class Explosion(pygame.sprite.Sprite):               #Explosion class to display an explosion on bullet-tank impact
  def __init__(self, center):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("explosion.png")
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.frame = 0                                  #frame counter (tick)
    self.last_update = pygame.time.get_ticks()      #get current tick
    self.frame_rate = 30
    
  def update(self):
    now = pygame.time.get_ticks()
    if now - self.last_update > self.frame_rate:   #if current tick minus last tick is greater than 30 (FPS)
      self.last_update = now                             #update last tick to current tick
      self.frame += 1                                    #update frame counter
      if self.frame == 10:                               #if 10 frames has passed, kill the explosion
        self.kill()
      else:
        center = self.rect.center
        
##Variable Setup##
WIDTH = 640
HEIGHT = 480
FPS = 30
TITLE = "Capstone Python Game"
pygame.font.init()
font = pygame.font.SysFont('comicsans', 30, True)

walls = []

level = [
"WWWWWWWWWWWWWWWW",
"W              W",
"W              W",
"W   W      W   W",
"W              W",
"W      WW      W",
"W      WW      W",
"W              W",
"W   W      W   W",
"W              W",
"W              W",
"WWWWWWWWWWWWWWWW",
  ]
  
x = y = 0                  #Creates wall objects
for row in level:
  for col in row:
    if col == "W":
      Wall((x, y))
    x += 40
  y += 40
  x = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#Player Setup
player_list = pygame.sprite.Group() #Creates Sprite group

player_1 = Player(95, 240, 1)
player_list.add(player_1) #Adds player 1 to sprite group
player_2 = Player(545, 240, 2)
player_list.add(player_2) #Adds player 1 to sprite group

#Bullet Setup
bullet_list = pygame.sprite.Group()

#Spawns Setup
spawn_list = pygame.sprite.Group()
p1Spawn = Spawn((95, 240))
p2Spawn = Spawn((545, 240))
spawn_list.add(p1Spawn)
spawn_list.add(p2Spawn)


##
gameovertext = font.render("GAME OVER", 1, pygame.Color("white"))

##MAIN GAME LOOP##

running = True
while running:
  clock.tick(FPS)
  screen.fill((20, 20, 20))
  
  
  for wall in walls:
    screen.blit(wall.image, wall.rect) #Draws walls onto screen
  
  screen.blit(player_1.text, (20, 10))
  screen.blit(player_2.text, (530, 10))
  #p1Circle = pygame.draw.circle(screen, (0, 255, 0), (95, 240), 35)
 # p2Circle = pygame.draw.circle(screen, (0, 255, 0), (545, 240), 35)
  
  for event in pygame.event.get():
    #IF KEY PRESSED
    #PLAYER 1 KEYS (ARROWKEYS, / to shoot)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a: 
        player_1.angle_speed = -5      #Angle Player Left
      if event.key == pygame.K_d:
        player_1.angle_speed = 5       #Angle Player Right
      if event.key == pygame.K_w:
        player_1.speed = 3
      if event.key == pygame.K_s:
        player_1.speed = -3
      if event.key == pygame.K_SPACE:  #Shoot bullet
        bullet_list.add(Bullet(player_1.position, player_1.direction.normalize(), player_1.current_angle))
    #PLAYER 2 KEYS (AWSD, space to shoot)
      if event.key == pygame.K_LEFT: 
        player_2.angle_speed = -5      #Angle Player Left
      if event.key == pygame.K_RIGHT:
        player_2.angle_speed = 5       #Angle Player Right
      if event.key == pygame.K_UP:
        player_2.speed = 3
      if event.key == pygame.K_DOWN:
        player_2.speed = -3
      if event.key == pygame.K_SLASH:  #Shoot bullet
        bullet_list.add(Bullet(player_2.position, player_2.direction.normalize(), player_2.current_angle))
    #IF KEY RELEASED
    #PLAYER 1 KEYS
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        player_1.angle_speed = 0
      if event.key == pygame.K_d:
        player_1.angle_speed = 0
      if event.key == pygame.K_w:
        player_1.speed = 0
      if event.key == pygame.K_s:
        player_1.speed = 0
    #PLAYER 2 KEYS
      if event.key == pygame.K_LEFT: 
        player_2.angle_speed = 0      #Angle Player Left
      if event.key == pygame.K_RIGHT:
        player_2.angle_speed = 0       #Angle Player Right
      if event.key == pygame.K_UP:
        player_2.speed = 0
      if event.key == pygame.K_DOWN:
        player_2.speed = 0

  player_list.update() #Updates players
  player_list.draw(screen) #Send players to screen
  bullet_list.update() #Updates bullets
  bullet_list.draw(screen) #Send bullets to screen
  spawn_list.update()
  spawn_list.draw(screen)
  
  
  pygame.display.flip() #Sends screen to display
  
  ##GAME OVER
  if player_1.score == 10:
    winnertext = font.render("Player 1 Wins!", 1, pygame.Color("white"))
    screen.fill((0,0,0))
    screen.blit(gameovertext, (200, 100))
    screen.blit(winnertext, (190, 125))
    pygame.display.flip()
  if player_2.score == 10:
    winnertext = font.render("Player 2 Wins!", 1, pygame.Color("white"))
    screen.fill((0,0,0))
    screen.blit(gameovertext, (200, 100))
    screen.blit(winnertext, (190, 125))
    pygame.display.flip()
    
###END MAIN LOOP##


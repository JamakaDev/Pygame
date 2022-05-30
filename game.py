##################################################################
from operator import truediv
import pygame
from random import *
import time
import os

pygame.init()

def game():
  # Variables
  WINDOW_WIDTH = 720
  WINDOW_HEIGHT = 400
  SCALE = (48, 48)
  FPS = 20
  HERO_VEL = 5
  GROUND_HEIGHT = WINDOW_HEIGHT - SCALE[1]
  #-----------------------------------------------------------------
  w, h = SCALE[0], SCALE[1] # width & height for Rects
  direction = 'Right'
  heroIndex = 0
  jumpCount = 10
  isJumping = False
  isGrounded = True
  isFalling = False
  

  

  #==================================================================
  # Game Window => Surface => bg layer
  window = pygame.display.set_mode([WINDOW_WIDTH,  WINDOW_HEIGHT], ) # -> Surface
  pygame.display.set_caption('CS50 Final Project')
  icon = pygame.image.load(os.path.join('images/ninjaSprites', 'Attack__009.png')).convert_alpha()
  pygame.display.set_icon(icon)
  #==================================================================
  # Characters => Surface => obj layer
  heroIdle = pygame.image.load(os.path.join('images/ninjaSprites', 'Idle__002.png')).convert_alpha()
  heroIdleRight = pygame.transform.scale(heroIdle, (SCALE[0]*0.7, SCALE[1]))
  heroIdleLeft =pygame.transform.flip(heroIdleRight, flip_x=True, flip_y=False)
  #------------------------------------------------------------------
  heroAttack = [pygame.image.load(os.path.join('images/ninjaSprites', f'Attack__00{i}.png')).convert_alpha() for i in range(10)]
  heroAttackRight = [pygame.transform.scale(heroAttack[i], SCALE) for i in range(10)]
  heroAttackLeft = [pygame.transform.flip(hero, flip_x=True, flip_y=False) for hero in heroAttackRight]
  #------------------------------------------------------------------
  heroJump = [pygame.image.load(os.path.join('images/ninjaSprites', f'Jump__00{i}.png')).convert_alpha() for i in range(10)]
  heroJumpRight = [pygame.transform.scale(heroJump[i], SCALE) for i in range(10)]
  heroJumpLeft = [pygame.transform.flip(hero, flip_x=True, flip_y=False) for hero in heroJumpRight]
  #------------------------------------------------------------------
  heroRun = [pygame.image.load(os.path.join('images/ninjaSprites', f'Run__00{i}.png')).convert_alpha() for i in range(10)]
  heroRunRight = [pygame.transform.scale(heroRun[i], SCALE) for i in range(10)]
  heroRunLeft = [pygame.transform.flip(hero, flip_x=True, flip_y=False) for hero in heroRunRight]
  #------------------------------------------------------------------
  hero = {
    'heroAttackRight': heroAttackRight,
    'heroAttackLeft': heroAttackLeft,
    'heroJumpRight': heroJumpRight,
    'heroJumpLeft': heroJumpLeft,
    'heroRunRight': heroRunRight,
    'heroRunLeft': heroRunLeft,
    'heroIdleRight': heroIdleRight,
    'heroIdleLeft': heroIdleLeft
  }
  #==================================================================
  
  #------------------------------------------------------------------
  bgLayer1 = pygame.image.load(os.path.join('images/oak_woods_v1.0/background/','background_layer_1.png')).convert_alpha()
  bgLayer1 = pygame.transform.scale(bgLayer1, (WINDOW_WIDTH,WINDOW_HEIGHT))
  #------------------------------------------------------------------
  bgLayer2 = pygame.image.load(os.path.join('images/oak_woods_v1.0/background/','background_layer_2.png')).convert_alpha()
  bgLayer2 = pygame.transform.scale(bgLayer2, (WINDOW_WIDTH,WINDOW_HEIGHT))
  #------------------------------------------------------------------
  bgLayer3 = pygame.image.load(os.path.join('images/oak_woods_v1.0/background/','background_layer_3.png')).convert_alpha()
  bgLayer3 = pygame.transform.scale(bgLayer3, (WINDOW_WIDTH,WINDOW_HEIGHT))

  #==================================================================
  # Tileset Sheet => 24x24 => bg, obj, fg layers
  tileset = pygame.image.load(os.path.join('images/oak_woods_v1.0/','oak_woods_tileset.png')).convert_alpha()
  tiles = [tileset.subsurface(((i,j),(24,24))) for j in range(360) for i in range(504) if (i%24==0 and j%24==0)]
  tiles = [pygame.transform.scale(tiles[i], SCALE) for i in range(len(tiles))]
  
  #==================================================================
  # Ground Surfaces and Rects
  soilDark = [((tiles[22]), tiles[22].get_rect(x=i*SCALE[0], y=WINDOW_HEIGHT-(SCALE[1]*.5), width=SCALE[0],height=SCALE[1])) for i in range(WINDOW_WIDTH//24)]
  groundList = [((tiles[2]), tiles[2].get_rect(x=i*SCALE[0], y=WINDOW_HEIGHT-(SCALE[1]*1.5), width=SCALE[0],height=SCALE[1])) for i in range(WINDOW_WIDTH//24)]
  groundRects = list(map(lambda x: x[1],groundList))
  
  #==================================================================
  # Alternative terrain and obstacles
  ltMix4 = pygame.transform.scale(tileset.subsurface(((120,0),(96,24))),(SCALE[0]*4,SCALE[1]))
  ltMix4Rect = ltMix4.get_rect(left=w*5,y=GROUND_HEIGHT-(h*2),width=w*4,height=h*.75)

  orgMix4 = pygame.transform.scale(tileset.subsurface(((0,0),(96,24))),(SCALE[0]*4,SCALE[1]))
  orgMix4Rect = orgMix4.get_rect(left=w*8,y=GROUND_HEIGHT-(h*4),width=w*4,height=h*.75)

  ltSolid = ((tiles[12]), tiles[12].get_rect(x=0,y=GROUND_HEIGHT-(h*2),width=w,height=h))
  orgSolid = ((tiles[10]), tiles[10].get_rect(x=0,y=GROUND_HEIGHT-(h*2),width=w,height=h))
  
  
  #==================================================================
  
  heroSurface = hero[f'heroIdle{direction}']
  heroRect = heroSurface.get_rect(x=w,y=(GROUND_HEIGHT-(h*1.5)),width=w,height=h)

  #==================================================================
  collisionRects = groundRects.copy()
  collisionRects.append(ltMix4Rect)
  collisionRects.append(orgMix4Rect)

  #==================================================================
  
  def drawHero():
    window.blit(heroSurface, heroRect)

  def drawBg():
    window.blit(bgLayer1,(0,0))
    window.blit(bgLayer2,(0,0))
    window.blit(bgLayer3,(0,0))
    window.blits(soilDark)
    window.blits(groundList)

  def drawFg():
    window.blit(ltMix4, ltMix4Rect)
    window.blit(orgMix4, orgMix4Rect)
    
  
  def groundCollision():
    tmpRect = heroRect.copy()
    tmpRect.bottom += 1
    collideIndex = tmpRect.collidelist(collisionRects)
    if collideIndex != -1:
      heroRect.bottom = collisionRects[collideIndex].top
      isJumping = False
      isGrounded = True
      isFalling = False
      return collideIndex

    return None
    

  # LEFT = if my (left => x) touches solid then no more left movement
  # if my.x - my.vel <= obj.right: continue || my.vel = 0 else {existing code}

  # RIGHT = if my right touches solid then no more right movement
  # if my.x + w + my.vel >= obj.left: continue || my.vel = 0 else {existing code}
  
  # TOP = if my top touches solid then no more up movement
  # if my.y - my.vel <= obj.bottom: continue || my.vel = 0 else {existing code}
  # if heroRect.top - jumpCount*(HERO_VEL*.5) <= obj.bottom:
  
  # BOTTOM = if my bottom touches solid then no more down movement
  # if my.y + h + my.vel >= obj.top: continue || my.vel = 0 else {existing code}
      
  def drawGame():
    drawBg()
    drawHero()
    drawFg()
    # groundCollision()
    pygame.display.update()
  

  clock = pygame.time.Clock()
  isRunning = True

  while isRunning:
        
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        isRunning = False
    
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and heroRect.x > 0:
      direction = 'Left'
      heroSurface = hero[f'heroRun{direction}'][heroIndex]
      heroRect.x -= HERO_VEL
      heroIndex += 1
    elif keys[pygame.K_RIGHT] and heroRect.x < WINDOW_WIDTH-w:
      direction = 'Right'
      heroSurface = hero[f'heroRun{direction}'][heroIndex]
      heroRect.x += HERO_VEL
      heroIndex += 1
    else:
      heroSurface = hero[f'heroIdle{direction}']
    
    if keys[pygame.K_SPACE] and isGrounded:
      isJumping = True
      isGrounded = False

    if isJumping:
      heroSurface = hero[f'heroJump{direction}'][5]
      heroRect.bottom -= jumpCount*(HERO_VEL*.5)
      jumpCount -= 1
      if not jumpCount:
        isJumping = False
        isFalling = True
    
    if not isGrounded and isFalling:
      heroSurface = hero[f'heroJump{direction}'][8]
      heroRect.bottom += jumpCount*(HERO_VEL*.75)
      jumpCount += 1
    
    i = groundCollision()
    if i and not isJumping:
      if heroRect.bottom+HERO_VEL >= collisionRects[i].top:
        heroRect.bottom = collisionRects[i].top
        isGrounded = True
        isFalling = False
        jumpCount = 10
    elif i == None and not isJumping:
      jumpCount = 5
      isGrounded = False
      isFalling = True
    

      
    if heroIndex+1 >= 10: heroIndex = 0
    drawGame()


if __name__ == '__main__':
  game()
  
  
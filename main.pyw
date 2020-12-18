import pygame
from pygame.locals import *
from random import randint
from typing import List

def randomCoordinates():
  return (
    randint(square_size, width - square_size),
    randint(square_size, height - square_size)
  )

def restart_game():
  global points,initialWidth, x_snake, y_snake, snake_list, head_list, x_apple, y_apple, gameData

  gameData['points'] = 0
  initialWidth = 5
  x_snake, y_snake = centerCoordinates
  snake_list = []
  head_list = []
  x_apple, y_apple = randomCoordinates()
  gameover = False

def quit():
  pygame.quit()
  exit()

def snake_increases(snake_list: List):
  for coordenate in snake_list:
    pygame.draw.rect(
      window, 
      colors['snake'], 
      (coordenate[0], coordenate[1], square_size, square_size)
    )

pygame.init()

width, height = (640, 480)
square_size = 20
centerCoordinates = (width // 2, height //2)

window = pygame.display.set_mode([width, height])
pygame.display.set_caption('Snake Game')

apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (40, 40))
miniApple = pygame.transform.scale(apple_image, (square_size + 10, square_size + 10))
clock = pygame.time.Clock()

coin_music = pygame.mixer.Sound('coin.wav')
font = pygame.font.SysFont('arial', 32)

x_snake, y_snake = centerCoordinates
x_control, y_control = [0, 20]
initialWidth = 5
snake_list = []

colors = {
  'background': (40, 120, 40),
  'snake': (0, 255, 0),
  'text': (255, 255, 255)
}

gameData = {
  'points': 0,
  'gameover': False
}

x_apple, y_apple = randomCoordinates()
while True:
  clock.tick(30)
  window.fill(colors['background'])

  snake = pygame.draw.rect(window, colors['snake'], (x_snake, y_snake, square_size, square_size))
  pointsText = font.render(f'{gameData["points"]}', True, colors['text'])
  appleInWindow = window.blit(miniApple, (x_apple, y_apple))

  for e in pygame.event.get():
    if e.type == QUIT:
      quit()

    if e.type == KEYDOWN:
      if e.key == K_SPACE:
        pause = True

        while pause:
          pauseText = font.render('Pause', True, colors['text'])

          snake_increases(snake_list)

          window.blit(pauseText, (
            centerCoordinates[0] - pauseText.get_width() //2,
            centerCoordinates[1] - pauseText.get_width() //2)
          )

          for event in pygame.event.get():
            if event.type == KEYDOWN:
              if event.key == K_SPACE:
                pause = False

            if event.type == QUIT:
              quit()
          
          pygame.display.update()
          
      if e.key == K_UP:
        if y_control != square_size:
          y_control = -square_size
          x_control = 0

      if e.key == K_DOWN:
        if y_control != - square_size:
          y_control = square_size
          x_control = 0

      if e.key == K_LEFT:
        if x_control != square_size:
          x_control = -square_size
          y_control = 0

      if e.key == K_RIGHT:
        if x_control != -square_size:
          x_control = square_size
          y_control = 0

  x_snake += x_control
  y_snake += y_control

  if appleInWindow.colliderect(snake):
    x_apple, y_apple = randomCoordinates()
    gameData['points'] += 1
    initialWidth += 2
    coin_music.play()

  if x_snake > width:
    x_snake = 0

  if y_snake > height:
    y_snake = 0

  if x_snake < 0:
    x_snake = width

  if y_snake < 0:
    y_snake = height

  head_coordenates = [x_snake, y_snake]
  snake_list.append(head_coordenates)
  snake_increases(snake_list)

  if len(snake_list) > initialWidth:
    del snake_list[0]

  if snake_list.count(head_coordenates) > 1:
    gameData['gameover'] = True

    while gameData['gameover']:
      window.fill(colors['background'])
      restart_text = font.render('Gameover! R to Restart', True, colors['text'])

      for e in pygame.event.get():
        if e.type == QUIT:
          quit()

        if e.type == KEYDOWN:
          if e.key == K_r:
            gameData['gameover'] = False
            restart_game()

      window.blit(restart_text, (
        centerCoordinates[0] - restart_text.get_width() //2,
       centerCoordinates[1] - restart_text.get_height() //2)
      )
      pygame.display.update()

  window.blit(pointsText, (width - pointsText.get_width() - 30 - apple_image.get_width(), 25))
  window.blit(apple_image, (width - pointsText.get_width() - 40, 10))

  pygame.display.update()

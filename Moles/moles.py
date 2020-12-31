# import sys
# sys.path.append('max-dev')
# import untitled

import hub
from time import sleep
from util.scratch import convert_image

def rotl(l):
  return l[1:]+l[:1]

def rot(l):
  return l[-1:]+l[:-1]

def matrix2image(pos):
  image = ''.join(map(str,[j for i in pos for j in i]))
  image = hub.Image(convert_image(image))
  return image

def moles():
  print("Welcome to Moles")
  pos = [
    [9,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
  ]
  hub.display.show(matrix2image(pos))

  i = 0
  while True:
    pressed = [hub.button.left.was_pressed(), hub.button.right.was_pressed(), hub.button.center.was_pressed()]
    if any(pressed):
        # down
      if pressed == [1,1,0]:
        # position = list(map(sum, zip(position,[-1,0])))
        pos = rot(pos)

        # left
      elif pressed == [1,0,0]:
        # position = list(map(sum, zip(position,[0,-1])))
        pos = list(map(rotl, pos))

        # right
      elif pressed == [0,1,0]:
        # position = list(map(sum, zip(position,[0,1])))
        pos = list(map(rot, pos))

        # up
      elif pressed == [0,0,1]:
        # position = list(map(sum, zip(position,[1,0])))
        pos = rotl(pos)

      hub.display.show(matrix2image(pos))

    sleep(0.2)


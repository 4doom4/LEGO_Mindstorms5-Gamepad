#!/usr/bin/env python

"""Moles for 51515 GamePad

Frank likes his garden but moles do too. They dig molehills so Frank has to
stomp on them to retain control of his property. But be cautious! When Frank
is sourrounded by moles jumping out of their molehill Frank is trapped and
looses!

Playing:
Use the left/right and center button to move up. To move down press left and
right at the same time. When a molehill is bright like Frank he can't stomp
on it any more.

First level requires 3, second 5 and third level 8 molehills.

    Changelog:
    09-jan-2020 (me) first 3 levels for beta
    01-jan-2020 (me) added moles and winning condition
    30-dec-2020 (me) created
"""

import hub
from time import sleep
from util.scratch import convert_image
from random import randrange

from mindstorms import MSHub

    # override back to menu for center button
def null(sender):
    return

class Moles():
    def __init__(self, occupiedCoords):
        self._intensity = 1
        self._coord = self.spawn(occupiedCoords)

    def spawn(self, occupiedCoords):
        coords = [[i,j] for i in range(5) for j in range (5)]
        while len(coords):
            pick = randrange(len(coords))
            moleCoord = coords[pick]
            if not any([moleCoord == coord for coord in occupiedCoords]):
                return moleCoord
            else:
                coords.pop(pick)
        return None

    def intensity(self):
        return str(self._intensity)

    def coord(self):
        return self._coord

    def dig(self):
        if not self._intensity == 9:
            self._intensity += 1

class Player():
    def __init__(self):
            # keeps track of the position of the player by pushing
            # the current position to [0,0] in the list
            # we move invert to the actual movement to always have
            # the coordinate there. initially player is at top left
        self._pos = [
            [0,1,2,3,4],
            [10,11,12,13,14],
            [20,21,22,23,24],
            [30,31,32,33,34],
            [40,41,42,43,44]
        ]
    def _rotl(self, l):
        return l[1:]+l[:1]

    def _rot(self, l):
        return l[-1:]+l[:-1]

    def _occupied(self, pos, moleCoords):
        [x, y] = self._rot(list(divmod(pos[0][0], 10)))
        for moleCoord in moleCoords:
            if moleCoord == [x, y]:
                return 1
        return 0

    def moveUp(self, moleCoords):
        pos = self._rotl(self._pos)
        if not self._occupied(pos, moleCoords):
            self._pos = pos

    def moveDown(self, moleCoords):
        pos = self._rot(self._pos)
        if not self._occupied(pos, moleCoords):
            self._pos = pos

    def moveLeft(self, moleCoords):
        pos = list(map(self._rot, self._pos))
        if not self._occupied(pos, moleCoords):
            self._pos = pos

    def moveRight(self, moleCoords):
        pos = list(map(self._rotl, self._pos))
        if not self._occupied(pos, moleCoords):
            self._pos = pos

    def coord(self):
            # rot to return x,y
        return self._rot(list(divmod(self._pos[0][0], 10)))

class Level():
    emptyImage = '0' * 25
    def __init__(self, digTime, spawnTime, levelScore):
        hub.button.center.on_change(null) # override back to menu
            # reset pressed buttons
        hub.button.left.was_pressed()
        hub.button.right.was_pressed()
        hub.button.center.was_pressed()

        self.player = Player()
        self.moles = [Moles(self.player.coord())]
        self.levelScore = levelScore
        self.digTime = digTime
        self.spawnTime = spawnTime
        self.win = 0
        self.loose = 0

        self._hub = MSHub()
        self._score = 0

    def score(self):
        return self._score

    def playerUp(self):
        self.player.moveUp(self.moleBlockCoord())

    def playerDown(self):
        self.player.moveDown(self.moleBlockCoord())

    def playerLeft(self):
        self.player.moveLeft(self.moleBlockCoord())

    def playerRight(self):
        self.player.moveRight(self.moleBlockCoord())

    def didPlayerBlock(self):
        [x, y] = self.player.coord()
        left = []
        playerEnv = [
            hub.display.pixel(x + 1 if x + 1 < 5 else 0, y),
            hub.display.pixel(x - 1 if x - 1 >= 0 else 4, y),
            hub.display.pixel(x, y + 1 if y + 1 < 5 else 0),
            hub.display.pixel(x, y - 1 if y - 1 >= 0 else 4)
        ]

        if all(intensity == 9 for intensity in playerEnv):
           self.loose = 1

    def moleBlockCoord(self):
        return [mole.coord() for mole in self.moles if mole.intensity() == '9']

    def moleCoords(self):
        return [mole.coord() for mole in self.moles]

    def moleCreate(self):
        occupiedCoords = self.moleCoords()
        occupiedCoords.append(self.player.coord())
        newMole = Moles(occupiedCoords)
        if newMole.coord() == None:
            self.loose = 1
        else:
            self.moles.append(newMole)

    def molesDig(self):
        [mole.dig() for mole in self.moles]

    def draw(self):
            # draw player
        [xP, yP] = self.player.coord()
        index = yP * 5 + xP
        image = self.emptyImage[:index] + '9' + self.emptyImage[index+1:]

            # draw mole but verify if player stands on mole which is not fully
            # exposed. If the case mole will be removed from the system and a
            # point is give to the player
        moles = []
        for mole in self.moles:
            [xM, yM] = mole.coord()
            if [xP, yP] == [xM, yM]:
                self._score += 1
                if self._score >= self.levelScore:
                    self.win = 1
                hub.led(238, 246, 246)
                hub.sound.beep(260, 200)
                hub.led(255, 70, 35)
            else:
                moles.append(mole)
                index = yM * 5 + xM
                image = image[:index] + mole.intensity() + image[index+1:]
        self.moles = moles
        hub.display.show(hub.Image(convert_image(image)))

    def didLoose(self):
        print("Game Over")
        hub.led(255,0,0)
        sleep(2)

    def didWin(self):
        print("Game Won")
        hub.led(0,255,0)
        sleep(2)

class Game():
    def __init__(self):
        self.curLevel = 0
        self.active = 1

        self._spawnTime = [1, 0.4, 0.2]
        self._digTime = [0.4, 0.2, 0.2]
        self._levelScore = [3,5,8]
        self._totalLevels = len(self._spawnTime) - 1

    def spawnTime(self):
        return self._spawnTime[self.curLevel]

    def digTime(self):
        return self._digTime[self.curLevel]

    def levelScore(self):
        return self._levelScore[self.curLevel]

    def nextLevel(self):
        self.curLevel += 1
        print([self.curLevel, self._totalLevels])
        if self.curLevel > self._totalLevels:
            self.active = 0

def moles():
    print("Welcome to Moles")

    game = Game()
    while game.active:

        level = Level(game.digTime(), game.spawnTime(), game.levelScore())
        level.draw()

        i = 0
        while True:
            i += 1
            pressed = [
                hub.button.left.was_pressed(),
                hub.button.right.was_pressed(),
                hub.button.center.was_pressed()
            ]
            if any(pressed):
                    # down
                if pressed == [1,1,0]:
                    level.playerDown()

                    # left
                elif pressed == [1,0,0]:
                    level.playerLeft()

                    # right
                elif pressed == [0,1,0]:
                    level.playerRight()

                    # up
                elif pressed == [0,0,1]:
                    level.playerUp()

            if not i%(level.digTime/0.2):
               level.molesDig()
            if not i%(level.spawnTime/0.2):
               level.moleCreate()
            
            if level.loose:
                level.didLoose()
                game.active = 0
                break

            level.draw()
            if level.win:
                level.didWin()
                break

            level.didPlayerBlock()

            sleep(0.2)
        game.nextLevel()

moles()
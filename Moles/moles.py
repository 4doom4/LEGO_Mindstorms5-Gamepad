#!/usr/bin/env python

"""Moles for 51515 GamePad

<insert moles descriptions>

Playing:
<insert how to play>

    Changelog:
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
        while True:
            moleCoord = [randrange(5), randrange(5)]
            if not any([moleCoord == coord for coord in occupiedCoords]):
                break
        return moleCoord

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
        [row, col] = divmod(pos[0][0], 10)
        print(moleCoords)
        print([row, col])
        for moleCoord in moleCoords:
            if moleCoord == [row, col]:
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
        return list(divmod(self._pos[0][0], 10))

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
    
    def moleBlockCoord(self):
        return [mole.coord() for mole in self.moles if mole.intensity() == '9']

    def moleCoords(self):
        return [mole.coord() for mole in self.moles]

    def moleCreate(self):
        occupiedCoords = self.moleCoords()
        occupiedCoords.append(self.player.coord())
        self.moles.append(Moles(occupiedCoords))

    def molesDig(self):
        [mole.dig() for mole in self.moles]

    def draw(self):
            # draw player
        [rowP, colP] = self.player.coord()
        index = rowP * 5 + colP
        image = self.emptyImage[:index] + '9' + self.emptyImage[index+1:]

            # draw mole but verify if player stands on mole which is not fully
            # exposed. If the case mole will be removed from the system and a
            # point is give to the player
        moles = []
        for mole in self.moles:
            [rowM, colM] = mole.coord()
            if [rowP, colP] == [rowM, colM]:
                self._score += 1
                hub.led(238, 246, 246)
                hub.sound.beep(260, 200)
                hub.led(255, 70, 35)
            else:
                moles.append(mole)
                index = rowM * 5 + colM
                image = image[:index] + mole.intensity() + image[index+1:]
        self.moles = moles
        hub.display.show(hub.Image(convert_image(image)))

    def didWin(self):
        if self._score >= self.levelScore:
            

            for i in range (2):
                if i%2:
                    self._hub.status_light.on('white')
                else:
                    self._hub.status_light.on('green')
                # self._hub.speaker.beep(60, 0.2)
                # self._hub.speaker.beep(67, 0.2)
                # self._hub.speaker.beep(60, 0.2)
            return 1
        else:
            return 0

class Game():
    def __init__(self):
        self.totalLevels = 2
        self.curLevel = 1

        self._spawnTime = [1, 0.4]
        self._digTime = [0.4, 0.2]
        self._levelScore = [3,5]

    def spawnTime(self):
        return self._spawnTime[self.curLevel-1]

    def digTime(self):
        return self._digTime[self.curLevel-1]
    
    def levelScore(self):
        return self._levelScore[self.curLevel-1]

    def levels(self):
        while self.curLevel <= self.totalLevels:
            yield self.curLevel
            self.curLevel += 1


def moles():
    print("Welcome to Moles")

    game = Game()

    for level in game.levels():

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

            if level.didWin():
                print('WON!')
                break

            if not i%5:
                level.molesDig()
            if not i%5:
                level.moleCreate()

            level.draw()
            sleep(0.2)

moles()
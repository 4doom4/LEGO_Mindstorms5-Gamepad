#!/usr/bin/env python

"""Emotions for 51515 GamePad

This script is a really simple game similar to simon says which pretends to
predict a person's emotion by randomly picking it from a list of pre-encoded 
emojis on the 51515 hub.

Playing:
Hold down the left key on the GamePad. Once released the final pick is made.

    Changelog:
    28-dec-2020 (me) created
"""
__version__ = '1.0'

    # Import the 51515 classes
from mindstorms import MSHub
from mindstorms.control import wait_for_seconds
    # Import micropython classes
import random

    # Existing emojis images on the hub
emotions = [
    'ANGRY', 'ASLEEP', 'HAPPY', 'HEART', 'MEH', 'SAD', 'SILLY'
]

colorEmotions = [
    'red', 'white', 'yellow', 'pink', 'black', 'white', 'azure'
]



def ShowRandomImage(imageList, duration=0.1):
    '''
    Shows a random image from imageList on the hub for 0.2s and returns
    the position of that element.

            Parameters:
                    imageList ([str]): a list of existing images on hub
                    duration (float): length to show the image

            Returns:
                    pick (int): position in imageList
    '''
    pick = random.randrange(len(imageList))
    hub.light_matrix.show_image(imageList[pick])
    wait_for_seconds(duration)
    return pick

def ShowSpecificColor(pick, colorList):
    '''
    Shows a specific color to match the emotions from the image list.

            Parameters:
                    pick (int): position in imageList
                    colorList ([str]): a list of matching colors

            Returns:
                    nothing
    '''
    hub.status_light.on(colorList[pick])

def ShowSpecificImage(pick, imageList):
    '''
    Shows a specific image based on a previous pick.

            Parameters:
                    pick (int): position in imageList
                    imageList ([str]): a list of existing images on hub

            Returns:
                    nothing
    '''
    hub.light_matrix.show_image(imageList[pick])

    # Initilized the hub
hub = MSHub()

    # "Game engine" ;)
gameStart = 0
while True:
        # Start the game
    if hub.left_button.is_pressed():
        if gameStart == 0: hub.speaker.start_beep()
        pick = ShowRandomImage(emotions)
        ShowSpecificColor(pick, colorEmotions)
        gameStart = 1

        # End the game and show final pick
    elif (not hub.left_button.is_pressed() and gameStart == 1):
            # Slow down the picker
        for i in range(10):
            hub.speaker.start_beep()
            pick = ShowRandomImage(emotions, 0.08*i)
            ShowSpecificColor(pick, colorEmotions)
            hub.status_light.off()
            hub.speaker.stop()
            wait_for_seconds(0.02*i)

            # Show the final pick
        for i in range (7):
            ShowSpecificColor(pick, colorEmotions)
            ShowSpecificImage(pick, emotions)

                # "Final Music"
            hub.speaker.beep(60, 0.2)
            hub.speaker.beep(67, 0.2)
            hub.speaker.beep(60, 0.2)

            hub.light_matrix.off()
            hub.status_light.off()
            wait_for_seconds(0.5)
        gameStart = 0

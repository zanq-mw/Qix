# Qix

This project is a simplified version of the 1981 arcade game **Qix**. 

In this game the player controls a sprite represented by a red square, in a large field. The goal of this game is to  use the sprite to paint 65% of the field. The sprite can traverse the four walls of the field. It can also enter the field.

When the sprite enters the field, its path is tracked. The path is shown as a red dotted line. Once the sprite reaches another wall of the field, the space enclosed by the path of the sprite in the field, and the walls, is painted. A counter on the top of the screen tracks the percentage of the field painted.

The player must try to reach the goal without losing all their health. The player starts with 3 units of health. Bumping into an enemy takes away 1 health unit. If a player loses all 3, they lose the game. 

When the sprite is traversing the walls of the field, the player must look out for the 2 Sparx. These are 2 enemy sprites represented by purple squares, that also traverse the walls. 

When in the field, the player must avoid the Qix, a white rectangle sprite that moves in random directions. If the player is hit by the Qix, not only do they lose a health unit, but the path that was being tracked is erased and the player is sent back to the original position they were at before entering the field.

The player must also be weary of the Sparx when in the field. If a Sparx makes contact with the beginning of the path (located at the spot where the player entered into the field), the player loses a health unit, the path is erased, and the player is sent back to that position. 

![Game screen](Qix/images/game.png?raw=true)

### Setup

Clone this github repository to your computer
```bash
$ git clone https://github.com/zanq-mw/Qix.git
```
Execute the Qix/Qix/main.py file to start a game
```bash
$ python3 "{PATH TO FOLDER CONTAINING REPO}/Qix/Qix/main.py"
```
A Pygame window will open up with the game home screen, with the controls displayed. Press ENTER to start the game

![Home screen](Qix/images/startup.png?raw=true)

### How to play
While the player is on the walls, they can traverse them by using the arrow keys. If they are on a vertical wall (the left or right wall) they can only move up and down. Likewise, if they are on a horizontal wall (top or bottom), they can only move left or right.

To enter the field, the player must press the space bar while also pressing the correct arrow key. They must press the arrow key that is opposite direction of the wall they are on. For example, if the player is on the left wall, they must press the right key. Once in the field, the player can use the the arrow keys to move in any direction. Once the player returns to any of the walls, they must use the space bar and the correct arrow key to enter the field again. 

Players can keep track of their health and score in the top left of the screen.

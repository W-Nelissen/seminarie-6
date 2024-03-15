from game_area import GameArea
import pygame as pg
from game_constants import *
from colors import *

from event_handler import Button



class GameAreaControls(GameArea):
    def __init__(self, game, r):
        GameArea.__init__(self, game, r)
        self.startbutton = Button(self, self._x(10), self._y(10), BUTTON_WIDTH, BUTTON_HEIGHT, "beginstelling", "launch_start" )
        self.loadbutton = Button(self, self._x(20 + BUTTON_WIDTH), self._y(10), BUTTON_WIDTH, BUTTON_HEIGHT, "load", "load_game" )
        self.loadbutton.enabled = False
        self.savebutton = Button(self, self._x(30 + 2 * BUTTON_WIDTH), self._y(10), BUTTON_WIDTH, BUTTON_HEIGHT, "save", "save_game" )
        self.savebutton.enabled = False

    def draw(self):
        GameArea.draw(self)
        # Teken hier de controls
        # Save, Open, Quit, ...
        # rect = pg.Rect((645, 45, 150, 70))
        # pg.draw.rect(self.game.win, LTRED, rect, 0)
        # pg.draw.rect(self.game.win, DRED, rect,4)
        # pg.draw.line(self.game.win,DRED, (rect.left, rect.top), (rect.right, rect.bottom), 4)
        # pg.draw.line(self.game.win,DRED, (rect.right, rect.top), (rect.left, rect.bottom), 4)

        
        self.startbutton.draw(self.game.win)
        self.loadbutton.draw(self.game.win)
        self.savebutton.draw(self.game.win)

    def execute_action(self, action):
        if action == "launch_start":
            self.game.chess_board.resetBoard()




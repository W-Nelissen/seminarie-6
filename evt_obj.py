from colors import *
import pygame as pg
""""
 EvtObj handles standard events.
    Buttons
    Drag/drop objects
    ...

"""
class EvtObj:
    def __init__(self, has_select=False, has_dragging=False):
        #all features are turned off by default, but adding them is just adding parameters
        self.has_select = has_select
        self.has_dragging = has_dragging

        # Keep track of mouse activity, object dragging, button mechanics
        self.isWithin = False
        self.isPressed = False
        self.isDragged = False

        # Default colors for highlighting objects
        self.cPressed = (0, 255, 255)
        self.cNormal = (255, 255, 0)
        self.cDragged = LTGREY

        #TODO: implement modifiers (_left/_right may be ditched later)
        self.mod_shift = False
        self.mod_shift_left = False
        self.mod_shift_right = False
        self.mod_ctrl = False
        self.mod_ctrl_left = False
        self.mod_ctrl_right = False
        self.mod_alt = False

        self.evtObjects = []

    # checks if click was within object. Needs override
    def isMouseWithin(self, mouse_x, mouse_y):
        return False

    def MOUSEWHEEL(self, _wheel):
        pass

    def MOUSEBUTTONDOWN(self, mouse_x, mouse_y):
        for obj in self.evtObjects:
            obj.MOUSEBUTTONDOWN(mouse_x, mouse_y)
    def MOUSEBUTTONUP(self, mouse_x, mouse_y):
        for obj in self.evtObjects:
            obj.MOUSEBUTTONUP(mouse_x, mouse_y)
    def MOUSEMOTION(self, mouse_x, mouse_y):
        for obj in self.evtObjects:
            obj.MOUSEMOTION(mouse_x, mouse_y)

    def action_hovering(self):
        pass
    def action_dragging(self):
        pass
    def action_dropped(self):
        pass
    def action_clicked(self):
        pass

class EvtBtn(EvtObj):
    def __init__(self, x, y, w, h, name, action):
        EvtObj.__init__(self)
        self.rect = pg.Rect((x, y, w, h))
        self.name = name
        self.action = action

    def isMouseWithin(self, mouse_x, mouse_y):
        return self.rect.left < mouse_x < self.rect.right and self.rect.top < mouse_y < self.rect.bottom

    def MOUSEBUTTONDOWN(self, mouse_x, mouse_y):
        self.isWithin = self.isMouseWithin(mouse_x, mouse_y)
        if self.isWithin:
            self.isPressed = True

    def MOUSEBUTTONUP(self, mouse_x, mouse_y):
        self.isWithin = self.isMouseWithin(mouse_x, mouse_y)
        if self.isWithin and self.isPressed:
            self.action_clicked()
        self.isPressed = False

    def MOUSEMOTION(self, mouse_x, mouse_y):
        self.isWithin = self.isMouseWithin(mouse_x, mouse_y)

    def write_string(self, win, strText, text_color, x, y):
        self.font = pg.font.Font("freesansbold.ttf", 24)
        text_surface = self.font.render(strText, True, text_color)
        win.blit(text_surface, (x, y))

    def draw(self, win):
        bg_color = BLUE
        fg_color = RED
        txt_color = RED
        if self.isPressed and self.isWithin:
            fg_color = BLUE
            bg_color = RED
            txt_color = BLUE
        pg.draw.rect(win, bg_color, self.rect, 0)
        pg.draw.rect(win, fg_color, self.rect, 4)
        self.write_string(win, self.name, txt_color, self.rect.left + 4, self.rect.top + 4)
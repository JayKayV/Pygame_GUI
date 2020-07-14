import pygame

class GUI_OBJ:
    children = []
    parent = None
    def __init__(self):
        pass

    #function to be override
    def blit(self, surf):
        for child in self.children:
            child.blit(surf)

    #function available only to boxes and buttons (dropdown list (wether vertical or not) doesnot)
    def set_border(self):
        pass

    #function available to all objects except slider
    def set_hover(self):
        pass

    #DO NOT OVERRIDE THESE
    def set_relative_to(self, other_rect, offset_x = 0, offset_y=0):
        if isinstance(other_rect, pygame.Rect):
            self.pos = (other_rect.x + offset_x, other_rect.y + offset_y)
        elif isinstance(other_rect, tuple):
            self.pos = (other_rect[0] + offset_x, other_rect[1] + offset_y)
        else:
            raise TypeError

    def set_parent(self, other):
        other.children.append(self)
        self.parent = other

    def animation(self, func, startDelay):
        pass

class GUI_MANAGER:
    def __init__(self, gui_object_list):
        self.guiOBJECTS = gui_object_list

    def blit(self, screenSurf):
        for obj in self.guiOBJECTS:
            obj.blit(screenSurf)

    def add_guiObj(self, guiObj):
        self.guiOBJECTS.append(guiObj)

    def toString(self):
        res = ''
        for obj in self.guiOBJECTS:
            res += str(obj) + ' '
        return res
import pygame
from types import FunctionType

class GUI_OBJ:
    children = []
    parent = None

    surf = None
    text_img = None
    pos = None
    font = None

    borderColor = None
    borderThickness = None
    hover = False
    ppos = None

    data = {
        'surface': surf,
        'textImg': text_img,
        'pos': pos,
        'font': font
    }
    def __init__(self):
        pass

    #function to be override
    def blit(self, surf):
        for child in self.children:
            if isinstance(child, GUI_OBJ):
                child.blit(surf)
            else:
                raise TypeError

    #function available only to boxes and buttons (dropdown list (wether vertical or not) doesnot)
    def set_border(self):
        pass

    #function available to all objects except slider
    def set_hover(self):
        pass

    #update to all object's attribute
    #if attr is a key in data, update that attribute with func
    #if attr is a function (must be available in all children and its descendants),
    # call them instead with func being parameters
    #if attr is None then update the object instead
    def update(self, attr, *func):
        if isinstance(attr, str) or isinstance(attr, FunctionType) or not attr:
            for child in self.children:
                child.update_obj(attr, *func)
        else:
            raise TypeError

    def update_key(self, key_name, key_value):
        for child in self.children:
            temp = child.data
            temp[key_name] = key_value
            child.data = temp

    #DO NOT OVERRIDE THESE
    def set_relative_to(self, other_rect, offset_x=0, offset_y=0):
        if isinstance(other_rect, pygame.Rect):
            self.pos = (other_rect.x + offset_x, other_rect.y + offset_y)
        elif isinstance(other_rect, tuple):
            self.pos = (other_rect[0] + offset_x, other_rect[1] + offset_y)
        else:
            raise TypeError

    def set_parent(self, other):
        other.children.append(self)
        self.parent = other

    def update_obj(self, attr, *func):
        update_func = None
        if len(func) == 1 and isinstance(func, FunctionType):
            update_func = func[0]
        if attr:
            if attr in self.data:
                self.data[attr] = update_func(self.data[attr])
            elif isinstance(attr, FunctionType):
                execString = attr.__name__ + '('
                for values in func:
                    execString += str(func) + ','
                execString = execString[:-1] + ')'
                exec(execString)
            else:
                print('Key is not updated or TypeError?')
        else:
            self = update_func(self)


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
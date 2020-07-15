import pygame
import pygame.freetype

from types import FunctionType
from varname import nameof
from pygame_gui_base import *
pygame.init()

DEFAULT_FCOLOR = (0, 0, 0) #black
DEFAULT_BCOLOR = (255, 255, 255) #white
DEFAULT_SIZE = 16 #in px
DEFAULT_FONT = pygame.freetype.SysFont('arial', DEFAULT_SIZE)

DEFAULT_HFCOLOR = (255, 0, 255) #magenta
DEFAULT_HBCOLOR = (255, 255, 0)  #yellow
DEFAULT_SLIDERCOLOR = (80, 80, 80)

def std_text(text):
    resText = ''
    i = 0
    while i < len(text):
        while text[i] == ' ':
            i += 1
        j = i
        while text[i] != ' ':
            i += 1
            if i == len(text):
                break
        resText += text[j:i]
        if i != len(text):
            resText += ' '
    return resText

def word_wrap(text, font, color, box, padding_left, padding_right = 2):
    text = std_text(text)

    boxWidth = box.get_width() - padding_left - padding_right
    sentenceWidth = 0
    surf = pygame.Surface((boxWidth, box.get_height()), pygame.SRCALPHA)
    i = 0
    k = 0
    lap = 0

    while i < len(text):
        temp = font.render(text[i])[0]

        sentenceWidth += temp.get_width() + 1
        if sentenceWidth > boxWidth or i + 1 == len(text):
            if i != len(text) - 1:
                i -= 1
                while not text[i + 1] == ' ':
                    i -= 1

                textImg = font.render(text[k:i + 1], color)[0]
                surf.blit(textImg, (0, lap * (font.get_sized_height() - 2)))
                lap += 1
                k = i + 2
                sentenceWidth = 0
            else:
                textImg = font.render(text[k:], color)[0]
                surf.blit(textImg, (0, lap * (font.get_sized_height() - 2)))
        i += 1
    return surf

class TEXT(GUI_OBJ):
    def __init__(self, text, pos=(30, 30), fcolor=DEFAULT_FCOLOR, font=DEFAULT_FONT):
        self.text = text
        self.pos = pos
        self.fcolor = fcolor
        self.font = font

        self.hover = False
        self.text_img = font.render(text, fcolor)[0]

        self.hover_func = None
        self.hover_img = None
        self.blit_once = False

    def set_hover(self, ishover, hover_img = DEFAULT_HFCOLOR):
        self.hover = ishover
        if isinstance(hover_img, tuple) and len(hover_img) == 3:
            self.hover_fcolor = hover_img
        elif isinstance(hover_img, pygame.Surface):
            self.hover_img = hover_img
        elif isinstance(hover_img, FunctionType):
            self.hover_func = hover_img
        else:
            raise TypeError

    def set_hover_function(self, func):
        self.hover_func = func

    def blit(self, surf):
        if not self.blit_once:
            self.rect = surf.blit(self.text_img, self.pos)
            self.blit_once = True
        if self.hover:
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if self.hover_func:
                    self.text_img = self.hover_func(self.img)
                elif self.hover_img:
                    self.text_img = self.hover_img
                else:
                    self.text_img = self.font.render(self.text, self.hover_fcolor)[0]

            else:
                self.text_img = self.font.render(self.text, self.fcolor)[0]

        surf.blit(self.text_img, self.rect)

class TEXT_BOX(GUI_OBJ):
    def __init__(self, text, size, pos=(50, 50), ppos=(0, 0),
                 fcolor=DEFAULT_FCOLOR,
                 b_img=DEFAULT_BCOLOR,
                 font=DEFAULT_FONT,
                 padding_right = 5):

        self.surf = pygame.Surface(size)

        self.text_img = word_wrap(text, font, fcolor, self.surf, ppos[0], padding_right)
        self.b_img = b_img
        self.pos = pos
        if not isinstance(self.b_img, pygame.Surface):
            self.surf.fill(self.b_img)
        else:
            self.b_img = pygame.transform.smoothscale(self.b_img, size)
            self.surf = self.b_img
        self.ppos = ppos
        self.surf.blit(self.text_img, ppos)

        self.hover = False
        self.hover_func = None
        self.hover_img = None
        self.border = False
        self.blit_once = False

    def set_hover(self, ishover, hover_img=DEFAULT_HBCOLOR):
        self.hover = ishover
        if isinstance(hover_img, tuple) and len(hover_img) == 3:
            self.hover_bcolor = hover_img
        elif isinstance(hover_img, pygame.Surface):
            self.hover_bimg = hover_img
        elif isinstance(hover_img, FunctionType):
            self.hover_func = hover_img
        else:
            raise TypeError

    def set_border(self, haveborder, borderColor, borderThickness):
        if borderThickness < 1:
            raise ValueError
        if haveborder:
            self.border = haveborder
            self.borderColor = borderColor
            self.borderThickness = borderThickness

    def blit(self, surf):
        if not self.blit_once:
            self.surf.blit(self.text_img, self.ppos)
            self.rect = surf.blit(self.surf, self.pos)
            self.blit_once = True
        if self.hover:
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if self.hover_func:
                    self.hover_bimg = self.hover_func(self.surf)
                elif self.hover_img:
                    self.surf = self.hover_img
                else:
                    self.surf.fill(self.hover_bcolor)
            else:
                if not isinstance(self.b_img, pygame.Surface):
                    self.surf.fill(self.b_img)
                else:
                    self.surf.fill((0, 0, 0))
                    self.surf.blit(self.b_img, (0, 0))

            self.surf.blit(self.text_img, self.ppos)
        surf.blit(self.surf, self.rect)

        if self.border:
            point1 = (self.rect.x, self.rect.y)
            point2 = (self.rect.right, self.rect.y)
            point4 = (self.rect.x, self.rect.bottom)
            point3 = (self.rect.right, self.rect.bottom)
            pygame.draw.line(surf, self.borderColor, point1, point2, self.borderThickness)
            pygame.draw.line(surf, self.borderColor, point2, point3, self.borderThickness)
            pygame.draw.line(surf, self.borderColor, point3, point4, self.borderThickness)
            pygame.draw.line(surf, self.borderColor, point1, point4, self.borderThickness)

class BUTTON(TEXT_BOX):
    def __init__(self, text, size, pos=(50, 50), ppos=(0, 0),
                 fcolor=DEFAULT_FCOLOR,
                 b_img=DEFAULT_BCOLOR,
                 font=DEFAULT_FONT,
                 padding_right=5):
        super().__init__(text, size, pos, ppos,
                 fcolor,
                 b_img,
                 font,
                 padding_right)

        self.ClickUpFunc = None
        self.ClickDownFunc = None
        self.ClickUpArgs = None
        self.ClickDownArgs = None

    def setClickUpFunc(self, func, *args):
        self.ClickUpArgs = args
        self.ClickUpFunc = func

    def setClickDownFunc(self, func, *args):
        self.ClickDownArgs = args
        self.ClickDownFunc = func

    def CheckonClickUp(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.ClickUpFunc:
            return self.ClickUpFunc(self.ClickUpArgs)

    def CheckonClickDown(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.ClickDownFunc:
            return self.ClickDownFunc(self.ClickDownArgs)

#TODO: DROPDOWN LIST and fix SLIDER
class SLIDER(GUI_OBJ):
    def __init__(self, startpos, endpos, minimum_value, maximum_value, _step = 1, slideColor = (0, 0, 0), slideThickness = 2):
        self.start_pos = startpos
        self.end_pos = endpos
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.step = _step

        self.slideColor = slideColor
        self.slideThickness = slideThickness

        self.slider = self.set_baseslider((10, 21), 2, DEFAULT_SLIDERCOLOR)

    def set_slide(self, surf_img):
        self.slider = surf_img

    def set_baseslider(self, size, borderThickness, borderColor):
        sliderSurf = pygame.Surface(size, pygame.SRCALPHA)
        width, height = size
        #create hexagon slider
        point1 = (width // 2, 0)
        point2 = (width, height // 3)
        point3 = (width, (height // 3) * 2)
        point4 = (width // 2, height)
        point5 = (0, (height // 3) * 2)
        point6 = (0, height // 3)
        pygame.draw.line(sliderSurf, borderColor, point1, point2, borderThickness)
        pygame.draw.line(sliderSurf, borderColor, point2, point3, borderThickness)
        pygame.draw.line(sliderSurf, borderColor, point3, point4, borderThickness)
        pygame.draw.line(sliderSurf, borderColor, point4, point5, borderThickness)
        pygame.draw.line(sliderSurf, borderColor, point5, point6, borderThickness)
        pygame.draw.line(sliderSurf, borderColor, point6, point1, borderThickness)

        return sliderSurf

    def blit(self, surf):
        pygame.draw.line(surf, self.slideColor, self.start_pos, self.end_pos, self.slideThickness)
        surf.blit(self.slider, (self.start_pos[0], self.start_pos[1] - self.slider.get_height() // 2))
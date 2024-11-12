import sys
import random

import pygame
from pygame import KEYDOWN
from pygame.locals import QUIT, MOUSEBUTTONUP
import xml.etree.ElementTree as ET

"""
class Node:
    def __init__(self,ele):
        self.ele = ele
        self.next = []

tree = ET.parse('save.xml')
root = tree.getroot()

root_node = Node(root)
que = [(0, root_node)]
while que:
    pre, now = que.pop(0)
    if pre:
        pre.next.append(now)
    que += [ (now, Node(i)) for i in now.ele ]
"""

class Text:
    def __init__(self, canvas, text, pos):
        self.canvas = canvas
        self.pygame = pygame
        self.pos = pos
        self.color = (0, 0, 0)

        self.text = text
        self.font = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.color)

    def set_pos(self, pos):
        self.pos = pos

    def set_text(self, text):
        self.text = text
        self.font = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.color)

    def update(self):
        self.canvas.blit(self.font, self.pos)

class Input_box:
    def __init__(self, canvas, pos):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.size = (100, 30)
        self.activate = False
        self.color = (200,200,200)
        self.text = Text(self.canvas, "", self.pos)
        self.pygame.draw.rect(self.canvas, self.color, self.pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def update(self, **kwargs):
        if ("click" in kwargs) and (kwargs["click"]) and self.hover():
            self.activate = not self.activate
        if self.activate and ("key" in kwargs) and (kwargs["key"]):
            if kwargs["key"] != "del":
                self.text.set_text(self.text.text+kwargs["key"])
            else:
                self.text.set_text(self.text.text[0:-1])

        self.pygame.draw.rect(self.canvas, self.color, self.pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.text.update()

    def hover(self):
        (x, y) = self.pygame.mouse.get_pos()
        return  (self.pos[0] <= x <= self.pos[0]+self.size[0]) and (self.pos[1] <= y <= self.pos[1]+self.size[1])

class button:
    def __init__(self, canvas, event, pos:list, text:str):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.event = event

        self.size = (30,30)
        self.color_1 = (200,100,100)
        self.color_2 = (100,100,100)
        self.color = self.color_2

        self.text = text
        self.text_color = (0, 0, 0)
        self.font_text = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.text_color)
        self.text_pos = [self.pos[0] + self.font_text.get_rect().width // 2,
                         self.pos[1] + self.font_text.get_rect().height // 4]

        self.activate = False

        self.pygame.draw.rect(self.canvas, self.color, self.pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def update(self, **kwargs):
        if ("click" in kwargs) and (kwargs["click"]) and self.hover():
            self.activate = not self.activate

        if self.activate:
            self.activate = self.event() # 連續動作

        self.pygame.draw.rect(self.canvas, self.color, self.pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.canvas.blit(self.font_text, self.text_pos)

    def hover(self):
        (x, y) = self.pygame.mouse.get_pos()
        return  (self.pos[0] <= x <= self.pos[0]+self.size[0]) and (self.pos[1] <= y <= self.pos[1]+self.size[1])

    def set_text(self, text):
        self.text = text
        self.font_text = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.text_color)
    def set_pos(self, pos):
        self.pos = pos
        self.text_pos = [self.pos[0] + self.font_text.get_rect().width // 2,
                         self.pos[1] + self.font_text.get_rect().height // 4]

class Input_val:
    def __init__(self, canvas, pos):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.in_ = Input_box(self.canvas, self.pos)
        self.btn_ = button(self.canvas, self.event, [self.pos[0]+100, self.pos[1]], "OK")

    def update(self, **kwargs):
        self.in_.update(**kwargs)
        self.btn_.update(**kwargs)

    def event(self):
        print(self.in_.text.text)
        return False


class Node:
    def __init__(self, canvas, pos:list, text:str):
        self.pygame = pygame
        self.canvas = canvas

        self.pos = pos
        self.radius = 40
        self.color_1 = (100, 200, 200)
        self.color_2 = (200, 200, 200)
        self.color = self.color_1

        self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius,2)

        self.text = text
        self.text = Text(self.canvas, text, self.pos)

        self.move_btn = button(self.canvas, self.move_node, [self.pos[0], self.pos[1]-80], "M")
        self.add_btn = button(self.canvas, self.add_node, [self.pos[0]-35, self.pos[1]-80], "+")
        self.del_btn = button(self.canvas, self.del_node, [self.pos[0]-70, self.pos[1]-80], "-")

        self.activate = False

        self.next = {}
        self.pre = {}
        self.link = {}
        self.del_node_name = []

    def add_node(self):
        name = str(random.randint(1,100))
        new_node_pos = list(self.pos).copy()
        new_node_pos[0] += 100
        new_node_pos[1] += len(self.next)*100

        self.next[name] = Node(self.canvas, new_node_pos, name)
        self.link[name] = Link(self.canvas, self.pos, new_node_pos)
        self.next[name].pre[self.text.text] = self
        self.next[name].link[self.text.text] = self.link[name]
        return False

    def del_next(self, name):
        del self.next[name]

    def search_next(self, name):

        pass

    def del_node(self):
        for i in self.pre:
            self.pre[i].next[self.text.text] = None
        return False

    def move_node(self):
        self.set_pos(self.pygame.mouse.get_pos())
        return True

    def update(self, **kwargs):
        if self.hover():
            self.color = self.color_2
            if kwargs["click"]:
                if self.move_btn.activate:
                    self.move_btn.activate = False
                self.activate = not self.activate
        else:
            self.color = self.color_1

        for i in self.link:
            self.link[i].update()

        del_node_name = []
        for i in self.next:
            if self.next[i] == None:
                del_node_name.append(i)
            else:
                self.next[i].update(click=kwargs["click"])

        while del_node_name:
            name = del_node_name.pop()
            del self.link[name]
            del self.next[name]

        if self.activate:
            self.move_btn.update(click=kwargs["click"])
            self.add_btn.update(click=kwargs["click"])
            self.del_btn.update(click=kwargs["click"])

        pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
        self.text.update()

    def set_pos(self, pos):
        self.pos = pos
        self.text.set_pos(pos)

        for i in self.link:
            if i in self.next:
                self.link[i].pos1 = self.pos
            elif i in self.pre:
                self.link[i].pos2 = self.pos

        self.move_btn.set_pos((self.pos[0], self.pos[1]-80))
        self.add_btn.set_pos((self.pos[0]-35, self.pos[1]-80))
        self.del_btn.set_pos((self.pos[0]-70, self.pos[1]-80))
    """
        in node btn function：
            (x-h)**2+(y-k)**2=r**2
    """
    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0]-self.pos[0])**2+((mouse_pos[1]-self.pos[1])**2) <= self.radius**2

class Link:
    def __init__(self, canvas, node1_pos, node2_pos):
        self.canvas = canvas
        self.pygame = pygame
        self.color = (100, 200, 200)
        self.pos1 = node1_pos
        self.pos2 = node2_pos

        self.pygame.draw.line(self.canvas, self.color, self.pos1, self.pos2, 2)

    def update(self):
        self.pygame.draw.line(self.canvas, self.color, self.pos1, self.pos2, 2)



windows_size = (800, 600)
pygame.init()
window_surface = pygame.display.set_mode(windows_size)
pygame.display.set_caption("node")
window_surface.fill((255, 255, 255))

main_node = Node(window_surface, [400,300], "main")
in1 = Input_val(window_surface, [200,200])


pygame.display.update()
while True:
    window_surface.fill((255, 255, 255))
    pygame_event = pygame.event.get()

    t = {}
    for e in pygame_event:
        t[e.type] = e

    if QUIT in t:
        pygame.quit()
        sys.exit()

    click = False
    if MOUSEBUTTONUP in t:
        click = True

    key = False
    if KEYDOWN in t:
        if (ord("0") <= t[KEYDOWN].key <= ord("9")) or \
            (ord("A") <= t[KEYDOWN].key <= ord("Z")) or \
            (ord("a") <= t[KEYDOWN].key <= ord("z")):
            key = chr(t[KEYDOWN].key)
        elif t[KEYDOWN].key == pygame.K_BACKSPACE:
            key = "del"

    # line -> node
    # node
    main_node.update(click=click)
    # btn

    # input
    in1.update(click=click, key=key)

    pygame.display.update()

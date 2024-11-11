import sys

import pygame
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
            self.event()

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
        self.text_color = (0, 0, 0)
        self.font_text = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.text_color)
        self.text_pos = [self.pos[0]-self.font_text.get_rect().width//2, self.pos[1]-self.font_text.get_rect().height//2]

        self.move_btn = button(self.canvas, self.move_node, (self.pos[0], self.pos[1]-80), "M")
        self.add_btn = button(self.canvas, self.add_node, (self.pos[0]-35, self.pos[1]-80), "+")

        self.activate = False

        self.next = {}
        self.pre = {}
        self.link = {}

    def add_next(self, name):
        new_node_pos = self.pos.copy()
        new_node_pos[0] += 100
        new_node_pos[1] += len(self.next)*100

        self.next[name] = Node(self.canvas, new_node_pos, name)
        self.link[name] = Link(self.canvas, self.pos, new_node_pos)
        self.next[name].pre[self.text] = self
        self.next[name].link[self.text] = self.link[name]

    def del_next(self, name):
        del self.next[name]

    def search_next(self, name):
        pass

    def add_node(self):
        pass
    def move_node(self):
        self.set_pos(self.pygame.mouse.get_pos())

    def update(self, **kwargs):
        if self.in_btn( self.pygame.mouse.get_pos() ):
            self.color = self.color_2
            if kwargs["click"]:
                if self.move_btn.activate:
                    self.move_btn.activate = False
                self.activate = not self.activate
        else:
            self.color = self.color_1

        for i in self.link:
            self.link[i].update()
        for i in self.next:
            self.next[i].update(click=kwargs["click"])

        if self.activate:
            self.move_btn.update(click=kwargs["click"])
            self.add_btn.update(click=kwargs["click"])

        pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
        self.canvas.blit(self.font_text, self.text_pos)

    def set_text(self, text):
        self.text = text
        self.font_text = self.pygame.font.SysFont("Arial", 20).render(self.text, False, self.text_color)
    def set_pos(self, pos):
        self.pos = pos
        self.text_pos = [self.pos[0]-self.font_text.get_rect().width//2, self.pos[1]-self.font_text.get_rect().height//2]

        for i in self.link:
            if i in self.next:
                self.link[i].pos1 = self.pos
            elif i in self.pre:
                self.link[i].pos2 = self.pos

        self.move_btn.set_pos((self.pos[0], self.pos[1]-80))
        self.add_btn.set_pos((self.pos[0]-35, self.pos[1]-80))
    """
        in node btn function：
            (x-h)**2+(y-k)**2=r**2
    """
    def in_btn(self, mouse_pos):
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
main_node.add_next("test1")
main_node.add_next("test2")
main_node.next["test1"].add_next("test3")
main_node.next["test1"].add_next("test4")


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

    # line -> node
    # node
    main_node.update(click=click)
    # btn

    pygame.display.update()

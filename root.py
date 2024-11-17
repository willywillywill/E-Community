import sys

from pygame import KEYDOWN
from pygame.locals import QUIT, MOUSEBUTTONUP
import xml.etree.ElementTree as ET
from component import *

class Node:
    def __init__(self, canvas, pos:list, name:str):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.radius = 40
        self.color_1 = (100, 200, 200)
        self.color_2 = (200, 200, 200)
        self.color = self.color_1

        self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius,2)

        self.text = Text(self.canvas, name, [self.pos[0]-10, self.pos[1]-10])

        self.move_btn = button(self.canvas, self.move_node, [self.pos[0], self.pos[1]-80], "M")
        self.add_btn = button(self.canvas, self.add_node, [self.pos[0]-35, self.pos[1]-80], "+")
        self.del_btn = button(self.canvas, self.del_node, [self.pos[0]-70, self.pos[1]-80], "-")

        self.add_input_activate = False
        self.add_input = Input_box(self.canvas, [self.pos[0]-35, self.pos[1]-120])

        self.activate = False

        self.next = {}
        self.pre = {}
        self.link = {}
        self.del_node_name = []

    def add_node(self):
        if self.add_input_activate:
            name = self.add_input.get_val()
            self.add_input.cls()
            new_node_pos = list(self.pos).copy()
            new_node_pos[0] += 100
            new_node_pos[1] += len(self.next) * 100

            self.next[name] = Node(self.canvas, new_node_pos, name)
            self.link[name] = Link(self.canvas, self.pos, new_node_pos)
            self.next[name].pre[self.text.text] = self
            self.next[name].link[self.text.text] = self.link[name]
            self.activate = False

        self.add_input_activate = not self.add_input_activate

        return False

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

                if not self.activate:
                    self.add_input_activate = False

        else:
            self.color = self.color_1

        for i in self.link:
            self.link[i].update()

        del_node_name = []
        for i in self.next:
            if self.next[i] == None:
                del_node_name.append(i)
            else:
                self.next[i].update(**kwargs)

        while del_node_name:
            name = del_node_name.pop()
            del self.link[name]
            del self.next[name]

        if self.add_input_activate:
            self.add_input.update(**kwargs)

        if self.activate:
            self.move_btn.update(**kwargs)
            self.add_btn.update(**kwargs)
            self.del_btn.update(**kwargs)

        self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
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
        self.add_input.set_pos((self.pos[0]-35, self.pos[1]-120))

    """
        in node btn function：
            (x-h)**2+(y-k)**2=r**2
    """
    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0]-self.pos[0])**2+((mouse_pos[1]-self.pos[1])**2) <= self.radius**2


def run():
    windows_size = (800, 600)
    pygame.init()
    window_surface = pygame.display.set_mode(windows_size)
    pygame.display.set_caption("root")
    window_surface.fill((255, 255, 255))

    main_node = Node(window_surface, [400,300],  "root")

    pygame.display.update()
    while True:
        window_surface.fill((255, 255, 255))

        t = {}
        for e in pygame.event.get():
            t[e.type] = e

        if QUIT in t:
            pygame.quit()
            break

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

        main_node.update(click=click, key=key)
        pygame.display.update()

    file = "save.xml"
    tree = ET.parse(file)
    root = tree.parse(file)
    root.clear()

    que = [(root,main_node)]
    while que:
        pre,now = que.pop(0)

        new_ele = ET.SubElement(ET.Element("node"), 'node')
        new_ele.set("name", now.text.text)
        new_ele.set("info", "")
        pre.append(new_ele)

        que += [ (new_ele, now.next[i]) for i in now.next ]

    tree.write(file)
    sys.exit()

if __name__ == "__main__":
    run()
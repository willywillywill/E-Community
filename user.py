import sys
import time
from pygame import KEYDOWN
from pygame.locals import QUIT, MOUSEBUTTONUP
import xml.etree.ElementTree as ET
from component import *

class Node:
    def __init__(self, canvas, element, pos=[100,100]):
        self.pygame = pygame
        self.canvas = canvas
        self.element = element
        self.pos = pos

        self.activate =  False
        self.activate_info = False

        self.radius = 40
        self.color_1 = (100, 200, 200)
        self.color_2 = (200, 200, 200)
        self.color = self.color_1

        self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
        self.text = Text(self.canvas, self.element.get("name"), [self.pos[0]-10, self.pos[1]-10])

        self.info_text = Input_box(self.canvas, [self.pos[0]-30, self.pos[1]-100])
        self.info_text.set_text(self.element.get("info"))

        self.next = []
        self.link = []
        self.info = []

    def update(self, **kwargs):
        if self.hover() and ("click" in kwargs) and kwargs["click"]:
            self.activate = not self.activate

        if self.activate:
            for i in self.info:
                i.update()

            self.info_text.update(**kwargs)
            self.element.set("info", self.info_text.get_val())


        for i in self.link:
            i.update()
        for i in self.next:
            i.update(**kwargs)

        self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
        self.text.update()

    def info_show(self):
        self.activate_info = True

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0] - self.pos[0]) ** 2 + ((mouse_pos[1] - self.pos[1]) ** 2) <= self.radius ** 2




def run():
    def build(node: Node, n=1):
        for i, child in enumerate(node.element):
            new_node = Node(window_surface, child, [node.pos[0] + n * 100, node.pos[1] + i * 100])
            node.link.append(Link(window_surface, node.pos, new_node.pos))
            node.next.append(new_node)
            build(new_node, n)
        n += 1
    windows_size = (800, 600)
    pygame.init()
    window_surface = pygame.display.set_mode(windows_size)
    pygame.display.set_caption("user")
    window_surface.fill((255, 255, 255))

    file = "save.xml"
    tree = ET.parse(file)
    root = tree.parse(file)[0]

    pos = [100, 300]

    main_node = Node(window_surface, root, pos)
    build(main_node)
    t1 = time.time()

    while 1:
        window_surface.fill((255, 255, 255))
        t2 = time.time()
        if t2-t1 > 10:
            t1 = t2
            tree = ET.parse(file)
            root = tree.parse(file)[0]
            main_node = Node(window_surface, root, pos)
            build(main_node)

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
        tree.write(file)
    sys.exit()

if __name__ == "__main__":
    run()
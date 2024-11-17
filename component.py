import pygame

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
        if self.activate:
            self.color = (100,200,200)
        else:
            self.color = (200,200,200)
        if self.activate and ("key" in kwargs) and (kwargs["key"]):
            if kwargs["key"] != "del":
                self.text.set_text(self.text.text+kwargs["key"])
            else:
                self.text.set_text(self.text.text[0:-1])

        self.pygame.draw.rect(self.canvas, self.color, self.pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.text.update()

    def set_pos(self, pos):
        self.pos = pos
        self.text.set_pos(self.pos)

    def set_text(self, text):
        self.text.set_text(text)

    def get_val(self):
        return self.text.text

    def cls(self):
        self.text.set_text("")

    def hover(self):
        (x, y) = self.pygame.mouse.get_pos()
        return  (self.pos[0] <= x <= self.pos[0]+self.size[0]) and (self.pos[1] <= y <= self.pos[1]+self.size[1])

class button:
    def __init__(self, canvas, event, pos:list, text:str, size=(30,30)):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.event = event

        self.size = size
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


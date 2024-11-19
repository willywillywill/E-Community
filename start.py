import sys
from component import *
import root
import user
from pygame.locals import QUIT, MOUSEBUTTONUP


windows_size = (800, 600)
pygame.init()
window_surface = pygame.display.set_mode(windows_size)
pygame.display.set_caption("start")
window_surface.fill((255, 255, 255))

root = button(window_surface, root.run, [100,100], "root", size=(100,100))
user = button(window_surface, user.run, [300,100], "user", size=(100,100))

while True:
    window_surface.fill((255, 255, 255))

    t = {}
    for e in pygame.event.get():
        t[e.type] = e

    if QUIT in t:
        pygame.quit()
        sys.exit()

    click = False
    if MOUSEBUTTONUP in t:
        click = True

    root.update(click=click)
    user.update(click=click)

    pygame.display.update()


import sys

import pygame

windows_size = (800, 600)
pygame.init()
window_surface = pygame.display.set_mode(windows_size)
pygame.display.set_caption("node")
window_surface.fill((255, 255, 255))

while True:
    window_surface.fill((255, 255, 255))
    pygame_event = pygame.event.get()
    for e in pygame_event:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            print(e.key)
    pygame.display.update()

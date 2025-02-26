import pygame
#import psutil

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y=10, x=10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)

#def show_fps(clock, y=10, x=10):
#    fps = int(clock.get_fps())
#    debug(f"FPS: {fps}", y, x)
#
#def show_memory_usage(y=40, x=10):
#    process = psutil.Process()
#    memory_info = process.memory_info()
#    memory_usage = memory_info.rss / (1024 * 1024)  # Convert to MB
#    debug(f"Memory Usage: {memory_usage:.2f} MB", y, x)
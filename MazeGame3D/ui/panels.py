import pygame

def draw_panel(surface, rect, radius=18, fill=(15, 18, 28, 200), border=(120, 160, 255, 90), border_w=2):
    x, y, w, h = rect
    panel = pygame.Surface((w, h), pygame.SRCALPHA)

    shadow = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 120), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (x + 6, y + 6))

    pygame.draw.rect(panel, fill, panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, border, panel.get_rect(), width=border_w, border_radius=radius)
    surface.blit(panel, (x, y))

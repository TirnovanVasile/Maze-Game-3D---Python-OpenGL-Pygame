import pygame
from ui.panels import draw_panel


def draw_hud(screen, game):
    w, h = screen.get_width(), screen.get_height()
    font = pygame.font.Font(None, 34)
    small = pygame.font.Font(None, 26)

    panel_rect = (18, 18, 380, 170)
    draw_panel(screen, panel_rect, radius=18)

    x, y, pw, ph = panel_rect
    pad = 18

    header_title = small.render("OBIECTIVE :", True, (170, 210, 255))
    objective_text = "Gaseste iesirea!" if game.keys_collected >= game.keys_total else "Colecteaza cheile"
    header_obj = small.render(objective_text, True, (200, 230, 255))

    screen.blit(header_title, (x + pad, y + pad))
    screen.blit(header_obj, (x + pad + header_title.get_width() + 14, y + pad))

    exit_label = font.render(f"Chei iesire: {game.keys_collected}/{game.keys_total}", True, (255, 215, 80))
    screen.blit(exit_label, (x + pad, y + pad + 30))

    bar_x = x + pad
    bar_y = y + pad + 66
    bar_w = pw - 2 * pad
    bar_h = 14

    pygame.draw.rect(screen, (40, 45, 60, 220), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
    t = 0 if game.keys_total == 0 else max(0.0, min(1.0, game.keys_collected / game.keys_total))
    pygame.draw.rect(screen, (255, 215, 80, 220), (bar_x, bar_y, int(bar_w * t), bar_h), border_radius=10)

    pill_text = font.render(f"Chei usi: {game.door_keys_collected}", True, (220, 230, 255))
    pill_rect = pygame.Rect(x + pad, y + pad + 92, pill_text.get_width() + 22, 34)
    pygame.draw.rect(screen, (60, 70, 95, 210), pill_rect, border_radius=999)
    pygame.draw.rect(screen, (140, 175, 255, 80), pill_rect, width=2, border_radius=999)
    screen.blit(pill_text, (pill_rect.x + 11, pill_rect.y + 6))

    if game.show_interaction_hint:
        hint = font.render("Apasa E pentru a interactiona", True, (120, 255, 160))
        hw = hint.get_width()
        hint_rect = (w // 2 - (hw + 44) // 2, h - 90, hw + 44, 52)
        draw_panel(screen, hint_rect, radius=16, fill=(10, 14, 22, 200), border=(120, 255, 180, 110))
        screen.blit(hint, (hint_rect[0] + 22, hint_rect[1] + 12))

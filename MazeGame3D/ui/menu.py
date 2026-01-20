import pygame
from ui.panels import draw_panel


def draw_menu(screen):
    w, h = screen.get_width(), screen.get_height()
    title_font = pygame.font.Font(None, 96)
    sub_font = pygame.font.Font(None, 36)
    btn_font = pygame.font.Font(None, 44)

    bg = pygame.Surface((w, h))
    for i in range(h):
        t = i / max(1, h - 1)
        col = (int(8 + 20 * t), int(10 + 18 * t), int(18 + 28 * t))
        pygame.draw.line(bg, col, (0, i), (w, i))
    screen.blit(bg, (0, 0))

    card_w, card_h = 620, 360
    card_x = w // 2 - card_w // 2
    card_y = h // 2 - card_h // 2
    draw_panel(screen, (card_x, card_y, card_w, card_h), radius=22, fill=(15, 18, 28, 210), border=(255, 215, 80, 110))

    title = "LABIRINT 3D"
    glow = title_font.render(title, True, (255, 215, 80))
    screen.blit(glow, (card_x + card_w // 2 - glow.get_width() // 2 + 2, card_y + 40 + 2))
    screen.blit(glow, (card_x + card_w // 2 - glow.get_width() // 2, card_y + 40))

    subtitle = sub_font.render("Exploreaza - Colecteaza chei - Gaseste iesirea", True, (170, 210, 255))
    screen.blit(subtitle, (card_x + card_w // 2 - subtitle.get_width() // 2, card_y + 135))

    start_txt = btn_font.render("SPACE  -  Start", True, (255, 255, 255))
    esc_txt = btn_font.render("ESC    -    Iesire", True, (220, 220, 220))

    pill1 = pygame.Rect(card_x + 150, card_y + 200, card_w - 300, 52)
    pygame.draw.rect(screen, (60, 70, 95, 200), pill1, border_radius=999)
    pygame.draw.rect(screen, (140, 175, 255, 90), pill1, width=2, border_radius=999)
    screen.blit(start_txt, (pill1.x + pill1.w // 2 - start_txt.get_width() // 2, pill1.y + 10))

    pill2 = pygame.Rect(card_x + 150, card_y + 265, card_w - 300, 52)
    pygame.draw.rect(screen, (45, 52, 70, 200), pill2, border_radius=999)
    pygame.draw.rect(screen, (200, 200, 200, 70), pill2, width=2, border_radius=999)
    screen.blit(esc_txt, (pill2.x + pill2.w // 2 - esc_txt.get_width() // 2, pill2.y + 10))


def draw_win_screen(screen):
    w, h = screen.get_width(), screen.get_height()
    title_font = pygame.font.Font(None, 96)
    sub_font = pygame.font.Font(None, 40)
    btn_font = pygame.font.Font(None, 44)

    screen.fill((8, 10, 18))

    card_w, card_h = 640, 360
    card_x = w // 2 - card_w // 2
    card_y = h // 2 - card_h // 2
    draw_panel(screen, (card_x, card_y, card_w, card_h), radius=22, fill=(12, 18, 20, 220), border=(120, 255, 170, 120))

    title = "AI CASTIGAT!"
    glow = title_font.render(title, True, (120, 255, 170))
    screen.blit(glow, (card_x + card_w // 2 - glow.get_width() // 2 + 2, card_y + 45 + 2))
    screen.blit(glow, (card_x + card_w // 2 - glow.get_width() // 2, card_y + 45))

    msg = sub_font.render("Felicitari! Ai gasit iesirea din labirint.", True, (180, 220, 255))
    screen.blit(msg, (card_x + card_w // 2 - msg.get_width() // 2, card_y + 145))

    restart_txt = btn_font.render("SPACE  -  Restart", True, (255, 255, 255))
    exit_txt = btn_font.render("ESC  -  Iesire", True, (230, 230, 230))

    pill1 = pygame.Rect(card_x + 160, card_y + 205, card_w - 320, 52)
    pygame.draw.rect(screen, (40, 70, 60, 210), pill1, border_radius=999)
    pygame.draw.rect(screen, (120, 255, 170, 110), pill1, width=2, border_radius=999)
    screen.blit(restart_txt, (pill1.x + pill1.w // 2 - restart_txt.get_width() // 2, pill1.y + 10))

    pill2 = pygame.Rect(card_x + 160, card_y + 270, card_w - 320, 52)
    pygame.draw.rect(screen, (45, 52, 70, 210), pill2, border_radius=999)
    pygame.draw.rect(screen, (200, 200, 200, 70), pill2, width=2, border_radius=999)
    screen.blit(exit_txt, (pill2.x + pill2.w // 2 - exit_txt.get_width() // 2, pill2.y + 10))


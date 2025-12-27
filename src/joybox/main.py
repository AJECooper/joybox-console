import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("JoyBox - Day 1")

    running = True
    font = pygame.font.SysFont("Arial", 32)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 30))

        text = font.render("JoyBox Started!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(640/2, 480/2))
        screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

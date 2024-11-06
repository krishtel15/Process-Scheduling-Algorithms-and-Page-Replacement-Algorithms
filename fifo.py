import pygame
import sys

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class FIFO:
    def __init__(self, frames):
        self.frames = frames
        self.page_faults = 0
        self.pages = []
        self.frame_contents = [None] * frames

    def add_page(self, page):
        self.pages.append(page)
        self.replace(page)

    def replace(self, page):
        if None in self.frame_contents:
            self.frame_contents[self.frame_contents.index(None)] = page
            self.page_faults += 1
        else:
            replaced_page = self.frame_contents.pop(0)
            self.frame_contents.append(page)
            self.page_faults += 1
            return replaced_page

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    frames = 5
    fifo = FIFO(frames)
    font = pygame.font.SysFont("Arial", 20)

    input_str = ""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if input_str:
                        fifo.add_page(int(input_str))
                        input_str = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.unicode.isdigit():
                    input_str += event.unicode

        screen.fill(BLACK)

        # Draw title
        pygame.draw.rect(screen, WHITE, (10, 10, WIDTH - 20, 50))
        draw_text(screen, "Page Replacement Algorithm - First In First Out", font, BLACK, 20, 30)

        # Draw input field
        pygame.draw.rect(screen, WHITE, (10, 70, WIDTH - 20, 50))
        draw_text(screen, "Enter page number: " + input_str, font, BLACK, 20, 90)

        # Draw frames and page faults
        pygame.draw.rect(screen, WHITE, (10, 130, WIDTH - 20, 50))
        draw_text(screen, f"Frames: {frames}, Page Faults: {fifo.page_faults}", font, BLACK, 20, 150)

        # Draw pages
        pygame.draw.rect(screen, WHITE, (10, 190, WIDTH - 20, 50))
        draw_text(screen, "Pages: " + str(fifo.pages), font, BLACK, 20, 210)

        # Draw frame contents
        pygame.draw.rect(screen, WHITE, (10, 250, WIDTH - 20, 50))
        draw_text(screen, "Frame Contents: " + str(fifo.frame_contents), font, BLACK, 20, 270)

        # Draw frame boxes
        for i in range(frames):
            pygame.draw.rect(screen, GREEN, (10 + i * 100, 320, 90, 50))
            if fifo.frame_contents[i] is not None:
                draw_text(screen, str(fifo.frame_contents[i]), font, BLACK, 20 + i * 100, 340)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
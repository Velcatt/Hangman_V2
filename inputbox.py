import pygame

pygame.init()
COLOR_ACTIVE = pygame.Color("white")
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text="", disabled=False, maxlength=45):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.last_input = ""
        self.disabled = disabled
        self.maxlength = maxlength

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not self.disabled:
                    self.last_input = self.text
                    self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.maxlength:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        self.txt_surface = FONT.render(self.text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset_last_input(self):
        self.last_input = ""

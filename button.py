import pygame

pygame.init()
FONT = pygame.font.Font(None, 32)


class Button:

    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.last_input = ""

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseposition = pygame.mouse.get_pos()
            if mouseposition[0] > self.rect.topleft[0]:
                if mouseposition[1] > self.rect.topleft[1]:
                    if mouseposition[0] < self.rect.bottomright[0]:
                        if mouseposition[1] < self.rect.bottomright[1]:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, window):
        # Blit the text
        window.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the rect.
        pygame.draw.rect(window, self.color, self.rect, 2)

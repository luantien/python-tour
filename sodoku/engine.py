import pygame
from pygame.locals import (
    KEYDOWN, MOUSEBUTTONDOWN, QUIT,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, K_DELETE, K_BACKSPACE, K_RETURN, K_KP_ENTER, K_SPACE,
    K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,
    K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9
)
from pygame import display, draw, font, mouse
from sodoku import Board


class GameEngine:
    BOARD_NAME = "Sodoku Gameboard"
    BOARD_SIZE = 630
    BOARD_COLORS = {
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "DARK_GREY": (128, 128, 128),
        "LIGHT_GREY": (224, 224, 224),
        "RED": (255, 51, 51),
        "ORANGE": (255, 178, 153),
        "GREEN": (0, 204, 102),
        "BLUE": (0, 128, 255),
    }
    FPS = 60

    def __init__(self, board_size=None):
        self.board_size = self.BOARD_SIZE if not board_size else board_size
        self.area_size = self.board_size / 9

        # Init screen
        pygame.init()
        display.set_caption(self.BOARD_NAME)
        self.screen = display.set_mode(
            (self.board_size, self.board_size + 60)
        )
        self.area_font = font.SysFont("comicsans", 40)

        # Generate game data
        self.board = Board(self.board_size)
        self.key = None

    def sketch_board(self):
        if self.board.selected and self.key is not None:
            self.board.sketch(self.key)

    def reload_board(self):
        self.board.refresh()

    # Get clicked area on the board
    def select_board(self, position):
        if position[0] < self.board_size and position[1] < self.board_size:
            y = int(position[0] // self.area_size)
            x = int(position[1] // self.area_size)
            self.board.select((x, y))
        else:
            return None

    def commit_board(self):
        self.board.commit()

    def solve_board(self):
        loc = self.board.find_next_location()
        if not loc:
            return True
        else:
            x, y = loc

        for num in range(1, 10):
            if self.board.is_safe_state(num, loc):
                self.board.areas[x][y].sketch(num)
                self.board.areas[x][y].save()
                self.board.update_stage(num, loc)
                self.draw_board()
                display.update()
                pygame.time.delay(100)

                if self.solve_board():
                    return True

                self.board.areas[x][y].sketch(0)
                self.board.areas[x][y].save()
                self.board.update_stage(0, loc)
                self.draw_board()
                display.update()
                pygame.time.delay(100)

        return False

    def draw_board(self):
        self.screen.fill(self.BOARD_COLORS["WHITE"])
        # Draw areas
        for i in range(9):
            for j in range(9):
                self.draw_area(self.board.areas[i][j])
        # Draw lines
        for i in range(10):
            line_width = 1
            if i % 3 == 0 and i != 0:
                line_width = 4
            # Draw vertical lines
            draw.line(
                self.screen,
                self.BOARD_COLORS["BLACK"],
                (0, i * self.area_size),
                (self.board_size, i * self.area_size),
                line_width
            )
            # Draw horizontal lines
            draw.line(
                self.screen,
                self.BOARD_COLORS["BLACK"],
                (i * self.area_size, 0),
                (i * self.area_size, self.board_size),
                line_width
            )

    def draw_area(self, area):
        x = area.col * self.area_size
        y = area.row * self.area_size
        value = area.value
        font_color = self.BOARD_COLORS["BLACK"]
        bkg_color = self.BOARD_COLORS["WHITE"]

        if area.default:
            bkg_color = self.BOARD_COLORS["LIGHT_GREY"]
        elif area.selected:
            bkg_color = self.BOARD_COLORS["ORANGE"]

        if area.temp != 0:
            if area.temp is area.value:
                bkg_color = self.BOARD_COLORS["GREEN"]
            else:
                font_color = self.BOARD_COLORS["RED"]
            value = area.temp

        draw.rect(
            self.screen,
            bkg_color,
            # Rectangle (x, y, width, height)
            (x, y, self.area_size, self.area_size)
        )

        if value != 0:
            text = self.area_font.render(str(value), 1, font_color)
            self.screen.blit(
                text,
                (
                    x + (self.area_size / 2 - text.get_width() / 2),
                    y + (self.area_size / 2 - text.get_height() / 2)
                )
            )

    def handle_event(self, event=None):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.reload_board()
            elif event.key in (K_RETURN, K_KP_ENTER):
                self.commit_board()
            elif event.key in (K_0, K_KP0, K_BACKSPACE):
                self.key = 0
            elif event.key in (K_1, K_KP1):
                self.key = 1
            elif event.key in (K_2, K_KP2):
                self.key = 2
            elif event.key in (K_3, K_KP3):
                self.key = 3
            elif event.key in (K_4, K_KP4):
                self.key = 4
            elif event.key in (K_5, K_KP5):
                self.key = 5
            elif event.key in (K_6, K_KP6):
                self.key = 6
            elif event.key in (K_7, K_KP7):
                self.key = 7
            elif event.key in (K_8, K_KP8):
                self.key = 8
            elif event.key in (K_9, K_KP9):
                self.key = 9
            elif event.key is K_SPACE:
                self.solve_board()
            elif event.key is K_DELETE:
                pass
        elif event.type == MOUSEBUTTONDOWN:
            self.select_board(mouse.get_pos())
            self.key = None
        elif event.type == QUIT:
            self.is_running = False

    def launch(self):
        self.is_running = True

        while self.is_running:
            # Event loop
            for event in pygame.event.get():
                self.handle_event(event)
            self.sketch_board()
            # Draw board after any event loop
            self.draw_board()
            # Update display to reflex the event
            pygame.time.Clock().tick(self.FPS)
            display.update()

        pygame.quit()

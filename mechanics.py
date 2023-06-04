######################################################################
#                             Libraries                              #
######################################################################


from pygame import init, font
from pygame import draw, Rect
from pygame import mouse, display, Surface

from pygame import QUIT, quit, event
from pygame import K_ESCAPE

from pygame.key import get_pressed
from pygame.time import get_ticks

from MiniMax import minimum_maximum_algoritm, move_checking
from itertools import product
from sys import exit


######################################################################
#                             Variables                              #
######################################################################


init()
font.init()

WIDTH, HEIGHT = display.Info().current_w // 1.5, display.Info().current_h // 1.5
COMIC_SANS_MS = font.SysFont('Comic Sans MS', 30)
MINIMAL_FIELD_SIZE = min(WIDTH, HEIGHT)
LENGTH = 3


######################################################################
#                             Game Class                             #
######################################################################


class TicTacToe:
    def __init__(self, screen: Surface, display: Surface) -> None:
        self.screen, self.display = screen, display
        self.field = [[0] * 3 for _ in range(3)]
        
        self.point = self.size = point = int(MINIMAL_FIELD_SIZE) // 5
        self.object_scale = 10
        
        self.fields_center_coordinates = sorted([*product(*[range(point, point * 3 + 1, point)] * 2)], key=lambda x: x[::-1])
        self.lines_array = [
            *[((point, point * n), (point * 4, point * n)) for n in [1, 2, 3, 4]],
            *[((point * n, point), (point * n, point * 4)) for n in [1, 2, 3, 4]]
        ]

        self.first_theme_timer, self.second_theme_timer = 0, 0
        self.first_clear_timer, self.second_clear_timer = 0, 0

        self.cross_color, self.circle_color = (255, 0, 0), (0, 255, 0)
        self.color_dictionary = {
            "Back_Ground_Color": (255, 255, 255),
            "Contrast_Color" : (0, 0, 0),
            "Other_not_pressed": (205, 205, 205),
            "Other_pressed": (175, 175, 175),
            "Now_not_pressed": (50, 50, 50),
            "Now_pressed": (80, 80, 80)
        }

        self.buttons_width_center = MINIMAL_FIELD_SIZE // 2 + WIDTH // 2
        self.buttons_dictionary = {
            "Clear Field": Button(
                                self.screen, self.buttons_width_center, HEIGHT * 0.35, WIDTH * 0.2, HEIGHT * 0.2, text="Clear Field", border_radius=10, text_color=self.color_dictionary["Back_Ground_Color"],
                                inactive_color=(self.color_dictionary["Contrast_Color"]), not_pressed_color=self.color_dictionary["Now_not_pressed"], pressed_color=self.color_dictionary["Now_pressed"]
                                ),
            "Theme": Button(
                            self.screen, self.buttons_width_center, HEIGHT * 0.65, WIDTH * 0.2, HEIGHT * 0.2, text="Theme", border_radius=10, text_color=self.color_dictionary["Back_Ground_Color"],
                            inactive_color=(self.color_dictionary["Contrast_Color"]), not_pressed_color=self.color_dictionary["Now_not_pressed"], pressed_color=self.color_dictionary["Now_pressed"]
                            )
        }

    def update(self) -> None:
        self.screen.fill(self.color_dictionary["Back_Ground_Color"])

        self.second_clear_timer = get_ticks()
        self.second_theme_timer = get_ticks()

        self.line_drawing()
        self.game_logic()
        self.elements_drawing()
        self.button_drawing()

    def cross_drawing(self, x, y) -> None:
        x, y = x + self.size, y + self.size
        first_line_coordinates = ((x + self.object_scale, y + self.object_scale), (x + self.size - self.object_scale, y + self.size - self.object_scale))
        second_line_coordinates = ((x + self.size - self.object_scale, y + self.object_scale), (x + self.object_scale, y + self.size - self.object_scale))

        draw.line(self.screen, self.cross_color, *first_line_coordinates, width=10)
        draw.line(self.screen, self.cross_color, *second_line_coordinates, width=10)
    
    def circle_drawing(self, x, y) -> None:
        x, y = x + self.size, y + self.size
        coordinates = ((x + self.object_scale, y + self.object_scale), (self.size - 2 * self.object_scale, self.size - 2 * self.object_scale))

        draw.ellipse(self.screen, self.circle_color, coordinates, width=10)
    
    def elements_drawing(self) -> None:
        answer = move_checking(self.field)

        for position_x, line in enumerate(self.field):
            for position_y, value in enumerate(line):
                if value is None:
                    continue
                elif value == 1:
                    self.circle_drawing(position_x * self.size, position_y * self.size)
                elif value == -1:
                    self.cross_drawing(position_x * self.size, position_y * self.size)
        
        if answer is None:
            answer = "The game continues"
        elif answer == 0:
            answer = "Draw"
        elif answer == 1:
            answer = "O win!"
        elif answer == -1:
            answer = "X win!"

        text = COMIC_SANS_MS.render(answer, False, self.color_dictionary["Contrast_Color"])
        self.screen.blit(text, text.get_rect(center=(self.point * 2.5, self.point * 0.5)))

    def line_drawing(self) -> None:
        for line in self.lines_array:
            draw.line(self.screen, self.color_dictionary["Contrast_Color"], *line, width=5)

    def change_theme(self) -> None:
        self.color_dictionary = {
            "Back_Ground_Color": self.color_dictionary["Contrast_Color"],
            "Contrast_Color" : self.color_dictionary["Back_Ground_Color"],
            "Other_not_pressed": self.color_dictionary["Now_not_pressed"],
            "Other_pressed": self.color_dictionary["Now_pressed"],
            "Now_not_pressed": self.color_dictionary["Other_not_pressed"],
            "Now_pressed": self.color_dictionary["Other_pressed"]
        }

        self.buttons_dictionary["Clear Field"].inactive_color = self.color_dictionary["Contrast_Color"]
        self.buttons_dictionary["Clear Field"].not_pressed_color = self.color_dictionary["Now_not_pressed"]
        self.buttons_dictionary["Clear Field"].pressed_color = self.color_dictionary["Now_pressed"]
        self.buttons_dictionary["Clear Field"].text_color = self.color_dictionary["Back_Ground_Color"]

        self.buttons_dictionary["Theme"].inactive_color = self.color_dictionary["Contrast_Color"]
        self.buttons_dictionary["Theme"].not_pressed_color = self.color_dictionary["Now_not_pressed"]
        self.buttons_dictionary["Theme"].pressed_color = self.color_dictionary["Now_pressed"]
        self.buttons_dictionary["Theme"].text_color = self.color_dictionary["Back_Ground_Color"]

    def button_drawing(self) -> None:
        if self.buttons_dictionary["Clear Field"].draw_and_check_press() and self.second_clear_timer - self.first_clear_timer >= 250:
            self.first_clear_timer = self.second_clear_timer
            self.field = self.field = [[0] * 3 for _ in range(3)]
        if self.buttons_dictionary["Theme"].draw_and_check_press() and self.second_theme_timer - self.first_theme_timer >= 250:
            self.first_theme_timer = self.second_theme_timer
            self.change_theme()
    
    def game_logic(self) -> None:
        mouse_x, mouse_y = mouse.get_pos()
        mouse_state = mouse.get_pressed()[0]

        for x, y in self.fields_center_coordinates:
            if (x <= mouse_x <= x + self.size) and (y <= mouse_y <= y + self.size) and (mouse_state):
                x, y = x // self.size - 1, y // self.size - 1
                answer = move_checking(self.field)

                if self.field[x][y]:
                    return None
                
                if answer is None:
                    self.field[x][y] = -1
                    self.field = minimum_maximum_algoritm(self.field)
                    break
    
    def pygame_exit_function(self) -> None:
        keys = get_pressed()
        for pygame_event in event.get():
            if pygame_event.type == QUIT or keys[K_ESCAPE]:
                quit()
                exit()


class Button:
    def __init__(self, screen: Surface, x: int, y: int, width: int, height: int, text: str = "",
           inactive_color: tuple[int, int, int] = (90, 90, 90), not_pressed_color: tuple[int, int, int] = (60, 60, 60),
           pressed_color: tuple[int, int, int] = (30, 30, 30), text_color: tuple[int, int, int] = (255, 255, 255),
           border_radius: int = 1) -> None:

        self.screen = screen
        self.rect = Rect(x - width * 0.5, y - height * 0.5, width, height)
        self.x, self.y = x, y
        self.width, self.height = width, height

        self.inactive_color = inactive_color
        self.not_pressed_color = not_pressed_color
        self.pressed_color = pressed_color

        self.text = text
        self.text_color = text_color
        self.border_radius = border_radius


    def draw_and_check_press(self) -> bool:
        flag: bool = False
        mouse_state: bool = mouse.get_pressed()[0]
        mouse_position: tuple[int, int] = mouse.get_pos()
        rendered_text: Surface = COMIC_SANS_MS.render(self.text, False, self.text_color)

        if (self.x - self.width * 0.5 <= mouse_position[0] <= self.x + self.width * 0.5 and
            self.y - self.height * 0.5 <= mouse_position[1] <= self.y + self.height * 0.5):
            if mouse_state:
                draw.rect(self.screen, self.pressed_color, self.rect, border_radius=self.border_radius)
                flag = True
            else:
                draw.rect(self.screen, self.not_pressed_color, self.rect, border_radius=self.border_radius)
        else:
            draw.rect(self.screen, self.inactive_color, self.rect, border_radius=self.border_radius)

        self.screen.blit(rendered_text, rendered_text.get_rect(center=(self.x, self.y)))

        return flag


######################################################################
#                  Made by: @Ice_Lightning_Strike                    #
######################################################################

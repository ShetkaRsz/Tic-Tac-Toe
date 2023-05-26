######################################################################
#                             Libraries                              #
######################################################################


from library_checker import download_libraries
download_libraries()

from pygame import init, display
from pygame.time import Clock

from mechanics import TicTacToe


######################################################################
#                             Variables                              #
######################################################################


init()
display.set_caption("Tic-Tac-Toe")

width, height = display.Info().current_w // 1.5, display.Info().current_h // 1.5
screen = display.set_mode((width, height))
game_field = TicTacToe(screen, display)
clock = Clock()


######################################################################
#                           Game Functions                           #
######################################################################


def main():
    while True:
        clock.tick(60)
        game_field.update()
        game_field.pygame_exit_function()
        display.update()


######################################################################
#                             Starting                               #
######################################################################


if __name__ == '__main__':
    main()


######################################################################
#                  Made by: @Ice_Lightning_Strike                    #
######################################################################
import pygame as pg
from src.enemyType import EnemyType

class Settings:
    """
    Class designed to hold all constants in the game. maybe more?

     Attributes
    ----------
    screen_width : int
        horizontal size of main game screen in pixels
    screen_height : bool
        vertical size of main game screen in pixels
    screen_size : (int, int)
        current state of left arrow key True if pressed
    FPS : int
        number of maximum frames per second
    bg_color: (int, int, int)
        depricated rgb background color
    logo_path: str
        path to logo image
    """

    def __init__(self):
        self.screen_width = 500
        self.screen_height = 500
        self.screen_size = (self.screen_width, self.screen_height)

        self.bg_color = pg.Color('gray')

        # BACKGROUND SPRITE PICTURES
        self.bg_animation = []
        for i in range(0, 49):
            string = 'resources/images/background/bg' + str(i) + '.png'
            self.bg_animation.append(pg.image.load(string))


        self.logo_path = "resources/images/logo_shark.png"
        self.FPS = 60

        # PLAYER SPRITE PICTURES
        self.player_steady = "resources/images/sprite_sheets/player0.png"
        self.player_tailRight = "resources/images/sprite_sheets/player1.png"
        self.player_tailLeft = "resources/images/sprite_sheets/player2.png"

        # ENEMIES
        """(speed, width, height, path_R, path_S, path_L)"""
        red_fish = EnemyType(1, width=48, height=48, path_R="resources/images/enemy2.png", path_S="resources/images/enemy1.png", path_L="resources/images/enemy3.png")
        green_fish = EnemyType(2, width=60, height=60, path_R="resources/images/enemy5.png", path_S="resources/images/enemy4.png", path_L="resources/images/enemy6.png")
        brown_fish = EnemyType(2, width=100, height=100, path_R="resources/images/enemy8.png", path_S="resources/images/enemy7.png", path_L="resources/images/enemy9.png")
        white_fish = EnemyType(1, width=80, height=80, path_R="resources/images/enemy10.png", path_S="resources/images/enemy11.png", path_L="resources/images/enemy12.png")
        blue_fish = EnemyType(1, width=100, height=100, path_R="resources/images/enemy13.png", path_S="resources/images/enemy14.png", path_L="resources/images/enemy15.png")
        purple_fish = EnemyType(2, width=100, height=100, path_R="resources/images/enemy16.png", path_S="resources/images/enemy17.png", path_L="resources/images/enemy18.png")
        self.enemies = [red_fish, green_fish, brown_fish, white_fish, blue_fish, purple_fish]
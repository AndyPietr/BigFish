from enum import Enum
import pygame
from src.state import State

class Player():
    """
    Player object to hold all values describing player fish. Contains also methods to modify player attr.

    Parameters
    ----------
    game : BiggerFish

    Attributes
    ----------
    speed : int
        How fast player moves per tick, (TODO would be nice to base it on time not framerate)
    size : [int, int]
        Actual size of displayed player image in pixels. [width, height]
    sizes : [[int,int], [int,int], [int,int], ...]
        List of all possible sizes player can take.
    screen : pygame.surface
        local copy of main screen used in main game class (DO we really need it)
    screen_rect: pygame.Rect
        rect structure derived from main screen, used in boundary case calculations
    all_sizes_sprites: {int: {str: pygame.Surface, str: pygame.Surface, str: pygame.Surface}... }
       Dict containing all of possible images of player. Calculated in the beginning of the game.
       Data Structure Explained:
           {level_1 : dict_with_sprites, level_2 : dict_with_sprites, level_3 : dict_with_sprites...}
            it is a dictionary of dictionaries. Keys in outer dictionary are integers (so far). While in the inner dicts
            called in here 'dict_with_sprites' we find rescaled sprites.
            Structure of inner dict called in here dict_with_sprites looks like this:
            {'steady': pygame.Surface, 'tailRight': pygame.Surface, 'tailLeft': pygame.Surface}
    sprites : {'steady': pygame.Surface, 'tailRight': pygame.Surface, 'tailLeft': pygame.Surface}
        current set of sprites used to display animations.
    img : pygame.Surface
        current image to blit on screen
    rect : pygame.Rect
        rect corresponding to self.img, used to describe position in bliting
    direction : str
        deprecated, Used in past to represent current state of player
    currentState : State
        instance of imported enum struct, describes current state in which player is
    """


    def __init__(self, game):
        self.speed = 5
        self.size = [48, 48] # [width, height]
        self.sizes = [[48, 48], [60, 60], [100, 100], [120, 120], [140, 140]]
        self.size_level = 0 # initial size level = first element of the sizes list

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect() # creating the rectangle of the whole screen
        self.all_sizes_sprites = self._calculate_surfaces_from_sizes(self.sizes) #unused

        self.change_size(0)  # Used for testing, not needed in here

        # Getting player sprites
        self.sprites={}
        self.sprites['steady'] = pygame.image.load("resources/images/sprite_sheets/tile037.png").convert()
        self.sprites['tailRight'] = pygame.image.load("resources/images/sprite_sheets/tile036.png").convert()
        self.sprites['tailLeft'] = pygame.image.load("resources/images/sprite_sheets/tile038.png").convert()

        # Initial image rescaling
        self.img = self.sprites['steady']
        self.size = [self.sizes[self.size_level][0], self.sizes[self.size_level][1]]
        self.img = pygame.transform.scale(self.img, self.size)
        self.rect = self.img.get_rect()

        # Setting initial position
        self.rect.midbottom = self.screen_rect.midbottom # midbottom point of the screen is set to be equal with  midbnottom point of the player

        self.direction = "stop" # initial movement direction set to "stop"
        self.currentState= State.stop

        self.right = False
        self.left = False

    def update(self):
        """ deprecated
        """
        # if self.direction == "right" and self.rect.right < self.screen_rect.right: # ...and player movement range restriction
        if self.right and not self.left and self.rect.right < self.screen_rect.right: # ...and player movement range restriction
            self.rect.x += self.speed
            self.img = self.sprites["tailLeft"]
            self.img = pygame.transform.scale(self.img, self.size)
        elif self.left and not self.right and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.speed
            self.img = self.sprites["tailRight"]
            self.img = pygame.transform.scale(self.img, self.size)
        else: # to rethink
            # self.rect.x += 0
            self.img = self.sprites["steady"]
            self.img = pygame.transform.scale(self.img, self.size)


    # def update(self, controls_state):
        """ update current player actions attr/flags according to given state

        Parameters
        ----------
        controls_state : State
            desired state in which player would like to be

        """
        """
        if controls_state == State.stop:
            self.img = self.sprites["steady"]
            self.img = pygame.transform.scale(self.img, self.size)
        elif controls_state == State.right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
            self.img = self.sprites["tailLeft"]
            self.img = pygame.transform.scale(self.img, self.size)
        elif controls_state == State.left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.speed
            self.img = self.sprites["tailRight"]
            self.img = pygame.transform.scale(self.img, self.size)
        """

    def blit_player(self):
        """
        Render player img on screen surface
        """
        self.screen.blit(self.img, self.rect)  # blit() method draws the image on top

    def change_size(self, level):
        """
        Modify current sprite set into chosen one.

        Parameters
        ----------
        level : int
            specify which dict of sprites should be used (among all_sizes_sprites)
        """
        """
        self.sprites= self.all_sizes_sprites[level]
        position_tmp_midbottom= self.rect.midbottom
        self.rect= self.sprites["steady"].get_rect()
        self.rect.midbottom= position_tmp_midbottom
        """
        self.size_level = level


    def _calculate_surfaces_from_sizes(self, sizes):
        """ Calculates all surfaces by rescaling to given sizes. Should be executed in the initialization

        Parameters
        ----------
        sizes : [[int, int], [int, int], [int, int]...]

        Returns
        -------
        all_sizes_sprites : {int: {str: pygame.Surface, str: pygame.Surface, str: pygame.Surface}... }
            Dict containing all of possible images sets of player.
        """

        all_sizes_sprites={}
        # TODO those paths should be in one place
        steady= pygame.image.load("resources/images/sprite_sheets/tile037.png").convert()
        tailRight= pygame.image.load("resources/images/sprite_sheets/tile036.png").convert()
        tailLeft= pygame.image.load("resources/images/sprite_sheets/tile038.png").convert()
        for i, size in enumerate(sizes):
            all_sizes_sprites[i]={
                'steady':       pygame.transform.scale(steady,  size),
                'tailRight':    pygame.transform.scale(tailRight,  size),
                'tailLeft':     pygame.transform.scale(tailLeft,  size)
            }
        return all_sizes_sprites

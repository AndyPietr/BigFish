import random
import pygame
from src import settings
from src import player
from src import enemy
from src.state import State
from src.controls import Controls


class BiggerFish:
    def __init__(self):
        pygame.init()
        self.settings = settings.Settings()

        pygame.display.set_caption('Bigger Fish')
        icon = pygame.image.load(self.settings.logo_path)
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode(self.settings.screen_size)  # screen is a tuple of width and height
        self.bg_img = pygame.image.load(self.settings.bg_img_path)
        self.bg_img = pygame.transform.scale(self.bg_img, self.settings.screen_size)

        self.clock = pygame.time.Clock()  # for frames per second/ delay?
        #self.start_time = 0

        # Events ID generator, created to keep track of eventID
        # user event ID has to be between pygame.USEREVENT and pygame.NUMEVENTS
        self.event_id_generator= (id for id in range(pygame.USEREVENT+1, pygame.NUMEVENTS))

        # Counter initialization
        self.counter = self.Counter(self.screen)
        self.counter.addEvent(self.event_id_generator, 100)

        self.enemies = [] # array of enemies
        self.spawn_rate = 2000 # initial spawn rate
        self.SPAWN_EVENT = pygame.USEREVENT # TODO use generator in here 'next( self.event_id_generator)'
        pygame.time.set_timer(self.SPAWN_EVENT, self.spawn_rate)

        self.player = player.Player(self)  # player instance
        self.running = True

        self.controls= Controls()

    def run_game(self):
        while self.running:  # Start of the game's main loop
            self.check_events()  # Event loop
            self.player.update()
            # self.player.update(self.controls.what_fish_should_do())  # Checking the update method in PLAYER each loop.
            for enem in self.enemies: # Can be reduced with sprite.group
                enem.update()
            for enem in self.enemies.copy(): # deleting enemies
                if enem.rect.midbottom[1] >= self.settings.screen_height:
                    self.enemies.remove(enem)
            print(len(self.enemies)) # checking the size of the list
            self.screen_update()  # Updating screen
            self.clock.tick(self.settings.FPS)
            #self.start_time = pygame.time.get_ticks()
            # self.spawn()
            #print(self.controls) # DEBUG

    # def spawn(self):
    #     if self.start_time > self.spawn_rate:
    #         self.enemies.append(enemy.Enemy(self))
    def spawn_enemies(self):
        self.enemies.append(enemy.Enemy(self))  # adding enemies

    def check_events(self):
        for event in pygame.event.get():
            
            # QUIT GAME
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.running = False

            # KEYBOARD INPUT
            elif event.type == pygame.KEYDOWN:  # Check for events when a keypress is done
                if event.key == pygame.K_RIGHT:
                    # self.player.direction = "right"
                    # self.controls.right_down()
                    self.player.right = True
                elif event.key == pygame.K_LEFT:
                    # self.player.direction = "left"
                    # self.controls.left_down()
                    self.player.left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    # self.player.direction = "stop"
                    # self.controls.right_up()
                    self.player.right = False
                elif event.key == pygame.K_LEFT:
                    # self.player.direction = "stop"
                    # self.controls.left_up()
                    self.player.left = False

            elif event.type == self.counter.event:
                # increment counter up to 200
                self.counter.update( (self.counter.points + 1)%200 )

            if event.type == self.SPAWN_EVENT: # TODO change to elif
                self.spawn_enemies()

    def screen_update(self):
        self.screen.fill(self.settings.bg_color)  # Redrawing the background each pass
        self.screen.blit(self.bg_img, [0,0])
        self.player.blit_player()  # drawing our fish on top of our background
        for enem in self.enemies: # Can be reduced with sprite.group
            enem.blit_enemy()

        self.counter.blit(self.screen)

        #self.enemy.blit_enemy()
        # blit enemies in the screen (iterate over self.enemies )
        pygame.display.flip()  # TODO change to update

    class Counter():
        def __init__(self, parentScreen):
            self.screen=parentScreen
            self.points=0
            self.font = pygame.font.SysFont('Comic Sans MS', 30)
            self.font_color= pygame.Color('black')
            self.img= self.font.render(str(self.points), False,  self.font_color, None)
            self.rect = self.img.get_rect()

            self._move_to_bottomright_of(self.screen)

        def addEvent(self, generator, timeBetweenEvents):
            """ add test event to increment counter every x miliseconds
            """
            self.event=next(generator)
            pygame.time.set_timer(self.event, timeBetweenEvents)

        def eventAction(self):
            self.points = ( self.points + 13 + 100) % 100

        def update(self, points):
            self.points = points
            self.img= self.font.render(str(self.points), False,  self.font_color, None)
            self.rect = self.img.get_rect()
            self._move_to_bottomright_of(self.screen)

        def _move_to_bottomright_of(self, screen):
            self.rect.bottomright = self.screen.get_rect().bottomright

        def _move_to_bottomleft_of(self, screen):
            self.rect.bottomleft = self.screen.get_rect().bottomleft

        def blit(self, screen):
            screen.blit(self.img, self.rect)
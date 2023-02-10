# Import and initialize pygame
from random import randint, choice
import pygame
from pygame import mixer
pygame.init()

# Get the clock
clock = pygame.time.Clock()

# Configure the screen
screen = pygame.display.set_mode([500, 500])

lanes = [93, 218, 343]

# points
points = 0

# high score
high_score = 0

# level
level = 1
level_name = ''

def draw_text(text, color, font_size, x, y):
    font = pygame.font.SysFont(None, font_size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# sound effects
boo = pygame.mixer.Sound("boo.wav")
cheer = pygame.mixer.Sound("cheer.wav")

# background music
mixer.init()
mixer.music.load('Denigrate.mp3')
mixer.music.play()

# Make a Game Object class that draws a rectangle.


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(GameObject, self).__init__()
        self.surf = pygame.image.load(image)
        self.x = x
        self.y = y
        #  The get_rect() method returns a Rect object with the dimensions of the Surface.
        self.rect = self.surf.get_rect()
    
    def update_image(self, new_image):
        self.surf = pygame.image.load(new_image)

    def render(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.surf, (self.x, self.y))


# class extends GameObject
# generates random number for x position and always starts a y 0


class Mountain(GameObject):
    def __init__(self):
        super(Mountain, self).__init__(0, 0, 'mountain.png')
        self.dx = 0
        self.dy = (randint(0, 200) / 100) + 1
        self.reset()  # call reset here!

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # Check the y position of the mountain
        if self.y > 500:
            self.reset()

    # add a new method
#  move an mountain back to the top of the screen after moving off the bottom and give it a new random x.
    def reset(self):
        # Here the mountain chooses a random value from the lanes List when it needs an x position.
        self.x = choice(lanes)
        self.y = -64

# instrument moves horizontally rather than veritcally


class Instrument(GameObject):
    def __init__(self):
        super(Instrument, self).__init__(0, 0, 'saxophone.png')
        self.dx = (randint(0, 200) / 100) + 1
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x > 500:
            self.reset()

    def reset(self):
        self.x = -64
        self.y = choice(lanes)


# Make an instance of image
mountain = Mountain()

# instrument
instrument = Instrument()


# Bomb


class Thumbs(GameObject):
    def __init__(self):
        super(Thumbs, self).__init__(0, 0, 'thumbs.png')
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x > 500 or self.x < -64 or self.y > 500 or self.y < -64:
            self.reset()

    def reset(self):
        direction = randint(1, 4)
        if direction == 1:  # left
            self.x = -64
            self.y = choice(lanes)
            self.dx = (randint(0, 200) / 100) + 1
            self.dy = 0
        elif direction == 2:  # right
            self.x = 500
            self.y = choice(lanes)
            self.dx = ((randint(0, 200) / 100) + 1) * -1
            self.dy = 0
        elif direction == 3:  # down
            self.x = choice(lanes)
            self.y = -64
            self.dx = 0
            self.dy = (randint(0, 200) / 100) + 1
        else:
            self.x = choice(lanes)
            self.y = 500
            self.dx = 0
            self.dy = ((randint(0, 200) / 100) + 1) * -1


thumbs = Thumbs()


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__(0, 0, 'colton.png')
        self.dx = 0
        self.dy = 0
        self.pos_x = 1
        self.pos_y = 1
        self.reset() 

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
        self.update_dx_dy()

    def right(self):
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
        self.update_dx_dy()

    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
        self.update_dx_dy()

    def down(self):
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
        self.update_dx_dy()

    def move(self):
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25

    def reset(self):
        self.x = lanes[self.pos_x]
        self.y = lanes[self.pos_y]
        self.dx = self.x
        self.dy = self.y

    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]



# make an instance of Player
player = Player()

# Group is a class that manages a collection of Sprites.
# Make a group
all_sprites = pygame.sprite.Group()

# Add sprites to group
all_sprites.add(player)
all_sprites.add(mountain)
all_sprites.add(instrument)
all_sprites.add(thumbs)

# make a Group
iatm_sprites = pygame.sprite.Group()

iatm_sprites.add(mountain)
iatm_sprites.add(instrument)

# Creat the game loop
running = True
while running:
    # Looks at events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Check for event type KEYBOARD
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()

# Clear screen
    screen.fill((219, 156, 217))
# Move and render Sprites
    for entity in all_sprites:
        entity.move()
        entity.render(screen)
# Check Colisions
# This method returns a sprite from the group that has collided with the test sprite.
    iatm = pygame.sprite.spritecollideany(player, iatm_sprites)
    if iatm:
        points += 1
        pygame.mixer.Sound.play(cheer)
        iatm.reset()
    # Check collision player and bomb
    if pygame.sprite.collide_rect(player, thumbs):
        if points > high_score:
          high_score = points
        points = 0
        pygame.mixer.Sound.play(boo)
        thumbs.reset()
    if points <= 20:
        player.update_image('colton.png')
        instrument.update_image('saxophone.png')
        level = 1
        level_name = 'Colton'
    if points > 20:
        player.update_image('keath.png')
        instrument.update_image('trumpet.png')
        level = 2
        level_name = 'Keath'
    if points > 40:
        player.update_image('rob.png')
        instrument.update_image('drums.png')
        level = 3
        level_name = 'Rob'
    if points > 60:
        player.update_image('jesse.png')
        instrument.update_image('bass.png')
        level = 4
        level_name = 'Jesse'
    if points > 80:
        player.update_image('dylan.png')
        instrument.update_image('trombone.png')
        level = 5
        level_name = 'Dylan'
    if points > 100:
        player.update_image('jay.png')
        instrument.update_image('guitar.png')
        level = 6
        level_name = 'Jay'
     # Draw the points
    draw_text(text=f'Points: {points}', color=(6, 13, 51), font_size=24, x=20, y=50)
    # draw high score
    draw_text(text=f'High Score: {high_score}', color= (6, 13, 51), font_size=24, x=370, y=20)
    # draw levels
    draw_text(text=f'Level {level}: {level_name}',
              color=(6, 13, 51), font_size=24, x=20, y=20)
# Update the window
    pygame.display.flip()
    # tick the clock!
    # saying the next update should be applied in 1/30th of a second.
    clock.tick(60)

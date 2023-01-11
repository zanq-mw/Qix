import pygame
import random
import pygame.gfxdraw
from pygame.locals import *
from pygame.math import Vector2

class Push(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface((10,10))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def hit(self, push, enemy,player):
        # Player dead
        if player.health == 0:
            global game_start
            game_start=True

        # Check Hit
        global x
        global y
        global polygon_outline
        global hit
        global push_sprite
        global pushing
        if not (type(enemy)==Qix and not inside(x, y)):
            if pygame.sprite.collide_rect(push, enemy) and player.immunity == 0:
                player.health -= 1
                player.immunity = 60
                polygon_outline=[]
                x = firstx
                player.rect.x = x
                y = firsty
                player.rect.y = y
                hit = True
                push_sprite.remove(push)
                pushing = False
            elif player.immunity != 0:
                player.immunity -= 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((player_size, player_size))
        self.image.fill(PLAYER)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.health = 3
        self.immunity = 0

    def update(self):
        if direction == "L":
            self.rect.x -= vel
        elif direction == "R":
            self.rect.x += vel
        elif direction == "U":
            self.rect.y -= vel
        elif direction == "D":
            self.rect.y += vel

    def hit(self, player, enemy):
        # Player dead
        if self.health == 0:
            global game_start
            game_start=True

        # Check Hit
        global x
        global y
        global polygon_outline
        global hit
        global push_sprite
        global pushing
        if not (type(enemy)==Qix and not inside(x, y)):
            if pygame.sprite.collide_rect(player, enemy) and self.immunity == 0:
                self.health -= 1
                self.immunity = 60
                if inside(x, y) and type(enemy)==Qix:
                    for push in push_sprite:
                        push_sprite.remove(push)
                    polygon_outline=[]
                    x = firstx
                    player.rect.x = x
                    y = firsty
                    player.rect.y = y
                    hit = True
                    pushing = False
            elif self.immunity != 0:
                self.immunity -= 1


class Qix(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((130, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (12, 5)

    def update(self):
        global movex
        global movey

        if self.rect.left < 12:
            rand = random.randint(0, 3)
            self.rect.x += 3
            self.rect.y += rand
            movex = 3
            movey = rand
        if self.rect.right > screen_size - 13:
            rand = random.randint(-3, 3)
            self.rect.x += -3
            self.rect.y += rand
            movex = -3
            movey = rand
        if self.rect.top < 5:
            rand = random.randint(-3, 3)
            self.rect.x += rand
            self.rect.y += 3
            movex = rand
            movey = 3
        if self.rect.bottom > screen_size - 6:
            rand = random.randint(-3, 3)
            self.rect.x += rand
            self.rect.y += -3
            movex = rand
            movey = -3

        else:
            self.rect.x += movex
            self.rect.y += movey


class Boundary(pygame.sprite.Sprite):
    def __init__(self, l, w, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((l, w))
        self.image.fill(SPARC)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Sparc(pygame.sprite.Sprite):
    def __init__(self, pos=(100, 100), points=[(0, 0), (100, 100)]):
        super().__init__()
        # Position/Velocity
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)

        # Sprite
        self.image = pygame.Surface([11, 11])
        self.image.fill(SPARC)
        self.rect = self.image.get_rect(center=self.pos)

        # Border Path
        self.points = points
        self.currentpoint = 0
        self.target = self.points[self.currentpoint]


    def update(self):
        # Original Movement
        dir = self.target - self.pos
        dist = dir.length()
        dir.normalize_ip()

        if dist <= 1:
            self.currentpoint = (self.currentpoint + 1) % len(self.points)
            self.target = self.points[self.currentpoint]
        else:
            self.vel = dir

        self.pos += self.vel * 2
        self.rect.center = self.pos



# Colours
BLACK = (0, 0, 0)
WHITE = (200, 210, 210)
SPARC = (200, 0, 200)
BORDER = (0, 225, 0)
PLAYER = (255, 56, 0)
QIX = (225, 225, 0)
TEXT = (24, 129, 161)

pygame.init()
screen_size = 500
win = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Qix")

movex = 3
movey = 3
player_size = 11
vel = 15
hit=False
x = (500 - vel - player_size) / 2
lastx = x
firstx = None
y = 500 - vel
firsty = None
player = Player()
qix = Qix()
push_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
qix_sprite = pygame.sprite.Group()
all_sprites.add(player)
qix_sprite.add(qix)
lasty = y
direction = None
lastdirection = None
firstdirection = None
polygon_outline = []
polygons = []
percent = 0

pushing = False

# Health
font = pygame.font.Font('freesansbold.ttf', 20)
health_txt = font.render("Health:" + str(player.health), True, TEXT)
health_rect = health_txt.get_rect()

# Percent Covered
percent_txt = font.render("Covered:" + str(percent), True, TEXT)
percent_rect = percent_txt.get_rect()

vectors = [(player_size + 1, player_size), (player_size + 1, screen_size - player_size),
           (screen_size - player_size, screen_size - player_size), (screen_size - player_size, player_size)]
sparc_sprite = pygame.sprite.Group(Sparc((player_size + 1, 6), vectors))
rev_vectors = [(screen_size - player_size, player_size),(screen_size - player_size, screen_size - player_size),
(player_size + 1, screen_size - player_size),(player_size + 1, player_size)]

sparc_sprite.add(Sparc((player_size + 1, 6), rev_vectors))


run = True
game_start=True
clock = pygame.time.Clock()


def inside(x, y):
    return (x < screen_size - vel - player_size and x > vel and y < screen_size - player_size - vel and y > vel)


def getCorners(dir):
    if dir == "U" or dir == "D":
        ldist = x + firstx
        rdist = 2 * (screen_size) - x - firstx
        if ldist >= rdist:
            x_cord = screen_size - (player_size + 1)
        else:
            x_cord = player_size + 1
        if dir == "U":
            polygon_outline.append((x_cord, 5))
            polygon_outline.append((x_cord, screen_size - 5))
        else:
            polygon_outline.append((x_cord, screen_size - 5))
            polygon_outline.append((x_cord, 5))
    elif dir == "R" or dir == "L":
        tdist = y + firsty
        bdist = 2 * screen_size - y - firsty
        if tdist >= bdist:
            y_cord = screen_size - 5
        else:
            y_cord = 5
        if dir == "R":
            polygon_outline.append((screen_size - (player_size + 1), y_cord))
            polygon_outline.append((player_size + 1, y_cord))
        else:
            polygon_outline.append((player_size + 1, y_cord))
            polygon_outline.append((screen_size - (player_size + 1), y_cord))


def get_percent(polygons):
    total = 490 * 490
    area = 0
    for shape in polygons:

        psum = 0
        nsum = 0
        for i in range(len(shape)):
            sindex = (i + 1) % len(shape)
            sum = shape[i][0] * shape[sindex][1]
            psum += sum

        for i in range(len(shape)):
            sindex = (i + 1) % len(shape)
            sum = shape[sindex][0] * shape[i][1]
            nsum += sum

        area += abs(1 / 2 * (psum - nsum))
    return int((area / total) * 100)

def show_start_screen():
    win.fill(BLACK)
    font = pygame.font.SysFont("Arial", 64)
    font2 = pygame.font.SysFont("Arial", 22)
    font3 = pygame.font.SysFont("Arial", 18)
    if percent>=65:
        text = font.render("YOU WIN", True, (255, 255, 255))
        text2 = font2.render("You reached the goal of covering 65%", True, (255, 255, 255))
        text3 = font3.render("Press ENTER to play again", True, (255, 255, 255))
    elif player.health <= 0:
        text = font.render("YOU LOSE", True, (255, 255, 255))
        text2 = font2.render("You lost all your health", True, (255, 255, 255))
        text3 = font3.render("Press ENTER to play again", True, (255, 255, 255))
    else:
        text=font.render("QIX", True, (255, 255, 255))
        text2 = font2.render("Arrow keys to move, space with an arrow key to push inside", True, (255, 255, 255))
        text3 = font3.render("Press ENTER to begin", True, (255, 255, 255))
    win.blit(text, (screen_size/2-text.get_rect().width/2, screen_size/4))
    win.blit(text2, (screen_size / 2 - text2.get_rect().width / 2, screen_size / 2))
    win.blit(text3, (screen_size / 2 - text3.get_rect().width / 2, screen_size * 3/4))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    waiting=False



while run:
    if game_start:
        show_start_screen()
        game_start=False
        hit=False
        player_size = 11
        vel = 15
        x = (500 - vel - player_size) / 2
        lastx = x
        firstx = x
        y = 500 - vel
        firsty = y
        player = Player()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        lasty = y
        direction = None
        lastdirection = None
        firstdirection = None
        polygon_outline = []
        polygons = []
        percent = 0
        vectors = [(player_size + 1, player_size), (player_size + 1, screen_size - player_size),
                   (screen_size - player_size, screen_size - player_size), (screen_size - player_size, player_size)]
        sparc_sprite = pygame.sprite.Group(Sparc((player_size + 1, 6), vectors))
        rev_vectors = [(player_size + 1, player_size), (player_size + 1, screen_size - player_size),
                       (screen_size - player_size, screen_size - player_size), (screen_size - player_size, player_size)]
        rev_vectors.reverse()
        sparc_sprite.add(Sparc((player_size + 1, 6), rev_vectors))

    if percent>=65:
        game_start=True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[
        pygame.K_LEFT] and (keys[pygame.K_SPACE] or (
            (x < screen_size - vel - player_size and (not inside(x, y) or lastdirection != "R")) or (
            y <= vel or y >= screen_size - player_size - vel))) and x > vel:  # Making sure the top left position of our character is greater than our vel so we never move off the screen.
        x -= vel
        direction = "L"
        all_sprites.update()

    elif keys[
        pygame.K_RIGHT] and (keys[pygame.K_SPACE] or ((x > vel and (not inside(x, y) or lastdirection != "L")) or (
            y <= vel or y >= screen_size - player_size - vel))) and x < screen_size - vel - player_size:  # Making sure the top right corner of our character is less than the screen player_size - its player_size
        x += vel
        direction = "R"
        all_sprites.update()

    elif keys[pygame.K_UP] and (keys[pygame.K_SPACE] or (
            (y < screen_size - player_size - vel and (not inside(x, y) or lastdirection != "D")) or (
            x <= vel or x >= screen_size - vel - player_size))) and y > vel:  # Same principles apply for the y coordinate
        y -= vel
        direction = "U"
        all_sprites.update()

    elif keys[pygame.K_DOWN] and (keys[pygame.K_SPACE] or (
            (y > vel and (not inside(x, y) or lastdirection != "U")) or (
            x <= vel or x >= screen_size - vel - player_size))) and y < screen_size - player_size - vel:
        y += vel
        direction = "D"
        all_sprites.update()

    if inside(x, y):
        if not pushing:
            pushing = True
            push_sprite.add(Push((int(lastx + player_size/2),int(lasty + player_size/2))))

        if inside(lastx, lasty) and lastdirection != direction:
            polygon_outline.append((lastx + (player_size / 2), lasty + (player_size / 2)))
        if not inside(lastx, lasty):
            firstdirection = direction
            firstx = lastx
            firsty = lasty
        if direction == "U":
            if not inside(lastx, lasty):
                polygon_outline.append((lastx + (player_size / 2), lasty + player_size))
            polygon_outline.append((x + (player_size / 2), y + player_size))
        elif direction == "D":
            if not inside(lastx, lasty):
                polygon_outline.append((lastx + (player_size / 2), lasty))
            polygon_outline.append((x + (player_size / 2), y))
        elif direction == "R":
            if not inside(lastx, lasty):
                polygon_outline.append((lastx, lasty + (player_size / 2)))
            polygon_outline.append((x, y + (player_size / 2)))
        elif direction == "L":
            if not inside(lastx, lasty):
                polygon_outline.append((lastx + player_size, lasty + (player_size / 2)))
            polygon_outline.append((x + player_size, y + (player_size / 2)))

    else:
        if inside(lastx, lasty) and hit==False:
            pushing = False
            for push in push_sprite:
                push_sprite.remove(push)
            if direction == "U":
                polygon_outline.append((lastx + (player_size / 2), lasty + (player_size / 2)))
                polygon_outline.append((x + (player_size / 2), y))
            elif direction == "D":
                polygon_outline.append((lastx + (player_size / 2), lasty + (player_size / 2)))
                polygon_outline.append((x + (player_size / 2), y + player_size))
            elif direction == "R":
                polygon_outline.append((lastx + (player_size / 2), lasty + (player_size / 2)))
                polygon_outline.append((x + player_size, y + (player_size / 2)))
            elif direction == "L":
                polygon_outline.append((lastx + (player_size / 2), lasty + (player_size / 2)))
                polygon_outline.append((x, y + (player_size / 2)))
            if (firstdirection == "U" or firstdirection == "D") and (direction == "R" or direction == "L"):
                polygon_outline.append((polygon_outline[-1][0], polygon_outline[0][1]))
            elif (firstdirection == "L" or firstdirection == "R") and (direction == "U" or direction == "D"):
                polygon_outline.append((polygon_outline[0][0], polygon_outline[-1][1]))
            elif direction == firstdirection:
                getCorners(direction)

        if hit==True:
            hit=False

        if len(polygon_outline) > 2:
            polygons.append(polygon_outline)
        polygon_outline = []
        firstdirection = None


    lastx = x
    lasty = y
    lastdirection = direction

    # Update Percent Text
    percent = get_percent(polygons)
    percent_txt = font.render("Covered: %" + str(percent), True, TEXT)

    # Update Health Text
    health_txt = font.render("Health:" + str(player.health), True, TEXT)

    for sparc in sparc_sprite:
        for push in push_sprite:
            push.hit(push,sparc,player)
        player.hit(player, sparc)
        sparc.update()
    player.hit(player, qix)
    sparc.update()

    win.fill(BLACK)

    # draw polygons
    for shape in polygons:
        pygame.draw.polygon(win, (64, 224, 208), shape)

    # draw player
    pygame.draw.rect(win, PLAYER, (x, y, player_size, player_size))
    # draw borders
    pygame.draw.rect(win, BORDER, (0, 0, player_size + 1, screen_size))
    pygame.draw.rect(win, BORDER, (screen_size - player_size - 1, 0, player_size + 1, screen_size))
    pygame.draw.rect(win, BORDER, (0, 0, screen_size, 5))
    pygame.draw.rect(win, BORDER, (0, screen_size - 5, screen_size, 5))

    # draw Sparcs
    sparc_sprite.draw(win)
    qix_sprite.draw(win)
    qix_sprite.update()

    # Draw Outline
    for cord in polygon_outline:
        pygame.draw.rect(win, PLAYER, (cord[0], cord[1], 1, 1))

    # Draw text
    win.blit(health_txt, (0, 5))
    win.blit(percent_txt, (0, 20))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
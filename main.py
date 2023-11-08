# Alexander Mortillite SolarSystemV3
# 10/3/2023

import pygame
import random

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1820, 1020
BACKGROUND_COLOR = (0, 0, 0)
center = (WIDTH / 2, HEIGHT / 2)

screen = pygame.display.set_mode([WIDTH, HEIGHT])

yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

initalMomentum = 10
initalMomentumMars = 9
planetMass = 900
marsMass = 300
starMass = 15000
G = -.01

marsStart = (WIDTH / 2 + 300, HEIGHT / 2)
startPos = (WIDTH / 2 + 700, HEIGHT / 2)
planetList = []

ZOOM_FACTOR = 1.2  # Adjust this value for zoom speed
MIN_ZOOM = 0.5
MAX_ZOOM = 2.0
zoom = 1.0
zoom_center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
# S

counter = 0
frameRemoverCount = 0


class SolarBody:
    def __init__(self, mass, radius, pos, acc, momentum, color, isIntert):
        self.mass = mass
        self.radius = radius
        self.pos = pygame.Vector2(pos)
        self.acc = pygame.Vector2(acc)
        self.momentum = pygame.Vector2(momentum)
        self.color = color
        self.force = (0, 0)
        self.pos_history = [pygame.Vector2(pos)]
        self.isInert = isIntert

    def update(self):
        self.momentum += self.force
        self.pos += self.momentum


class Settings:
    def __init__(self, paused, frames, scale):
        self.paused = paused
        self.frames = frames
        self.scale = scale


def gforce(p1, p2):
    r_vec = pygame.math.Vector2(p1.pos - p2.pos)
    r_mag = r_vec.magnitude()
    r_hat = r_vec / r_mag
    force_mag = G * p1.mass * p2.mass / r_mag ** 2
    force_vec = pygame.math.Vector2(force_mag * r_hat)
    return force_vec


def gravity():
    for x in planetList:
        x.force = pygame.math.Vector2()
        for y in planetList:
            if x != y:
                x.force += gforce(x, y)


def didCollide(p1, p2):
    if p1 != p2:
        r_vec = pygame.math.Vector2(p1.pos - p2.pos)
        r_mag = r_vec.magnitude()
        if r_mag - (p1.radius) - (p2.radius) <= 0:
            print(r_mag - (p1.radius) - (p2.radius))
            return True
        return False


def collisions():
    for x in planetList:
        for y in planetList:
            if x != y and didCollide(x, y):
                # if (x.isInert or y.isInert) != True:
                x.mass += y.mass
                x.radius += y.radius
                x.momentum += y.momentum
                planetList.remove(y)
                print("Collision")


def update():
    for x in planetList:
        if x.isInert == False:
            x.update()


def update_fps(font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def elapsed_frames(eFrames, font):
    ef = str(int(eFrames))
    ef_text = font.render(ef, 1, pygame.Color("coral"))
    return ef_text


def solarTrajectory():
    for x in planetList:
        x.pos_history.append(pygame.Vector2(x.pos.x, x.pos.y))
    for x in planetList:
        pygame.draw.lines(screen, x.color, False, x.pos_history)


def view():
    solarTrajectory()
    for x in planetList:
        pygame.draw.circle(screen, x.color, x.pos * settings.scale, x.radius)


def uiElements():
    eFrames = 1  # Elapsed Frames, Going to move this out
    font = pygame.font.SysFont("Arial", 18)
    clock.tick(settings.frames)
    screen.fill((0, 0, 0))
    eFrames += clock.get_fps()
    screen.blit(update_fps(font), (10, 0))
    screen.blit(elapsed_frames(eFrames, font), (10, 20))


def pan(offSetx, offSety):
    for x in planetList:
        x.pos.x += offSetx
        x.pos.y += offSety
        for y in x.pos_history:
            y.x += offSetx
            y.y += offSety


def scaler():
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            print("Zoom")
            settings.scale += 0.1
            settings.scale = round(settings.scale, 1)
            if settings.scale > 2:
                settings.scale = 2
        if event.button == 3:
            print("unZoom")
            settings.scale -= 0.1
            scale = round(settings.scale, 1)
            if scale < 0.5:
                scale = 0.5
                print(scale)


def garbage():
    for x in planetList:
        if len(x.pos_history) > 5000:
            x.pos_history.remove(x.pos_history[0])


def userControls():
    panOffset = 3
    keys = pygame.key.get_pressed()
    # Pan the player
    if keys[pygame.K_LEFT]:
        pan(panOffset, 0)
    if keys[pygame.K_RIGHT]:
        pan(-panOffset, 0)
    if keys[pygame.K_UP]:
        pan(0, panOffset)
    if keys[pygame.K_DOWN]:
        pan(0, -panOffset)
    if keys[pygame.K_BACKSPACE]:
        pygame.Vector2(planetList[0].pos)
    if keys[pygame.K_p]:
        settings.paused = not settings.paused
        pygame.time.delay(200)


def initDemo():
    star = SolarBody(starMass, 40, center, (0, 0), (0, 0), yellow, True)
    mars = SolarBody(marsMass, 20, marsStart, (0, 0), (0, random.randint(1, 15)), (255, 0, 0), False)
    planet = SolarBody(planetMass, 12, startPos, (0, 0), (0, random.randint(1, 15)), (0, 255, 0), False)
    planetList = [star, mars, planet]
    return planetList


def collisionDemo():
    star = SolarBody(starMass, 40, center, (0, 0), (0, 0), yellow, True)
    mars = SolarBody(marsMass, 20, marsStart, (0, 0), (0, 0), (255, 0, 0), False)
    planet = SolarBody(planetMass, 12, startPos, (0, 0), (-30, 0), (0, 255, 0), False)
    planetList = [star, mars, planet]
    return planetList


def warpDemo():
    star = SolarBody(starMass, 40, center, (0, 0), (0, 0), yellow, True)
    planet = SolarBody(planetMass, 12, startPos, (0, 0), (-50, 0), (0, 255, 0), False)
    planetList = [star, planet]
    return planetList


settings = Settings(False, 60, 1)

planetList = initDemo()
# planetList = collisionDemo()
# planetList = warpDemo()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    userControls()
    # scaler()
    uiElements()
    if settings.paused:
        gravity()
        update()
        collisions()
    view()
    garbage()

    pygame.display.flip()
pygame.quit()

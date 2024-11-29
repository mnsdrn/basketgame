import pygame
import pymunk
import pymunk.pygame_util
import math
from pygame.draw import *


pygame.init()

WIDTH, HEIGHT = 800, 600  #создание окна и звука
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.music.load('bsound.mp3')
pygame.mixer.music.play()


def calculate_distance(p1, p2): #дистанция между 2 точками
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calculate_angle(p1, p2): #рассчет угла
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw(space, window, draw_options, line, text1): #рисование задника
    window.fill("white")
    rect(window, (128, 160, 255), (0, 350, 800, 250))
    '''cиняя стена'''
    rect(window, (255, 160, 128), (0, 0, 300, 300))
    rect(window, (128, 255, 255), (0, 25, 275, 150))
    rect(window, (152, 255, 152), (0, 175, 275, 100))
    rect(window, (128, 255, 255), (0, 175, 10, 10))
    rect(window, (128, 255, 255), (65, 175, 10, 10))
    rect(window, (128, 255, 255), (75, 175, 20, 75))
    rect(window, (128, 255, 255), (95, 175, 50, 30))
    rect(window, (128, 255, 255), (190, 175, 50, 50))
    rect(window, (255, 255, 255), (185, 70, 50, 30))
    rect(window, (255, 255, 255), (160, 85, 50, 30))
    rect(window, (255, 255, 255), (210, 90, 50, 30))
    '''окно'''
    rect(window, (255, 160, 128), (400, 175, 20, 425))
    rect(window, (255, 160, 128), (600, 175, 20, 425))
    rect(window, (255, 160, 128), (420, 200, 200, 15))
    rect(window, (255, 160, 128), (420, 250, 200, 15))
    rect(window, (255, 160, 128), (420, 300, 200, 15))
    rect(window, (255, 160, 128), (420, 350, 200, 15))
    rect(window, (255, 160, 128), (420, 400, 200, 15))
    rect(window, (255, 160, 128), (420, 450, 200, 15))
    rect(window, (255, 160, 128), (420, 500, 200, 15))
    rect(window, (255, 160, 128), (420, 550, 200, 15))
    '''шведская стеннка'''
    rect(window, (255, 255, 152), (20, 550, 500, 20))
    rect(window, (255, 255, 152), (75, 560, 20, 40))
    rect(window, (255, 255, 152), (445, 560, 20, 40))

    font = pygame.font.Font('freesansbold.ttf', 32) #счетчик
    text = font.render('Score:' + str(text1), True, 'black', 'white')
    textRect = text.get_rect()
    textRect.center = (800 // 2, 50)
    window.blit(text, textRect)

    if line: #линия броска
        pygame.draw.line(window, "orange", line[0], line[1], 3)

    space.debug_draw(draw_options) 
    pygame.display.update()


def create_boundaries(space): #кольцо и стенки физические объекты
    segment1_shape = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5)
    segment1_shape.elasticity = 0.8
    segment1_shape.friction = 0.5
    space.add(segment1_shape)
    segment2_shape = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5)
    segment2_shape.elasticity = 0.8
    segment2_shape.friction = 0.5
    space.add(segment2_shape)
    segment3_shape = pymunk.Segment(space.static_body, (700, 150), (700, 250), 5)
    segment3_shape.elasticity = 1
    segment3_shape.friction = 0.5
    space.add(segment3_shape)
    segment4_shape = pymunk.Segment(space.static_body, (700, 250), (800, 250), 5)
    segment4_shape.elasticity = 0.1
    segment4_shape.friction = 0.5
    space.add(segment4_shape)


basket = pygame.Rect(700, 200, 150, 75) #границы для засчета очков


def create_ball(space, radius, mass, pos): #создание мяча
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 153, 0, 255)
    space.add(body, shape)
    return shape


def run(window, width, height): #запуск игры
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)
    score = 0

    create_boundaries(space)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    pressed_pos = None
    ball = None

    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space, window, draw_options, line, score)
        space.step(dt)
        if ball: #счетчик
            if basket.collidepoint(ball.body.position):
                score += 1
                pygame.time.wait(1000)
                space.remove(ball, ball.body)
                ball = None
        clock.tick(fps)
    pygame.quit()
    print(score)


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)


from pygame import *
import math
init()
t_sound = mixer.Sound("t.ogg")
t_sound.set_volume(0.5)

class GameSprite(sprite.Sprite):
    def __init__(self, image1, x, y, speed, width, height):
        super().__init__()

        self.image = transform.scale(image.load(image1), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

back = (200, 255, 255)
win_width = 700
win_height = 500
win = display.set_mode((win_width, win_height))
win.fill(back)

score_1 = 0
score_2 = 0

game = True
finish = False
background = transform.scale(image.load("bk.jfif"), (win_width, win_height))
f = font.Font(None, 36)
clock = time.Clock()
FPS = 60

racket1 = Player("player1.png", 1, win_width - 500, 10, 100, 100)
racket2 = Player("player2.png", 600, win_width - 500, 10, 100, 100)

ball = GameSprite("ball.png", 300, win_height - 500, 250, 50, 50)

font = font.Font(None, 35)
lose1 = font.render("PLAYER 1 LOSE!", True, (180, 0, 0))
lose2 = font.render("PLAYER 2 LOSE!", True, (180, 0, 0))

speed = 5
speedxy = [0, 0]
ang = 15
speedxy[0] = math.cos(math.radians(ang)) * speed
speedxy[1] = math.sin(math.radians(ang)) * speed


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        win.fill(back)
        win.blit(background, (0,0))
        racket1.update_l()
        racket2.update_r()
        text_score_1 = f.render(f"Рахунок першого гравця: {score_1}", True, (0, 158, 78))
        win.blit(text_score_1, (10,20))

        text_score_2 = f.render(f"Рахунок другого гравця: {score_2}", True, (0, 158, 78))
        win.blit(text_score_2, (10,60))

        ball.rect.x += speedxy[0]
        ball.rect.y += speedxy[1]

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            t_sound.play()
            speedxy[0] *= -1

        if ball.rect.y > win_height - 50 or  ball.rect.y < 0:
            speedxy[1] *= -1

        if ball.rect.x < 0:
            score_2 += 1
            ball.rect.x = 250
            ball.rect.y = 250
            win.blit(lose1, (200, 100))

        if ball.rect.x > win_width:
            score_1 += 1
            ball.rect.x = 250
            ball.rect.y = 250
            win.blit(lose2, (200, 100))

        racket1.reset()
        racket2.reset()
        ball.reset()


        if score_1 >= 5:
            finish = True
            won_1 = f.render("FIRST PLAYER WIN!!!!!!!", True, (0, 0, 255))
            win.blit(won_1, (200, 200))

        if score_2 >= 5:
            finish = True
            won_2 = f.render("SECOND PLAYER WIN!!!!!!", True, (0, 0, 255))
            win.blit(won_2, (200, 200))

    display.update()
    clock.tick(FPS)
import pygame
import random
import com
from config import SCREEN_WIDTH, SCREEN_HEIGHT,FPS, BACK_COLOR
from config import RACKET_COLOR, RACKET_HEIGHT, RACKET_SPEED, RACKET_WIDTH
from config import BALL_COLOR, BALL_RADIUS, BALL_SPEED
from config import FONT_COLOR
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('game')
    clock = pygame.time.Clock()#fpsのコントロール用
    font = pygame.font.SysFont(None, 36)

    # 初期設定
    racket = Racket()
    ball = Ball()

    # aruduinoと接続
    com.init_serial()

    lives = 3
    running = True
    pause = False
    while running:
        screen.fill(BACK_COLOR)#全面塗りつぶし

        #ウィンドウのx押下で終了
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #キーボード入力
        input_data = {"direction" : None, "start": False}
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            input_data["direction"] = 'left'
        if key[pygame.K_RIGHT]:
            input_data["direction"] = 'right'
        if key[pygame.K_q]:
            running = False
        if key[pygame.K_p]:
            pause = True
        if key[pygame.K_s]:
            pause = False
        
        if not pause and lives > 0:
            if input_data["direction"] == 'left':
                racket.move_left()
            elif input_data['direction'] == 'right':
                racket.move_right()
            miss = ball.update(racket)
            racket.update()

        joy, a, b = com.read_contller()
        if not pause and lives > 0:
            if joy == 0:
                racket.move_left()
            elif joy == 2:
                racket.move_right()
            miss = ball.update(racket)
            racket.update()
        
        if a == 0:
            pause = True
        if b == 0:
            pause = False
            
        racket.draw(screen)
        ball.draw(screen)

        lives_text = font.render(f'lives : {lives}', True, FONT_COLOR)
        screen.blit(lives_text, (10, 10))
        if pause:
            pause_text = font.render('PAUSE', True, FONT_COLOR)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
        if miss:
            lives -= 1
            if lives < 1:
                screen.fill(BACK_COLOR)#全面塗りつぶし
                gemeover_text = font.render('Game Over!', True, FONT_COLOR)
                screen.blit(gemeover_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))

        live_view(lives)
        pygame.display.flip()
        clock.tick(FPS)#1秒間にFPS回の更新
    pygame.quit()
    com.serial_close()
def live_view(lives):
    if lives == 0:
        com.LED_0()
    elif lives == 1:
        com.LED_1()
    elif lives == 2:
        com.LED_2()
    elif lives == 3:
        com.LED_3()
    
    
class Racket:
    def __init__(self):
        self.width = RACKET_WIDTH
        self.height = RACKET_HEIGHT
        self.color = RACKET_COLOR
        #初期位置
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT * 4 // 5
        self.vx = 0 #差分

    def move_left(self):
        self.vx = -RACKET_SPEED
    def move_right(self):
        self.vx = RACKET_SPEED
    
    def update(self):
        self.x = self.x + self.vx
        #ウィンドウから飛び出ないようにする
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        self.vx = 0#フレームごとに速度をリセットする
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.reset()
    def reset(self):
        self.x = random.choice([1,2,3,4,5,6]) * SCREEN_WIDTH // 7
        self.y = SCREEN_HEIGHT // 3
        self.vx = BALL_SPEED * random.choice([1, -1])
        self.vy = BALL_SPEED * random.choice([1, -1])
    def update(self, racket):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vx *= -1
        if self.y - self.radius <= 0:
            self.vy *= -1
        if (racket.y <= self.y + self.radius <= racket.y + racket.height and
                racket.x <= self.x <= racket.x + racket.width and self.vy > 0):
            self.vy *= -1
        if self.y -self.radius > SCREEN_HEIGHT:
            self.reset()
            return True
        return False    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

if __name__ == '__main__':
    main()
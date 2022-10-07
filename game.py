from pickle import FALSE, HIGHEST_PROTOCOL

import sys
from tkinter import Canvas
from turtle import color
import pygame
import random
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pygame.locals import *
 
# 화면의 크기를 지정하는 변수
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800

# RGB 코드를 이용해서 사전에 색상들을 선언해둔다.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 깜빡이는 효과를 표현하기 위해서 색이 진해졌다 밝아졌다를 반복한다.
BLINK = [(255, 255, 255), (255, 255, 192), (255, 255, 128), (255, 224, 64), (255, 255, 128), (255, 255, 192)]

# 배경 도로의 움직임을 표현하기 위한 변수

bg_y = 0
 
background = pygame.image.load("background.png")

# 리소스(이미지, 사운드) 폴더 경로

DIROBJECTS = "OBJECTS/"
DIRSOUND = "sound/"
DIRBG = "bg/"


# 게임 진행, 초기화, 종료에 사용되는 변수들

STAGE = 1
obj_COUNT = 5
SCORE = 0
STAGESCORE = 0
STAGESTAIR = 1000
idx = 0  # 게임 진행 상황 표시 변수
tmr = 0  # 진행 시간 체크 변수
sel = 0 # 캐릭터 선택 변수
new_record = False
myplayer = 0


# 플레이어 캐릭터의 생명을 나타내는 변수 PNUMBER
# 변수명을 PNUMBER에서 좀 더 직관적인 life로 변경  PNUMBER → life

life = 5

# 장애물(쓰레기, 지형물)들을 저장하는 리스트 변수 OBJECT

OBJECTS = []


        
class Object:
    object_image = ['Obj01.png', 'Obj02.png', 'Obj03.png', 'Obj04.png', 'Obj05.png', \
                 'Obj06.png', 'Obj07.png', 'Obj08.png', 'Obj09.png', 'Obj10.png', \
                 'Obj11.png', 'Obj12.png', 'Obj13.png', 'Obj14.png', 'Obj15.png', \
                 'Obj16.png', 'Obj17.png', 'Obj18.png', 'Obj19.png', 'Obj20.png', \
                 'Obj21.png', 'Obj22.png', 'Obj23.png', 'Obj24.png', 'Obj25.png', \
                 'Obj26.png', 'Obj27.png', 'Obj28.png', 'Obj29.png', 'Obj30.png', \
                 'Obj31.png', 'Obj32.png', 'Obj33.png', 'Obj34.png', 'Obj35.png', \
                 'Obj36.png', 'Obj37.png', 'Obj38.png', 'Obj39.png', 'Obj40.png'
                ]

 

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""

 
# 해당 캐릭터에 맞는 이미지를 불러와 플레이어를 초기화한다.
    def load_object(self, p=""):
        
        if p == "p":
            
            # 첫 번째 캐릭터인 펭귄을 선택한 경우
            self.image = pygame.image.load(DIROBJECTS + "Player.png")

            #게임 화면 크기에 맞게 캐릭터의 크기를 조정한다.
            self.image = pygame.transform.scale(self.image, (150, 150))
            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
            # 두 번째 캐릭터인 북극곰을 선택한 경우
        elif p == "b":
            self.image = pygame.image.load(DIROBJECTS + "Player2.png")

            # 펭귄을 선택했을 때와 동일하게 적절한 크기로 이미지를 변환한다.
            self.image = pygame.transform.scale(self.image, (150, 150))
            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
        
        else:
            # 쓰레기와 자연, 동물 이미지        
            # 40개의 이미지중에서 랜덤으로 선택한다.
            self.image = pygame.image.load(DIROBJECTS + random.choice(self.object_image))
            self.rect = self.image.get_rect()


        
            object_width = 60
            object_height = round((self.rect.height * object_width) / self.rect.width)
 

            self.image = pygame.transform.scale(self.image, (object_width, object_height))
            self.rect.width = object_width
            self.rect.height = object_height

 

            # 생성 위치 - 스크린 크기 안에서 랜덤으로 x 좌표 생성. y 좌표는 스크린 밖 위에 생성
            self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)


            # 올라가는 STAGE에 따라 화면의 스크롤 속도를 높인다.

            # 고정된 속도의 변화 폭이 아닌 random한 값으로 5 ~ speed의 범위 안에서 증가시킨다.
            speed = STAGE + 5
            if speed > 15:
                speed = 15
            self.dy = random.randint(5, speed)

 

    # 생성한 오브젝트를 화면에 표현한다.

    def draw_object(self):
        SCREEN.blit(self.image, [self.rect.x, self.rect.y])



    # 플레이어 캐릭터의 x 좌표 이동을 담당하는 함수

    def move_x(self):
        self.rect.x += self.dx

 

    # 플레이어 캐릭터의 y 좌표 이동을 담당하는 함수

    def move_y(self):
        self.rect.y += self.dy

 

    # 화면에서 벗어나는 경우 다시 이동시킨다.

    def check_screen(self):        
        if self.rect.right > WINDOW_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

 

    # 오브젝트끼리 일어나는 충돌을 감지해서 처리
    # distance : 각 방향에서 떨어진 거리

    # x와 y의 범위가 겹쳐지는 경우를 충돌이라고 판정하기

    def check_collision(self, obj, distance = 0):
        if (self.rect.top + distance < obj.rect.bottom) and (obj.rect.top < self.rect.bottom - distance) and (self.rect.left + distance < obj.rect.right) and (obj.rect.left < self.rect.right - distance):
            return True
        else:
            return False


 
def draw_score():
    # 점수를 기록하고 출력한다.
    font_01 = pygame.font.SysFont("Consolas", 30, True, False)
    text_score = font_01.render("Score : " + str(SCORE), True, BLACK)
    SCREEN.blit(text_score, [15, 15])
    


 

    # 캐릭터의 생명 출력
    for i in range(life):
        # 생명의 숫자에 따라 문자 또는 이미지로 표시할 지 결정, 5개 이상인 경우 문자로 표현
        if i < 5:
            life_Image = pygame.image.load('heart.png')
            life_Image = pygame.transform.scale(life_Image, (25, 25))
            px = WINDOW_WIDTH - 25 - (i * 30)
            SCREEN.blit(life_Image, [px, 15])
        # 숫자로 표현하는 조건문
        else:
            text_Life = font_01.render("+" + str(life - 5), True, WHITE)
            text_Life_x = WINDOW_WIDTH - 30 - (5 * 30)
            SCREEN.blit(text_Life, [text_Life_x, 25])



# 미려한 폰트의 효과를 위한 함수
def draw_text(scrn, txt, x, y, siz, col):  # 그림자 포함 문자

    fnt = pygame.font.Font(None, siz)
    cr = int(col[0] / 2)
    cg = int(col[1] / 2)
    cb = int(col[2] / 2)
    sur = fnt.render(txt, True, (cr, cg, cb))
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur, [x + 1, y + 1])
    cr = col[0] + 128
    if cr > 255: cr = 255
    cg = col[1] + 128
    if cg > 255: cg = 255
    cb = col[2] + 128
    if cb > 255: cb = 255
    sur = fnt.render(txt, True, (cr, cg, cb))
    scrn.blit(sur, [x - 1, y - 1])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])

    
       
def increase_score():
    global SCORE, STAGE, STAGESCORE
    # 점수의 증가 폭은 100점

    SCORE += 100

    # 스테이지에 따라 속도의 증가 정도를 결정하는 STAIR
    if STAGE == 1:
        stair = STAGESTAIR
    else:
        stair = (STAGE - 1) * STAGESTAIR

 

    # 스테이지에 따른 증가 차이
    if SCORE >= STAGESCORE + stair:
        STAGE += 1
        STAGESCORE = STAGESCORE + stair
    

def main():
    global SCREEN, obj_COUNT, WINDOW_WIDTH, WINDOW_HEIGHT, life, bg_y, idx, tmr, SCORE, STAGE, sel, hiscore, new_record, myplayer



    # 초기화 작업

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Polar Wants to Go Home")
    
    icon = pygame.image.load(DIROBJECTS + 'icon.png').convert_alpha()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    
    # BGM 설정
    
    pygame.mixer.music.load(DIRSOUND + "background.mp3")
    
    # 오브젝트와 충돌한 경우 사용하는 효과음
    sound_crash = pygame.mixer.Sound(DIRSOUND + "crash.ogg")
    
    # 배경 음악은 무한 반복으로 재생
    pygame.mixer.music.play(-1)
    
    
    # tmr = tmr+1
    key = pygame.key.get_pressed()
    
    img_player = [
        pygame.image.load(DIROBJECTS + "Player.png"),
        pygame.image.load(DIROBJECTS + "Player2.png"),
        pygame.image.load(DIROBJECTS + "Player3.png")
    ]

    for i in range(3):
        img_player[i] = pygame.transform.scale(img_player[i], (200, 200))
    

    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()
                
                
        tmr = tmr+1
        key = pygame.key.get_pressed()
        
    


        if idx == 0:  # 메인 화면
           # SCREEN.blit(img_title, [360 - 320, 200 - 100])
           
            draw_text(SCREEN, "[S] Select Your Character", WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80, 60, YELLOW)
            if key[K_s] != 0:
                idx = 6
            
            if tmr % 10 < 5:
                draw_text(SCREEN, "Press SPACE !", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 60, YELLOW)
            if key[K_SPACE] == 1:
                    stage = 1
                    SCORE = 0
                    life = 5
                    new_record = FALSE
                    # player = Object(round(WINDOW_WIDTH / 2 ), round(WINDOW_HEIGHT - 150), 0 , 0)
                    # player.load_object("p")
                    


        # 위에 선언한 OBJECT 리스트를 사용하여 오브젝트 객체 생성

                    for i in range(obj_COUNT):
                        obj = Object(0, 0, 0, 0)
                        obj.load_object()
                        OBJECTS.append(obj)
                        idx = 1
                        tmr = 0
                
        if idx == 1:  # 게임 플레이
            
            # 배경 고속 스크롤
            bg_y = (bg_y + 16) % 800
            SCREEN.blit(background,[0, bg_y - 800])
            SCREEN.blit(background,[0, bg_y])
            
            # pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 5
                elif event.key == pygame.K_LEFT:
                    player.dx = -5
                if event.key == pygame.K_DOWN:
                    player.dy = 5
                elif event.key == pygame.K_UP:
                    player.dy = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.dx = 0
                elif event.key == pygame.K_LEFT:
                    player.dx = 0
                if event.key == pygame.K_DOWN:
                    player.dy = 0
                elif event.key == pygame.K_UP:
                    player.dy = 0
    


            # 
            player.draw_object()
            player.move_x()
            player.move_y()
            player.check_screen()
    

            # 오브젝트들의 움직임 나타내기
            for i in range(obj_COUNT):
                OBJECTS[i].draw_object()
                OBJECTS[i].rect.y += OBJECTS[i].dy
                # 화면의 y축에서 벗어나 완전히 보이지 않을 때 새롭게 로드한다.
                # 오브젝트의 y좌표를 랜덤으로 설정하여 갑자기 나타난 듯한 효과를 준다.
                if OBJECTS[i].rect.y > WINDOW_HEIGHT:
                    increase_score()
                    OBJECTS[i].load_object()
                    
                    
            for i in range(obj_COUNT):
                if player.check_collision(OBJECTS[i], 5) and life >= 0:
                    life -= 1
                    sound_crash.play()
                        
                    # 부딪쳤을 경우 서로 튕겨나가게 함. 좌우 튕김
                    if player.rect.x > OBJECTS[i].rect.x:
                        OBJECTS[i].rect.x -= OBJECTS[i].rect.width + 10
                    else:
                        OBJECTS[i].rect.x += OBJECTS[i].rect.width + 10
                        
                    # 위 아래 튕김
                    
                    if player.rect.y > OBJECTS[i].rect.y:
                        OBJECTS[i].rect.y -= 30
                    else:
                        OBJECTS[i].rect.y += 30
            
                        
                if life < 0:
                    pygame.time.delay(2000) 
                    # display_game_over()
                    
                    pygame.display.update()
                



            # 상대 오브젝트들끼리 충돌 감지, 각 오브젝트끼리 순서대로 비교한다.
            for i in range(obj_COUNT):
                for j in range(i + 1, obj_COUNT):
                    # 충돌 후 서로 튕겨 나가게 함.
                    if OBJECTS[i].check_collision(OBJECTS[j]):
                        # 왼쪽에 있는 오브젝트는, 왼쪽으로 오른쪽은 반대방향
                        if OBJECTS[i].rect.x > OBJECTS[j].rect.x:
                            OBJECTS[i].rect.x += 4
                            OBJECTS[j].rect.x -= 4
                        else:
                            OBJECTS[i].rect.x -= 4
                            OBJECTS[j].rect.x += 4

    

                        # 위쪽에 위치한 오브젝트는 위로, 아래에 위치한 오브젝트는 아래로 이동한다.
                        if OBJECTS[i].rect.y > OBJECTS[j].rect.y:
                            OBJECTS[i].rect.y += OBJECTS[i].dy
                            OBJECTS[j].rect.y -= OBJECTS[j].dy
                        else:
                            OBJECTS[i].rect.y -= OBJECTS[i].dy
                            OBJECTS[j].rect.y += OBJECTS[j].dy

 
            if life == 0:
                idx = 4
                tmr = 0
            if tmr == 1:
                pygame.mixer.music.load(DIRSOUND + "background.mp3")
                pygame.mixer.music.play(-1)


        if idx == 2:  # 생명을 모두 소진한 경우
            draw_text(SCREEN, "MISS", WINDOW_WIDTH, WINDOW_HEIGHT, 40, RED)
            if tmr == 1:
                pygame.mixer.music.stop()
                life = life - 1
            if tmr == 5:
                pygame.mixer.music.play(0)
            if tmr == 50:
                if life == 0:
                    idx = 3
                    tmr = 0
                else:
                    idx = 1
                    tmr = 0
        
        if idx == 3:  # 게임 오버
            draw_text(SCREEN, "GAME OVER", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 40, RED)
            if tmr == 50:
                idx = 0
            if new_record == True:
                draw_text(SCREEN, "NEW RECORD " + str(hiscore), 480, 400, 60, YELLOW)  
                
                
        if idx == 4:  # 마지막 생명에서 충돌한 경우 BAAM 문구 출력
            if stage < 5:
                draw_text(SCREEN, "BAAAM!!!", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 60, RED)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 5:
                pygame.mixer.music.play(0)
            if tmr == 50:
                    idx = 5
                    tmr = 0
                    
                    
        if idx == 5:  # 완전한 엔딩
            if tmr < 60:
                xr = 8 * tmr
                yr = 6 * tmr
                pygame.draw.ellipse(SCREEN, BLACK, [360 - xr, 270 - yr, xr * 2, yr * 2])
            else:
                pygame.draw.rect(SCREEN, BLACK, [0, 0, 720, 800])
                # SCREEN.blit(img_ending, [360 - 120, 300 - 80])
                draw_text(SCREEN, "Game Over", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 60, BLINK[tmr % 6])
            if tmr == 300:
                idx = 0     
        if idx == 6:
            draw_text(SCREEN, "Select your Character!", WINDOW_WIDTH//2 + 10, 160, 60, YELLOW) 
            for i in range(2):
                x = 160 + 240 * i
                y = 300
                col = BLACK
                if i == myplayer:
                    col = (0, 128, 255)
                pygame.draw.rect(SCREEN, col, [x - 100, y - 80, 200, 160])
                draw_text(SCREEN, "[" + str(i + 1) + "]", x, y - 50, 60, WHITE)
                SCREEN.blit(img_player[i], [x - 90, y - 70])
            draw_text(SCREEN, "[Enter] OK!", WINDOW_WIDTH//2, 440, 60, YELLOW)
            if key[K_1] == 1:
                myplayer = 0
                player = Object(round(WINDOW_WIDTH / 2 ), round(WINDOW_HEIGHT - 150), 0 , 0)
                
                player.load_object("p")

            if key[K_2] == 1:
                myplayer = 1
                player = Object(round(WINDOW_WIDTH / 2 ), round(WINDOW_HEIGHT - 150), 0 , 0)
                player.load_object("b")
                
            if key[K_RETURN] == 1:
                idx = 0    

        draw_score()
        pygame.display.flip()
        SCREEN.blit(background, (0, 0))



        # 초당 프레임 설정
        clock.tick(60)


pygame.quit()

if __name__ == '__main__':
    main()
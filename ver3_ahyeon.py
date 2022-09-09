import selectors
import sys
from tkinter import Canvas
from turtle import color
import pygame
import random
import time
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pygame.locals import *

# 게임 화면 크기
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLINK = [(255, 255, 255), (255, 255, 192), (255, 255, 128), (255, 224, 64), (255, 255, 128), (255, 255, 192)]

# 도로 움직임
bg_y = 0

background = pygame.image.load("background.png")
# img_title = pygame.image.load("title.png")
# img_ending = pygame.image.load("gameover.png")

# 소스 디렉토리
DIROBJECTS = "OBJECTS/"
DIRSOUND = "sound/"
DIRBG = "bg/"

# 게임 오버 관련 변수
# pygame.init()
# game_result = None # 게임 결과
# is_game_over = False\mmmmmmmmmmmmmmmmmmmmmmmmmmmmm      ,,
# game_font = pygame.font.SysFont(None, 40)

# 기본 변수
STAGE = 1 # 스테이지 수
obj_COUNT = 5
SCORE = 0 # 점수
STAGESCORE = 0 # 스테이지 점수
STAGESTAIR = 1000 # 스테이지 간격
idx = 0  # 게임 메뉴 선택 변수
tmr = 0  # 타이머
sel = 0  # 캐릭터 선택 변수

# 플레이어 Life 갯수
PNUMBER = 5

# 오브젝트를 저장할 List
OBJECTS = []

# Object 클래스 생성
class Object:
    # Object_image에 이미지를 배열의 형태로 저장
    Object_image = ['Obj01.png', 'Obj02.png', 'Obj03.png', 'Obj04.png', 'Obj05.png', \
                    'Obj06.png', 'Obj07.png', 'Obj08.png', 'Obj09.png', 'Obj10.png', \
                    'Obj11.png', 'Obj12.png', 'Obj13.png', 'Obj14.png', 'Obj15.png', \
                    'Obj16.png', 'Obj17.png', 'Obj18.png', 'Obj19.png', 'Obj20.png', \
                    'Obj21.png', 'Obj22.png', 'Obj23.png', 'Obj24.png', 'Obj25.png', \
                    'Obj26.png', 'Obj27.png', 'Obj28.png', 'Obj29.png', 'Obj30.png', \
                    'Obj31.png', 'Obj32.png', 'Obj33.png', 'Obj34.png', 'Obj35.png', \
                    'Obj36.png', 'Obj37.png', 'Obj38.png', 'Obj39.png', 'Obj40.png'
                    ]
    # 클래스 내부 attribute
    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""
    
    # 이미지 로드(가져오기)
    def load_object(self, p=""):

        if p == "p":

            # 플레이어 캐릭터
            self.image = pygame.image.load(DIROBJECTS + "Player.png")

            # 크기 조정
            self.image = pygame.transform.scale(self.image, (150, 150))
            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        elif p == "b":
            self.image = pygame.image.load(DIROBJECTS + "Player2.png")

            # 크기 조정
            self.image = pygame.transform.scale(self.image, (150, 150))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        else:
            # 쓰레기와 자연, 동물 이미지
            # 40개의 이미지 중에서 랜덤으로 선택한다.
            self.image = pygame.image.load(DIROBJECTS + random.choice(self.Object_image))
            self.rect = self.image.get_rect()

            # 이미지 크기 조절 - 이미지마다 크기가 다 다르므로 가로 세로 비율 유지하면서 변경
            # if self.rect.width <= 55:
            #     object_width = self.rect.width - 15
            #     object_height = round((self.rect.height * object_width) / self.rect.width)
            # else:
            #     object_width = self.rect.width
            #     object_height = self.rect.height

            object_width = 60
            object_height = round((self.rect.height * object_width) / self.rect.width)

            self.image = pygame.transform.scale(self.image, (object_width, object_height))
            self.rect.width = object_width
            self.rect.height = object_height

            # 생성 위치 - 스크린 크기 안에서 랜덤으로 x 좌표 생성. y 좌표는 스크린 밖 위에 생성
            self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)

            # STAGE에 따른 속도 변화, STAGE가 높아짐에 따라 물체의 속도도 빨라진다.
            # 다양한 속도 차이를 위해 5 ~ speed 사이에서 랜덤으로 속도를 선택하게 한다.
            speed = STAGE + 5
            if speed > 15:
                speed = 15
            self.dy = random.randint(5, speed)

    # 오브젝트를 스크린에 그리기
    def draw_object(self):
        # 설정된 x축과 y축 위치에 이미지를 화면에 표시
        SCREEN.blit(self.image, [self.rect.x, self.rect.y])

    # x 좌표 이동 - 플레이어 캐릭터의 x축 움직임 제어할 때 필요
    def move_x(self):
        self.rect.x += self.dx

    # y 좌표 이동 - 플레이어 캐릭터의 y축 움직임 제어할 때 필요
    def move_y(self):
        self.rect.y += self.dy

    # 화면 밖으로 못 나가게 방지
    def check_screen(self):
        #x축 밖으로 못 나가도록 설정
        if self.rect.right > WINDOW_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        #y축 밖으로 못 나가도록 설정 
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

    # 오브젝트 충돌 감지
    # distance : 오른쪽, 왼쪽, 아래쪽, 위쪽 이미지의 간격 설정
    def check_collision(self, obj, distance=0):
        if (self.rect.top + distance < obj.rect.bottom) and (obj.rect.top < self.rect.bottom - distance) and (
                self.rect.left + distance < obj.rect.right) and (obj.rect.left < self.rect.right - distance):
            return True
        else:
            return False

def draw_score():
    # SCORE 기록
    font_01 = pygame.font.SysFont("Consolas", 30, True, False)
    text_score = font_01.render("Score : " + str(SCORE), True, BLACK)
    SCREEN.blit(text_score, [15, 15])

    # STAGE 기록
    # text_stage = font_01.render("STAGE : " + str(STAGE), True, BLACK)
    # # 화면 가운데 위치
    # text_stage_rect = text_stage.get_rect()
    # text_stage_rect.centerx = round(WINDOW_WIDTH / 2)
    # SCREEN.blit(text_stage, [text_stage_rect.x, 15])

    # 플레이어 Life 기록
    for i in range(PNUMBER):
        # 5개는 그림으로
        if i < 5:
            pimage = pygame.image.load('heart.png')
            pimage = pygame.transform.scale(pimage, (25, 25))
            px = WINDOW_WIDTH - 25 - (i * 30)
            SCREEN.blit(pimage, [px, 15])
        # 5개가 넘으면 숫자로 표현해준다.
        else:
            text_pnumber = font_01.render("+" + str(PNUMBER - 5), True, WHITE)
            text_pnumber_x = WINDOW_WIDTH - 30 - (5 * 30)
            SCREEN.blit(text_pnumber, [text_pnumber_x, 25])

def draw_txt(scrn, txt, x, y, siz, col):
    # 그림자 포함 문자
    fnt = pygame.font.Font(None, siz * 2)
    sur = fnt.render(txt, True, BLACK)
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur, [x + 2, y + 2])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])

# def display_game_over():

#     txt_game_over = game_font.render("Game Over", True, RED)
#     rect_game_over = txt_game_over.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
#     SCREEN.blit(txt_game_over, rect_game_over)

def increase_score():
    global SCORE, STAGE, STAGESCORE
    # 점수 10점 추가
    SCORE += 10

    # STAGE별 증가율을 위한 stair 값 설정
    if STAGE == 1:
        stair = STAGESTAIR
    else:
        stair = (STAGE - 1) * STAGESTAIR

    # 스테이지 별 증가율에 따른 STAGE 증가
    if SCORE >= STAGESCORE + stair:
        STAGE += 1
        STAGESCORE = STAGESCORE + stair


def main():
    global SCREEN, obj_COUNT, WINDOW_WIDTH, WINDOW_HEIGHT, PNUMBER, bg_y, idx, tmr, SCORE, STAGE, sel

    # pygame 초기화 및 스크린 생성
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Polar Wants to Go Home")
    # 투명 아이콘은 32 x 32 로 해야 적용 됨
    windowicon = pygame.image.load(DIROBJECTS + 'icon.png').convert_alpha()
    pygame.display.set_icon(windowicon)

    clock = pygame.time.Clock()

    # 배경음악 지정
    pygame.mixer.music.load(DIRSOUND + "background.ogg")

    # 충돌 사운드 지정
    sound_crash = pygame.mixer.Sound(DIRSOUND + "crash.ogg")

    # 배경음악 무한 반복 실행
    pygame.mixer.music.play(-1)

    tmr = tmr + 1
    key = pygame.key.get_pressed()

    img_player = [
        pygame.image.load(DIROBJECTS + "Player.png"),
        pygame.image.load(DIROBJECTS + "Player2.png"),
        pygame.image.load(DIROBJECTS + "Player3.png")
    ]

    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 0:  # 타이틀 화면
            # SCREEN.blit(img_title, [360 - 320, 200 - 100])

            # draw_Txt(SCREEN, "Select Your Character", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 30, YELLOW)

            # 캐릭터 선택 기능
            # if tmr % 10 < 2:
            #     x = 160 + 240
            #     y = 300
            #     col = BLACK

            #     for i in range(2):
            #         pygame.draw.rect(SCREEN, col, [x - 100, y - 80, 200, 160])
            #         draw_Txt(SCREEN, "[" + str(i + 1) + "]", x, y - 50, WHITE, col)
            #         SCREEN.blit(img_player[i], [x - 100, y - 20])
            #     draw_Txt(SCREEN, "[Enter] OK!", 400, 440, YELLOW)

            # if key[K_1] == 1:
            #     player.load_Object("p")
            # if key[K_2] == 1:
            #     player.load_Object("b")

            # if key[K_RETURN] == 1:
            #     idx = 0

            if tmr % 10 < 5:
                draw_txt(SCREEN, "Press SPACE !", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 30, YELLOW)
            if key[K_SPACE] == 1:
                stage = 1
                score = 0
                PNUMBER = 5
                player = Object(round(WINDOW_WIDTH / 2), round(WINDOW_HEIGHT - 150), 0, 0)
                # player.load_Object("p")

                # 설정한 수 만큼 자동차 오브젝트 생성하여 OBJECTS 리스트에 넣기
                for i in range(obj_COUNT):
                    obj = Object(0, 0, 0, 0)
                    obj.load_object()
                    OBJECTS.append(obj)
                    idx = 1
                    tmr = 0

        if idx == 1:  # 게임 플레이
            # 배경 움직임
            bg_y = (bg_y + 16) % 800
            SCREEN.blit(background, [0, bg_y - 800])
            SCREEN.blit(background, [0, bg_y])

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

            ''' 게임 코드 작성 '''
            player.draw_object()
            player.move_x()
            player.move_y()
            player.check_screen()

            # 쓰레기, 사물 동물 도로위에 움직이기
            for i in range(obj_COUNT):
                OBJECTS[i].draw_Object()
                OBJECTS[i].rect.y += OBJECTS[i].dy
                # 화면 아래로 내려가면 오브젝트를 다시 로드한다.
                # 로드시 오브젝트의 이미지가 랜덤으로 바뀌므로 새로운 물체가 생긴 듯한 효과가 있다.
                if OBJECTS[i].rect.y > WINDOW_HEIGHT:
                    increase_score()
                    OBJECTS[i].load_Object()

            # 플레이어와 오브젝트 충돌 감지
            for i in range(obj_COUNT):
                # 부딪쳤을 경우 check_collision 함수를 이용하여 생명 수 1 감소, 부딪친 소리 내기
                if player.check_collision(OBJECTS[i], 5) and PNUMBER >= 0:
                    PNUMBER -= 1
                    sound_crash.play()
                    # if( == oil.png):

                    # 부딪쳤을 경우 물체끼리 좌우로 튕겨나가게 함(x축 기준)
                    if player.rect.x > OBJECTS[i].rect.x:
                        OBJECTS[i].rect.x -= OBJECTS[i].rect.width + 10
                    else:
                        OBJECTS[i].rect.x += OBJECTS[i].rect.width + 10

                    # 위 아래로 튕김(y축 기준)
                    if player.rect.y > OBJECTS[i].rect.y:
                        OBJECTS[i].rect.y -= 30
                    else:
                        OBJECTS[i].rect.y += 30

                # 생명 수가 0 미만일 때 일정 기간 동안 프로그램 일시 중지(pygame.time.delay() 이용)
                if PNUMBER < 0:
                    pygame.time.delay(2000)
                    # display_game_over()

                    pygame.display.update()

            # 상대 오브젝트들끼리 충돌 감지, 각 물체들을 순서대로 서로 비교
            for i in range(obj_COUNT):
                for j in range(i + 1, obj_COUNT):
                    # 충돌 후 서로 튕겨 나가게 함.
                    if OBJECTS[i].check_collision(OBJECTS[j]):
                        # 왼쪽에 있는 물체는 왼쪽으로 오른쪽 물체는 오른쪽으로 튕김(x축)
                        if OBJECTS[i].rect.x > OBJECTS[j].rect.x:
                            OBJECTS[i].rect.x += 4
                            OBJECTS[j].rect.x -= 4
                        else:
                            OBJECTS[i].rect.x -= 4
                            OBJECTS[j].rect.x += 4

                        # 위쪽 물체는 위로, 아래쪽 물체는 아래로 튕김(y축)
                        if OBJECTS[i].rect.y > OBJECTS[j].rect.y:
                            OBJECTS[i].rect.y += OBJECTS[i].dy
                            OBJECTS[j].rect.y -= OBJECTS[j].dy
                        else:
                            OBJECTS[i].rect.y -= OBJECTS[i].dy
                            OBJECTS[j].rect.y += OBJECTS[j].dy

            if PNUMBER == 0:
                idx = 4
                tmr = 0
            if tmr == 1:
                pygame.mixer.music.load(DIRSOUND + "background.mp3")
                pygame.mixer.music.play(-1)

        if idx == 2:  # 생명을 모두 소진했을 때
            draw_txt(SCREEN, "MISS", WINDOW_WIDTH, WINDOW_HEIGHT, 40, RED)
            if tmr == 1:
                pygame.mixer.music.stop()
                PNUMBER = PNUMBER - 1
            if tmr == 5:
                pygame.mixer.music.play(0)
            if tmr == 50:
                if PNUMBER == 0:
                    idx = 3
                    tmr = 0
                else:
                    idx = 1
                    tmr = 0

        if idx == 3:  # 게임 오버
            draw_txt(SCREEN, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 40, RED)
            if tmr == 50:
                idx = 0

        if idx == 4:  # 스테이지 클리어
            if stage < 5:
                draw_txt(SCREEN, "BAAAM!!!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 40, RED)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 5:
                pygame.mixer.music.play(0)
            if tmr == 50:
                idx = 5
                tmr = 0

        if idx == 5:  # 엔딩
            if tmr < 60:
                xr = 8 * tmr
                yr = 6 * tmr
                pygame.draw.ellipse(SCREEN, BLACK, [360 - xr, 270 - yr, xr * 2, yr * 2]) # 타원 그리기 모듈
            else:
                pygame.draw.rect(SCREEN, BLACK, [0, 0, 720, 540]) # 사각형 그리기 모듈
                # SCREEN.blit(img_ending, [360 - 120, 300 - 80])
                draw_txt(SCREEN, "Game Over", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 40, BLINK[tmr % 6])
            if tmr == 300:
                idx = 0
        ''' 게임 코드 끝 '''

        draw_score()

        pygame.display.flip()

        SCREEN.blit(background, (0, 0))

        # 초당 프레임 설정
        clock.tick(60)

# 파이게임 종료
pygame.quit()

if __name__ == '__main__':
    main()

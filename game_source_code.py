import pygame, sys
from pygame.locals import *
import random, time


pygame.init()
# 초당 프레임 설정
FPS = 60
FramePerSec = pygame.time.Clock()

# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수

# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("game over !", True, (0, 0, 0))  # 게임 종료시 문구

# 게임 배경화면
background = pygame.image.load('back_ground.jpg')  # 배경화면 사진 로드

# 게임 화면 생성 및 설정
GameDisplay = pygame.display.set_mode((600, 800))
GameDisplay.fill((255, 153, 153))
pygame.display.set_caption("폭탄 무당이 피하기")


class Enemy(pygame.sprite.Sprite):

    # 적의 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('boom2.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("Bomb : ", self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (random.randint(40, 600), 0)

    # 적의 움직임 설정 함수+ 플레이어 점수 측정
    def move(self):
        global SCORE

        # 적을 10픽셀크기만큼 위에서 아래로 떨어지도록 설정
        self.rect.move_ip(0, SPEED)  # x,y좌표 설정
        # 이미지가 화면 끝에 있으면(플레이어가 물체를 피하면) 다시 이미지 위치 세팅 + 1점 추가
        if self.rect.bottom > 440:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 610), 0)
        return self.rect.center

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('./image_user/user_Base.jpg')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("Player : ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (540, 390)

    # 플레이어 키보드움직임 설정 함수
    def move(self):
        prssdKeys = pygame.key.get_pressed()
        # 왼쪽 방향키를 누르면 5만큼 왼쪽 이동
        if self.rect.left > 0:
            if prssdKeys[K_LEFT]:
                self.rect.move_ip(-5, 0)
                position_p = self.rect.center
                return position_p # 이 부분은 왜 필요한 건지 모르겠지만 일단 지우지 않았음. (추후에 필요할까봐)
        # 오른쪽을 누르면 5만큼 오른쪽으로 이동
        if self.rect.right < 640:
            if prssdKeys[K_RIGHT]:
                self.rect.move_ip(5, 0)
                position_p = self.rect.center
                return position_p # 이 부분은 왜 필요한 건지 모르겠지만 일단 지우지 않았음. (추후에 필요할까봐)

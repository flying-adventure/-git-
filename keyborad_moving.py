# 캐릭터 사진으로 불러오고 키보드에 따라 움직이도록 설정
# 코드 돌리기 전에 터미널에 'pip install pygame' 명령어 입력해야함.

import pygame
from pygame.locals import K_LEFT, K_RIGHT

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
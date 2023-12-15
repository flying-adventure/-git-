import pygame, sys
from pygame.locals import *
import random, time
import os
import cv2
import numpy as np

##open CV를 사용하여 user 이미지를 받아 얼굴부분만 크롭하기
face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('../haarcascade_eye.xml')

img = cv2.imread("image/person.jpg")
if img is None:
    print("Can't read image file.")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)


    for (x,y,w,h) in faces:
        cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
        output_path = os.path.join("image", "cropped_by_OpenCV.png")
        cv2.imwrite(output_path, cropped)
      

   
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
##얼굴 크롭 사진과 캐릭터 이미지 병합하기

# 이미지 파일 로드
user_base_image = cv2.imread("image/user_Base.png")
user_lose_image = cv2.imread("image/user_Lose.png")
user_warning_image = cv2.imread("image/user_Warning.png")
user_win_image = cv2.imread("image/user_Win.png")

cropped_image = cv2.imread("image/cropped_by_OpenCV.png")

# 이미지 크기에 맞게 이미지 resize
cropped_image = cv2.resize(cropped_image, (user_base_image.shape[1], user_base_image.shape[0]))
user_lose_image = cv2.resize(user_lose_image, (user_base_image.shape[1], user_base_image.shape[0]))
user_warning_image = cv2.resize(user_warning_image, (user_base_image.shape[1], user_base_image.shape[0]))
user_win_image = cv2.resize(user_win_image, (user_base_image.shape[1], user_base_image.shape[0]))

# 두 이미지를 합치기
result = cv2.addWeighted(user_base_image, 0.4, cropped_image, 0.7, 0.5)
output_path = "image/combined_user_Base.png"
cv2.imwrite(output_path, result)
result_lose = cv2.addWeighted(cropped_image, 0.4, user_lose_image, 0.7, 0.5)
output_path_lose = "image/combined_user_Lose.png"
cv2.imwrite(output_path_lose, result_lose)
result_warning = cv2.addWeighted(cropped_image, 0.4, user_warning_image, 0.7, 0.5)
output_path_warning = "image/combined_user_Warning.png"
cv2.imwrite(output_path_warning, result_warning)
result_win = cv2.addWeighted(cropped_image, 0.4, user_win_image, 0.7, 0.5)
output_path_win = "image/combined_user_Win.png"
cv2.imwrite(output_path_win, result_win)


##game function

pygame.init()
# 초당 프레임 설정
FPS = 60
FramePerSec = pygame.time.Clock()

# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수
level = 1 # 플레이어 레벨


# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("game over !", True, (0, 0, 0))  # 게임 종료시 문구

# 게임 배경화면
background = pygame.image.load('image/back_ground.jpg')  # 배경화면 사진 로드
ending_image = pygame.image.load('image/combined_user_Lose.png')

# 게임 화면 생성 및 설정
GameDisplay = pygame.display.set_mode((600, 800))
GameDisplay.fill((255, 153, 153))
pygame.display.set_caption("무당이가 폭탄이라면?")


class Enemy(pygame.sprite.Sprite):

    # 적의 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('image/bomb_Base.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("Bomb : ", self.rect)
        # 이미지 시작 위치 설정

        self.rect.center = 40, 300

    # 적의 움직임 설정 함수 + 플레이어 점수 측정
    def move(self):
        global SCORE, SPEED, level

        self.rect.center = (random.randint(40, 600), 0)

    # 적의 움직임 설정 함수 + 플레이어 점수 측정
    def move(self):
        global SCORE, SPEED, level


        # 적을 10픽셀크기만큼 위에서 아래로 떨어지도록 설정
        self.rect.move_ip(0, SPEED)  # x,y좌표 설정
        # 이미지가 화면 끝에 있으면(플레이어가 물체를 피하면) 다시 이미지 위치 세팅 + 1점 추가

        if self.rect.bottom + 50 > 800:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = random.randint(30, 500),0

            # 레벨에 따라 속도 증가
            if SCORE % 6 == 0:  # 예시로 10점 단위로 레벨이 올라가도록 설정
                level += 0.5
                SPEED += level  # 레벨에 따라 속도 증가

        if self.rect.bottom + 50 > 750:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 610), 0)

        return self.rect.center

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('image/combined_user_Base.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("Player : ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (540, 700)
        
        
    # 플레이어 키보드움직임 설정 함수
    def move(self):
        prssdKeys = pygame.key.get_pressed()
        # 왼쪽 방향키를 누르면 6만큼 왼쪽 이동
        if self.rect.left > 0:
            if prssdKeys[K_LEFT]:
                self.rect.move_ip(-6, 0)
                position_p = self.rect.center
                return position_p
        # 오른쪽을 누르면 6만큼 오른쪽으로 이동
        if self.rect.right < 600:
            if prssdKeys[K_RIGHT]:
                self.rect.move_ip(6, 0)
                position_p = self.rect.center
                return position_p

###### 게임 설정 ########
# 플레이어 및 적 개체 생성
P1 = Player()

E1 = Enemy()

# Sprites Groups 생성하기
# 게임 물체들을 그룹화 하여 그룹별로 접근하여 설정 시 용이하게 만들기
# 적(enemy) 객체 그룹화하기
Enemies = pygame.sprite.Group()
Enemies.add(E1)
# 전체 그룹을 묶기
All_groups = pygame.sprite.Group()
All_groups.add(P1)
All_groups.add(E1)

# 적 개체 2초(2000ms)마다 새로 생기는 이벤트 생성
increaseSpeed = pygame.USEREVENT + 1
pygame.time.set_timer(increaseSpeed, 2000)

# 게임 BGM 설정
bgm = pygame.mixer.Sound('Sound/background_sound.mp3')
bgm.play()

## 게임 루프 설정 ##
# 게임 종료되기 전까지 실행되는 루프(이벤트) 설정
while True:
    for event in pygame.event.get():
        #속도 증가
        if event.type == increaseSpeed:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 배경화면 이미지 삽입
    GameDisplay.blit(background, (0, 0))
    # 하단부에 위치할 스코어 점수(적을 피할때마다 +1점 증가)
    scores = small_font.render("Score: " + str(SCORE), True, (0,0,0))
    GameDisplay.blit(scores, (5, 100))

    # group1 = '<Player Sprite(in 1 groups)>'
    # group2 = '<Enemy Sprite(in 2 groups)>'

    # 게임 내 물체 움직임 생성
    for i in All_groups:
        GameDisplay.blit(i.image, i.rect)
        i.move()
        if str(i) == '<Player Sprite(in 1 groups)>':
            player_pos = i
        else:
            enemy_pos = i

    # <Player Sprite(in 1 groups)>
    # 플레이어 충돌 판정(게임종료)시
    if pygame.sprite.spritecollideany(P1, Enemies):
        for i in All_groups:
            i.kill()
        # 물체 이미지 변경(충돌후 변경되는 이미지)
        # 플레이어
        GameDisplay.blit(background, (0, 0))
        image0 = pygame.image.load('image/combined_user_Warning.png')
        image0.get_rect()
        GameDisplay.blit(image0, player_pos)

        # 폭탄
        image1 = pygame.image.load('image/bomb_Warning.png')
        image1.get_rect()
        GameDisplay.blit(image1, enemy_pos)
        pygame.display.update()

        # 배경음악 멈춤
        bgm.stop()
        # 적과 충돌시 효과음 추가
        pygame.mixer.Sound('Sound/boom.mp3').play()
        time.sleep(0.5)
        
        # 게임오버화면 설정
        pygame.mixer.Sound('Sound/boom.mp3').play()
        GameDisplay.fill((255,255,255))
        final_scores = font.render("Your Score: " + str(SCORE), True, (0,0,0))
        GameDisplay.blit(final_scores, (100, 200))
        GameDisplay.blit(game_over, (100, 400))
        GameDisplay.blit(ending_image, (200, 500))
 
        
        time.sleep(1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
        
# End the game if Plyer score more than 15 points

    

    if SCORE > 1:
        GameDisplay.fill((255, 255, 255))
        special_image = pygame.image.load('image/combined_user_Win.png') # 승리 배경 이미지 
        special_image_rect = special_image.get_rect(center=(350, 500))
        font_size = 50
        font = pygame.font.Font(None, font_size)

        final_A = font.render("Successfully", True, (0,0,0))
        final_B = font.render("avoided", True, (0,0,0))
        final_C = font.render("the bombs!!", True, (0,0,0))
        GameDisplay.blit(final_A, (130, 200))
        GameDisplay.blit(final_B, (130, 254))
        GameDisplay.blit(final_C, (130, 308))

        GameDisplay.blit(special_image, special_image_rect)
        
        
        pygame.display.update()
          # 배경음악 멈춤
        bgm.stop()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    # 초당 프레임 설정

    FramePerSec.tick(FPS)


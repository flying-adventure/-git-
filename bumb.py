import pygame 
import random

#pygame 초기화
pygame.init() 

#pygame에 사용되는 전역변수 선언

size = [600, 800]
screen = pygame.display.set_mode(size)
 #스크린 이미지 삽입
background = pygame.image.load('./image/back_ground.jpg')

score = 0
heart=3
running =True
done = True
font = pygame.font.SysFont("arial",20,True,False)
text = font.render("SCORE : {}".format(score),True,(255,255,255))

while running:
    #score삽입 코드
    screen.blit(text,(100,100))
    #배경 삽입 코드
    screen.blit(background,(0,0))
    pygame.display.update()

    #접촉 처리 코드
    for bom in boms:
        #접촉 감지
        if bomb['rect'].colliderect(person):
            #변수 증가
            heart -=1;
        
        if not heart:
            running = False

        #폭탄 화면 출력

        #폭탄 출력 후 바닥 지점을 넘어갔을때
        if bomb['rect'].top > size[1]:
            #폭탄 제거, 리스트 추가.
            score+=1






pygame.quit()
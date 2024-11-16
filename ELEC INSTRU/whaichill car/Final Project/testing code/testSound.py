import pygame
import time
pygame.mixer.pre_init(44100,16, 2, 4096)
pygame.init()
x = pygame.mixer.Sound("ELEC INSTRU/whaichill car/Final Project/main/sound/chinesebt.wav")
a = pygame.mixer.Sound("ELEC INSTRU/whaichill car/Final Project/main/sound/bmwbong.wav")

x.play()
time.sleep(4)
a.play()
time.sleep(2)
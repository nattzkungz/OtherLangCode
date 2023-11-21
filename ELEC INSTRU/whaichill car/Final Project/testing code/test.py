import pygame
import time
pygame.mixer.pre_init(44100,16, 2, 4096)
pygame.init()

bmw = pygame.mixer.Sound("ELEC INSTRU/Raspberry Pi (Python)/Final Project/main/bmwbong.wav")

for i in range(3):
    bmw.play()
    time.sleep(2)
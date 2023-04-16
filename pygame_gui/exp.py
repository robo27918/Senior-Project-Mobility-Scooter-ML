import pygame
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

pygame.init()

screen = pygame.display.set_mode((640, 480))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            file_path = filedialog.askopenfilename()
            print(file_path)

    pygame.display.flip()

pygame.quit()

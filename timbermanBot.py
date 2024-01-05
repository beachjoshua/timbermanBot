import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("Press 's' to start.")
print("Press 'q' to quit.")
keyboard.wait('s')
left = True
sct = mss.mss()
dimensionsLeft = {
        'left': 20,
        'top': 720,
        'width': 370,
        'height': 250
    }

dimensionsRight = {
        'left': 420,
        'top': 720,
        'width': 360,
        'height': 250
    }

caneLeft = cv2.imread('cactusLLLL.png')
caneRight = cv2.imread('cactusRRRR.png')
w = caneLeft.shape[1]
h = caneLeft.shape[0]

fpsTime = time()
while True:
    if keyboard.is_pressed('q'):
        break
    
    if left:
        scr = numpy.array(sct.grab(dimensionsLeft))
        cane = caneLeft
    else:
        scr = numpy.array(sct.grab(dimensionsRight))
        cane = caneRight
        
    # Cut off alpha
    scr_remove = scr[:,:,:3]
    result = cv2.matchTemplate(scr_remove, cane, cv2.TM_SQDIFF_NORMED)
    
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    print(f"Max Val: {maxVal} Max Loc: {maxLoc}")
    src = scr.copy()
    if maxVal >= 0.71:
        print("NOWSWITCHC\n")
        left = not left
        scr = cv2.rectangle(scr, maxLoc, (maxLoc[0] + w, maxLoc[1] + h), (0,255,255), 2)
        sleep(.12)
    '''elif maxVal>=.81:
        print("NOW\n")
        left = not left
        scr = cv2.rectangle(scr, maxLoc, (maxLoc[0] + w, maxLoc[1] + h), (0,255,255), 2)
        sleep(.2)'''
    
    if left:
        pyautogui.press('left')
    else:
        pyautogui.press('right')
        
    cv2.imshow('Screen Shot', scr)
    cv2.waitKey(1)
    
    sleep(.13)
    print('FPS: {}'.format(1 / (time() - fpsTime)))
    fpsTime = time()

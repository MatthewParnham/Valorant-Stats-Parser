import cv2
import numpy as np
import os
from functools import reduce
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


def compare_images(im1, im2, threshold):
    buffer = 9
    if im1.shape == im2.shape:
        for i in range(buffer,im1.shape[0]-buffer):
            for j in range(buffer,im1.shape[1]-buffer):
                if Average(im1[i][j] - im2[i][j]) > threshold:
                    return False
        return True
    else:
        return False

def classify_hero(im):
    hero_images = []
    hero_image_names = ['brimstone', 'brimstone', 'cypher', 'cypher', 'jett', 'jett', 'omen', 'phoenix', 'phoenix', 'raze', 'raze', 'sage', 'sage',
                        'sova', 'sova', 'viper', 'viper']
    for filename in os.listdir("hero_training"):
        hero_images.append(cv2.imread("hero_training/" + filename))
    for i in range(len(hero_images)):
        if compare_images(hero_images[i],im,50):
            return hero_image_names[i]


img = cv2.imread('2020-05-01.png')

img = img[:,1920:,:]

scale_percent = 50

width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dsize = (width, height)

scaled_im = cv2.resize(img, dsize)

"""
curr_im = output[176:200,138:162,:]

cv2.imwrite('hero_training/cypher2.png',curr_im)
cv2.imshow('image',curr_im)
cv2.waitKey(0)
cv2.destroyAllWindows()

#output[176:200,138:162,:]
#output[202:226,138:162,:]
#output[228:252,138:162,:]
#output[254:278,138:162,:]
#output[280:304,138:162,:]
#output[306:330,138:162,:]
#output[332:356,138:162,:]
#output[358:382,138:162,:]
#output[384:408,138:162,:]
#output[410:434,138:162,:]
"""
hero_positions = [
    [176,200,138,162],
    [202,226,138,162],
    [228,252,138,162],
    [254,278,138,162],
    [280,304,138,162],
    [306,330,138,162],
    [332,356,138,162],
    [358,382,138,162],
    [384,408,138,162],
    [410,434,138,162]
                  ]

match_heroes = []
for f in range(len(hero_positions)):
    curr_im = scaled_im[hero_positions[f][0]:hero_positions[f][1],138:162,:]
    match_heroes.append(classify_hero(curr_im))




player_name_positions = [
    [352, 400, 328, 600],
    [404, 452, 328, 600],
    [456, 504, 328, 600],
    [508, 556, 328, 600],
    [560, 608, 328, 600],
    [612, 660, 328, 600],
    [664, 712, 328, 600],
    [716, 764, 328, 600],
    [768, 816, 328, 600],
    [820, 868, 328, 600]
                ]

ACS_positions = [
    [352, 400, 650, 750],
    [404, 452, 650, 750],
    [456, 504, 650, 750],
    [508, 556, 650, 750],
    [560, 608, 650, 750],
    [612, 660, 650, 750],
    [664, 712, 650, 750],
    [716, 764, 650, 750],
    [768, 816, 650, 750],
    [820, 868, 650, 750]
                ]

match_player_names = []
player = 0
for p in range(len(player_name_positions)):

    player = p
    img_slice = img[player_name_positions[player][0]:player_name_positions[player][1],player_name_positions[player][2]:player_name_positions[player][3],:]
    #img_slice = cv2.medianBlur(img_slice,3)
    img_slice = cv2.cvtColor(img_slice, cv2.COLOR_BGR2GRAY)
    #img_slice = cv2.adaptiveThreshold(img_slice, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    img_slice = cv2.bitwise_not(img_slice)
    text = pytesseract.image_to_string(img_slice)
    match_player_names.append(text)


match_ACS = []
player = 0
for p in range(len(ACS_positions)):

    player = p
    img_slice = img[ACS_positions[player][0]:ACS_positions[player][1],ACS_positions[player][2]:ACS_positions[player][3],:]
    img_slice = cv2.medianBlur(img_slice,3)
    img_slice = cv2.cvtColor(img_slice, cv2.COLOR_BGR2GRAY)
    #img_slice = cv2.adaptiveThreshold(img_slice, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    img_slice = cv2.bitwise_not(img_slice)
    text = pytesseract.image_to_string(img_slice)
    match_ACS.append(text)

print("hero name acs")
for q in range(10):
    print(match_heroes[q],match_player_names[q],match_ACS[q])

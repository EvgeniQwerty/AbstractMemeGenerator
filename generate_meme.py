from random_word import RandomWords
from PIL import Image, ImageFont, ImageDraw 
from os import system, listdir, remove
from time import sleep
from random import randint

'''
ТУДУ:
    - Исправить все ошибки, из-за которых происходят вылеты в цикле
    - реализовать запуск из командной строки с параметрами
    - исправить отображение многострочного текста
    - ввести проверку на размер изображения
'''

quantity = 100 #количество попыток генерации

for i in range(0, quantity):
    print("Генерируется мем номер {}".format(i+1))
    #генерируем случайное слово
    generator = RandomWords()
    rand_word = generator.get_random_word()
    if str(rand_word) == "None":
        print("Не удалось получить случайное слово\n\n")
        sleep(2)
        continue

    #скачиваем картинку
    args_string = "python download_images.py -s {} --limit 1".format(rand_word) #если не сработает, попробуйте python3 или указать полный путь к исполняемому файлу интерпретатора питона
    print("Слово для запроса картинки - {}".format(rand_word))
    system(args_string)
    sleep(2)
    files = listdir("bing")

    #если картинка скачалась, то добавляем текст
    if len(files) > 0:
        my_img = Image.open("bing\\{}".format(files[0]))
        width, height = my_img.size
        #print(width)
        font_size = 100
        font = ImageFont.truetype('Lobster-Regular.ttf', font_size)
        
        cits_file = open("cits.txt", "r")
        cits_lines = cits_file.readlines()
        text = cits_lines[randint(0, len(cits_lines)-1)].replace('\t', '').replace('…', '.').replace('.', '.\n').replace('!', '!\n').replace('?', '?\n')
        print("Цитата - {}".format(text[:len(text) - 1]))
        cits_file.close()
        
        text_size = font.getsize(text)
        #print(text_size)
        count_dots = text.count('\n')  - 1 
        if count_dots <= 0:
            count_dots = 1
        #print(count_dots)    
        text_size_new = (int(text_size[0] / count_dots), int(text_size[1] * count_dots))
        #print(text_size_new)
    
        while (text_size_new[0] > (width - (width * 0.2))):
            font_size -= 2
            font = ImageFont.truetype('Lobster-Regular.ttf', font_size)
            text_size = font.getsize(text)
            text_size_new = (int(text_size[0] / count_dots), int(text_size[1] * count_dots))
    
        if count_dots > 1:
            button_size = (int(text_size_new[0] + (text_size_new[0] * 0.3) + 20), text_size_new[1]+20)
        else:
            button_size = (int(text_size_new[0] + 20), text_size_new[1] + 20)
        button_img = Image.new('RGBA', button_size, "black")
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((20, 10), text, font=font)
        paste_w = randint(0, width - text_size_new[0]+20)
        paste_h = randint(0, height - text_size_new[1]+20)
        my_img.paste(button_img, (paste_w, paste_h))

        try:
            my_img.save("res/result-{} {}.jpg".format(i+1, randint(0, 100000)))
            print("Готово!\n\n")
        except:
            print("Не удалось сохранить мем\n\n")
        
        try:
            remove("bing\{}".format(files[0]))
        except:
            sleep(1)
            remove("bing\{}".format(files[0]))
        
    else:
        print("Картинка не скачалась\n\n")    
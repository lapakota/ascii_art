Первый проект на python

# Описание:
Консольная программа преобразует цветные картинки в ascii и ansi art формата .txt и .png
либо файлы формата .ansi выводит в консоль(цвета показываются только в linux). 
Принимает на вход картинку, есть возможность задать ширину и высоту выходного ascii art в символах либо scale,
выбрать 1 из 3 режимов(ascii art из 10, 40 или двух(единица и ноль) символов, по умолчанию
стоит режим 40 символов.

# Требования:
Pillow(Python Imaginary Lib)

# Примеры запуска:
python AsciiGenerator.py --image test.jpg --width 240 

python AsciiGenerator.py --image test.jpg --mode double

python AsciiGenerator.py --image test.jpg --scale 0.3

python AsciiGenerator.py --image test.jpg --scale 0.4 --mode double

python AsciiGenerator.py --image 256.ansi

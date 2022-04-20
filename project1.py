
from time import *
from random import choice
from random import randint
from graphics import *

file_gen = open("generation.txt", "a", encoding='utf-8')

''' глобальные переменные и константы:
RIB - ребро квадрата, т.е. размер графической единицы
n_cars - постоянное кол-во особей в каждом поколении
plain - поле
n_way - кол-во шагов в пути каждой особи, постоянное
n_gen - номер поколения
'''

# все функции


n_gen = 0
RIB = 20


# создание графического окна
def create_win():
    global plain, RIB
    winWidth = RIB * len(plain[0]) + 100
    winHeight = RIB * len(plain) + 100
    win = GraphWin("Лабиринт", winWidth, winHeight)
    return win


# отрисовка карты
def drawmap():
    global win
    for i in range(len(plain)):
        for j in range(len(plain[i])):
            p = Point(j * RIB, i * RIB)
            p1 = Point(j * RIB + RIB, i * RIB + RIB)
            figure = Rectangle(p, p1)
            if plain[i][j] == 1:
                figure.setFill('gray')
                figure.setOutline('black')
            elif plain[i][j] == 2:
                figure.setFill('blue')
                figure.setOutline('blue')
            figure.draw(win)
    time.sleep(2)


# отрисовка машины в текущем положении
def drawcar(location):
    figure = Rectangle(Point(location['x'] * RIB, location['y'] * RIB),
                       Point(location['x'] * RIB + RIB, location['y'] * RIB + RIB))
    figure.setOutline('red')
    figure.setFill('red')
    figure.draw(win)
    time.sleep(0.05)
    figure.undraw()


# импорт карты
def map_import(xsizemap):
    file = open('map.txt', 'r', encoding='utf-8')
    plain = [[int(line[i]) for i in range(xsizemap)] for line in file]
    return plain


# сгенерировать рандомный путь для машины в виде списка шагов
## n - количество шагов в пути
def way_gen(n):
    way = [choice(['U', 'D', 'R']) for i in range(n)]
    return way


# пройти путь и найти финиш
## plain - поле (двумерный массив)
## way - путь машины, массив
## результат функции - место и номер шага, на котором путь для конкретной машины закончился
##m - нужна для проверки что функция вызванна из selection
def journey(way,m):
    global pobeda, plain
    x_start = 1
    y_start = 1
    location = {'x': x_start, 'y': y_start}  # текущее местоположение конкретной машины
    for i in range(len(way)):
        # вправо
        if way[i] == 'R':
            location['x'] += 1
            if m == 1:
                drawcar(location)
            if int(plain[location['y']][location['x']]) == 1:
                location['x'] -= 1
                break
        # вверх
        elif way[i] == 'U':
            location['y'] -= 1
            if m == 1:
                drawcar(location)
            if int(plain[location['y']][location['x']]) == 1:
                location['y'] += 1
                break
                # вниз
        elif way[i] == 'D':
            location['y'] += 1
            if m == 1:
                drawcar(location)
            if int(plain[location['y']][location['x']]) == 1:
                location['y'] -= 1
                break
        # если новая координата - стена или финиш, то выходим из цикла
        if plain[location['y']][location['x']] == 2:
            print(location)
            print('WIN')
            pobeda = True
            break

    # конечная координата - место столкновения, i - номер шага, на котором машина споткнулась
    return location, i


# записать поколение в словарь
## шаблон: cars = { 1: { 'way': [], 'finish': {} }, 2: { 'way': [], 'finish': {} } }

# Генерация первого поколения:
def writedown():
    cars = {}
    for i in range(n_cars):
        way = way_gen(n_way)
        result = journey(way,0)
        cars[i] = {'way': way, 'finish': result[0], 'proideno': result[1]}
        file_gen.write(str(i) + " " + str(way) + "\n")
    return cars


# Отбор:
def selection(cars):
    p = 0
    best_1 = 0
    p1 = 0
    best_2 = 0
    for i in range(n_cars):
        if p < cars[i]['proideno']:
            p = int(cars[i]['proideno'])
            best_1 = i
        elif p1 < cars[i]['proideno']:
            p1 = cars[i]['proideno']
            best_2 = i

    journey(cars[best_1]['way'], 1)
    journey(cars[best_2]['way'], 1)
    return cars[best_1], cars[best_2]

# генерация от двух лучших
def reproduction(mom, dad):
    global n_gen
    n_gen += 1
    file_gen.write(str(n_gen) + ' ПОКОЛЕНИЕ' + "\n")
    cars1 = {}
    mway = mom['way']
    mproi = mom['proideno']
    dway = dad['way']
    dproi = dad['proideno']
    numbercut = 5  # число разрезаний

    if mproi >= dproi:
        n = mproi
    else:
        n = dproi
    for gg in range(1, n_cars, 2):
        way = mway[:n]  # mama
        way1 = dway[:n]  # papa
        nn = [n]

        for i in range(1, numbercut):
            # что-то типо разрезания
            g = randint(nn[i - 1] + 1, n_way)
            if g < n_way:
                nn.append(g)
            else:
                nn.append(g)
                break

        if nn[-1] != n_way:
            nn.append(n_way)

        for i in range(1, len(nn)):
            wm = mway[nn[i - 1]: nn[i]]
            # ну тут у нас типа мутации на выделенном отрезке
            for h in range(randint(1, len(wm))):
                c = randint(0, len(wm) - 1)
                spi = ['U', 'D', 'R']
                spi.remove(wm[c])
                wm[c] = choice(spi)

            wd = dway[nn[i - 1]: nn[i]]
            # ну тут у нас типа мутации на выделенном отрезке
            for h in range(randint(1, len(wd))):
                c = randint(0, len(wd) - 1)
                spi = ['U', 'D', 'R']
                spi.remove(wd[c])
                wd[c] = choice(spi)

            if randint(0, 1) == 0:
                for j in range(len(wm)):
                    way.append(wm[j])
                    way1.append(wd[j])
            else:
                for j in range(len(wm)):
                    way.append(wd[j])
                    way1.append(wm[j])
        # запись готовых потомков
        f1 = journey(way, 0)
        finish1 = f1[0]
        i1 = f1[1]
        cars1[gg - 1] = {'way': way, 'finish': finish1, 'proideno': i1}
        file_gen.write(str(gg - 1) + " " + str(way) + "\n")

        f2 = journey(way1, 0)
        finish2 = f2[0]
        i2 = f2[1]
        cars1[gg] = {'way': way1, 'finish': finish2, 'proideno': i2}
        file_gen.write(str(gg) + " " + str(way1) + "\n")


    return cars1



pobeda = False
n_cars = 100
n_way = 150

plain = map_import(50)
win = create_win()
drawmap()

# для скрещивания двух машин
carasiki = writedown()
luh2 = selection(carasiki)
c = reproduction(luh2[0], luh2[1])
while pobeda != True:
    d = selection(c)
    c = reproduction(d[0], d[1])
if pobeda == True:
    d = selection(c)
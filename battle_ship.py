from random import randint

#1. Описание внутренней логики игры:

#1.1 Описание класса точки

class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

#1.2 Описание классов исключений

class BoardException(Exception):
    pass

class BoardOutExeption(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!!!!!!"

class BoardUsedExeption(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipExeption(BoardException):
    pass

#1.3 Описание класса корабля

class Ship:

    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

#1.3 Описание класса игровой доски

class Board:

    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [ ["0"]*size for _ in range(size) ]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipExeption()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutExeption()

        if d in self.busy:
            raise BoardUsedExeption()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []

#2. Описание внешней логики игры:

#2.1 Определение классов игрока

class Player:

    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise  NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):

    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера {d.x + 1} {d.y + 1}')
        return d

class User(Player):

    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()

            if len(cords) != 2:
                print("Введите две координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

#2.2 Определение класса игры

class Game:

    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipExeption:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print('--------------------')
        print('  Приветствуем вас  ')
        print('       в игре       ')
        print('    морской бой     ')
        print('--------------------')
        print('  формат ввода: х у ')
        print('  х - номер строки  ')
        print('  у - номер столбца ')
        print('--------------------')

    def loop(self):
        num = 0
        while True:
            print('-'*20)
            print('Доска пользователя:')
            print(self.us.board)
            print('Доска компьютера:')
            print(self.ai.board)
            print('-'*20)
            if num % 2 ==0:
                print('Ходит пользователь!')
                repeat = self.us.move()
            else:
                print('Ходит компьютер!')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('-' * 20)
                print('Пользователь выиграл!')
                break

            if self.us.board.count == 7:
                print('-' * 20)
                print('Компютер выиграл!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()

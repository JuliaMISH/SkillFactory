#Это финальная версия кода игры "Крестики-нолики"

# 1.1 Объявление глобальных переменных
G1 = 'Игрок 1(х)'
G2 = 'Игрок 2(о)'
count = 1
M = [[" ", 1, 2, 3, '-> X'],
     [1, '-', '-', '-'],
     [2, '-', '-', '-'],
     [3, '-', '-', '-'],
	 ['Y', '', '', '']]
gamer = None
figure = None
marker = None

# 1.2 Объявление глобальных переменных для вывода сообщений
gr_game = '\n******Отличная игра!******\nКак-нибудь надо повторить!\n**************************'

# 2. Объявление функции печати
def print_mess(*args):
	print(*args)

# 3. Объявление функции старта игры
def g_start():
	print(' ***Игра началась!***\n*****Желаем удачи!*****\n***********************')
	a = input('\nИгрок 1(х), представьтесь: ')
	if len(a) != 0:
		global G1
		G1 = a
	b = input('\nИгрок 2(о), представьтесь: ')
	if len(b) != 0:
		global G2
		G2 = b

# 4. Объявление функции вывода поля
def printM():        
     print('')
     for i in range(len(M)):
          #print(M[i])
          for j in range(len(M[i])):
               print(M[i][j], end=" ")
          print("")

# 5. Объявление функции запроса координат х, о
def coord_input():
	global gamer
	global figure
	x = input(f"\n{gamer}, введите х-координату {figure}: ")
	y = input(f"\n{gamer}, введите y-координату {figure}: ")
	if x.isdigit() and y.isdigit():
		x = int(x)
		y = int(y)
		if 1<=x<=3 and 1<=y<=3:
			if M[y][x] == '-':
		         	M[y][x] = marker
		         	printM()
			else:
		         	print(f'\n{gamer}, выберите другие координаты, эти уже заняты')
		         	coord_input()
		else:
			print(f'\n{gamer}, введите координаты строго цифрами в диапазоне от 1 до 3')
			coord_input()
	else:
		print(f'\n{gamer}, введите координаты строго цифрами в диапазоне от 1 до 3')
		coord_input()
		
# 6. Проверка выигрыша
def win_check():
	global gamer
	global marker
	for c in range(1, 4):
		if M[c][1] == marker and M[c][2] == marker and M[c][3] == marker:
			print(f'\n{gamer}, поздравляем с победой!')
			print_mess(gr_game)
			exit()
	for d in range(1, 4):
		if M[1][d] == marker and M[2][d] == marker and M[3][d] == marker:
			print(f'\n{gamer}, поздравляем с победой!')
			print_mess(gr_game)
			exit()
	if M[1][1] == marker and M[2][2] == marker and M[3][3] == marker:
		print(f'\n{gamer}, поздравляем с победой!')
		print_mess(gr_game)
		exit()
	elif M[1][3] == marker and M[2][2] == marker and M[3][1] == marker:
		print(f'\n{gamer}, поздравляем с победой!')
		print_mess(gr_game)
		exit()

# 7. Основной код игры:
g_start()
print('Ваше игровое поле:')
printM()
while True:
	if count < 10 and count % 2 != 0:
		print(f'------------------------\nХод номер {count}')
		gamer = G1
		figure = 'крестика'
		marker = 'х'
		coord_input()
		win_check()
		count += 1
	if count < 10 and count % 2 == 0:
		print(f'------------------------\nХод номер {count}')
		gamer = G2
		figure = 'нолика'
		marker = 'о'
		coord_input()
		win_check()
		count += 1
	else:
		print('\nНичья!\n')
		print_mess(gr_game)
		break


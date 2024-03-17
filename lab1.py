com_sign_op = '{'
com_sign_cl = '}'
counter1 = 0
counter2 = 0
com_str = '/'

with open('Lab1.txt', 'r') as file:
    # Читаем файл посимвольно
    while True:
        char = file.read(1)
        # Если встречаем открывающую фигурную скобку, переключаем флаг
        if char == com_sign_op:
            counter1 += 1
        # Если встречаем закрывающую фигурную скобку, сбрасываем флаг
        elif char == com_sign_cl:
            counter1 -= 1
        elif char == com_str:
            counter2 += 1
        elif char == '\n' and counter2 != 0:
            counter2 -= 1

        # Если не внутри фигурных скобок, выводим символ
        elif counter1 == 0 and counter2 == 0:
            print(char, end='')
        # Если достигнут конец файла, выходим из цикла
        if not char:
            break

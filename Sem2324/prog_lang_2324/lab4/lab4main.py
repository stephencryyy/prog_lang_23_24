import struct
import sys
import traceback
import copy
class interpreter:
    def __init__(self, base_input=10, base_output=10, base_assign=10, debug='off'):
        self.variables = {}

        self.commands_binary = {'and': [], 'mult': [], 'or': [], 'xor': [], 'add': [],
                                'sub': [], 'div': [], 'rem': []}
        self.commands_unary = {'not': [], 'input': [], 'output': []}

        self.base_input = base_input
        self.base_output = base_output
        self.base_assign = base_assign
        self.debug = debug

    def assign(self, var_name, value):
        try:
            # Convert value to base 10
            value_base_10 = int(value, self.base_assign)
            self.variables[var_name] = value_base_10
            print(f"Assigned {value_base_10} to variable {var_name}")
        except ValueError:
            print(traceback.format_exc())

    def input(self, var_name):
        try:
            value = input(f"Enter value for {var_name}: ")
            # Convert input value to base 10
            value_base_10 = int(value, self.base_input)
            self.variables[var_name] = value_base_10
            print(f"Assigned {value_base_10} to variable {var_name}")
        except ValueError:
            print(traceback.format_exc())

    def execute_unary(self, command, argument):
        if command == "not":
            return self.bitwise_not(argument)
        elif command == "input":
            return self.input(argument)
        elif command == "output":
            return self.output_value(argument)
        else:
            self.execute_binary(command, argument)

    def execute_binary(self, command, arguments):
        try:
            com = command
            arg = arguments.split(',')
            for i, m in self.commands_binary.items():
                if command in m:
                    com = i
                else:
                    for ke, val in self.commands_unary.items():
                        if command in val:
                            com = ke

            if len(arg) == 2:
                for i in range(len(arg)):
                    if arg[i] in self.variables:
                        arg[i] = self.variables[arg[i]]
                if command == 'add' or com == 'add':
                    p = self.poland_notation(f'{arg[0]}+{arg[1]}')
                    return self.calc(p)
                elif command == 'mult' or com == 'mult':
                    p = self.poland_notation(f'{arg[0]}*{arg[1]}')
                    return self.calc(p)
                elif command == 'sub' or com == 'sub':
                    p = self.poland_notation(f'{arg[0]}-{arg[1]}')
                    return self.calc(p)
                elif command == 'div' or com == 'div':
                    p = self.poland_notation(f'{arg[0]}${arg[1]}')
                    return self.calc(p)
                elif command == 'rem' or com == 'rem':
                    p = self.poland_notation(f'{arg[0]}%{arg[1]}')
                    return self.calc(p)
                elif command == 'pow' or com == 'pow':
                    p = self.poland_notation(f'{arg[0]}^{arg[1]}')
                    return self.calc(p)
                elif command == 'xor' or command == 'and' or command == 'or' or com in ['and', 'or', 'xor']:
                    if com in ['and', 'or', 'xor']:
                        return self.logic_operations(com, arg[0], arg[1])
                    return self.logic_operations(command, arg[0], arg[1])

            else:
                raise Exception("Invalid operation, incorrect number of args")

        except Exception:
            print(traceback.format_exc())



    def logic_operations(self, command, a, b):
        try:
            abin = f'{bin(int(a))[2:]}'
            bbin = f'{bin(int(b))[2:]}'

            if len(abin) != len(bbin):
                if len(abin) > len(bbin):
                    while len(abin) > len(bbin):
                        bbin = '0' + bbin
                if len(bbin) > len(abin):
                    while len(bbin) > len(abin):
                        abin = '0' + abin
            if command == 'xor':
                xor = ''
                for i in range(len(abin)):
                    if abin[i] == bbin[i]:
                        xor += '0'
                    else:
                        xor += '1'
                return int(xor, 2)
            if command == 'and':
                and_op = ''
                for i in range(len(abin)):
                    if abin[i] == bbin[i]:
                       and_op += '0' if abin[i] == 0 else '1'
                    else:
                        and_op += '0'
                return int(and_op, 2)
            if command == 'or':
                or_op = ''
                for i in range(len(abin)):
                    if abin[i] == 0 and bbin[i] == 0:
                        or_op += '0'
                    else:
                        or_op += '1'
                return int(or_op, 2)

        except:
            print(traceback.format_exc())
    def poland_notation(self, string) -> list:
        try:
            str_ = ''
            out = []
            stack = []
            for i in range(len(string)):
                if string[i].isalnum() or string[i] == '.':
                    str_ += string[i]
                else:
                    if str_ != '':
                        out.append(str_)
                        str_ = ''
                    if string[i] == '(':
                        stack.append('(')
                    elif string[i] == ')':
                        while stack[-1] != '(':
                            out.append(stack.pop())
                        stack.pop()
                    elif string[i] in ['*', '/', '%', '$', '^']:
                        if stack and stack[-1] in ['*', '/', '%', '$', '^']:
                            out.append(stack.pop())
                        stack.append(string[i])
                    elif string[i] in ['+', '-']:
                        while stack and stack[-1] in ['*', '/', '+', '-', '%', '$', '^']:
                            out.append(stack.pop())
                        stack.append(string[i])

            if str_ != '':
                out.append(str_)

            while stack:
                out.append(stack.pop())

            return out

        except:
            print(traceback.format_exc())

    def is_float(self, s: str) -> bool:
        parts = s.split('.')
        if len(parts) != 2:
            return False  # Нет десятичной точки
        if not parts[0].isdigit() or not parts[1].isdigit():
            return False  # Целая или дробная часть не является числом
        return True

    def calc(self, string) -> float:
        try:
            stack = []
            for i in range(len(string)):
                if string[i].isdigit() or self.is_float(string[i]):
                    stack.append(float(string[i]))
                elif string[i] == '+':
                    stack.append(stack.pop() + stack.pop())
                elif string[i] == '-':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x2 - x1)
                elif string[i] == '*':
                    stack.append(stack.pop() * stack.pop())
                elif string[i] == '/':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x2 / x1)
                elif string[i] == '^':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x2 ** x1)
                elif string[i] == '%':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x2 % x1)
                elif string[i] == '$':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x2 // x1)

            return stack.pop()
        except Exception as e:
            print(f'Error: {e}')


    def output_value(self, arg):
        if arg in self.variables:
            val = self.convert_integer(int(self.variables[arg]),self.base_output)
            print(val)
            
        else:
            val = self.convert_integer(int(arg), self.base_output)
            print(val)

    def convert_integer(self, dec, radix):
        if radix > 36:
            return 'Основание системы счисления должно быть не больше 36-ти'

        number = ''
        while dec > 0:
            dec, remainder = divmod(dec, radix)
            if remainder > 9:
                remainder = chr(ord('A') + remainder - 10)
            number = str(remainder) + number
        return number

    def bitwise_not(self, number):
        # Преобразуем число в двоичную строку
        binary_str = bin(number)[2:]

        # Создаем пустую строку для результата
        result_str = ''

        # Проходим по каждому биту в двоичной строке
        for bit in binary_str:
            # Меняем 0 на 1 и 1 на 0
            if bit == '0':
                result_str += '1'
            else:
                result_str += '0'

        # Преобразуем результат обратно в число
        result = int(result_str, 2)

        return result

    def interactive_mode(self):
        while True:
            print("Debug mode. Choose an action:")
            print("1. Print variable")
            print("2. Print all variables")
            print("3. Change variable value")
            print("4. Declare a new variable")
            print("5. Undefine a variable")
            print("6. Continue execution")
            print("7. Exit interpreter")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.print_variable()
            elif choice == "2":
                self.print_all_variables()
            elif choice == "3":
                self.change_variable_value()
            elif choice == "4":
                self.declare_new_variable()
            elif choice == "5":
                self.undefine_variable()
            elif choice == "6":
                break
            elif choice == "7":
                sys.exit(0)

    def print_variable(self):
        name = input("Enter variable name: ").strip()
        if name in self.variables:
            value = self.variables[name]
            print(
                f"{name} = {value} (hex: {hex(value)}, bin: {' '.join(format(byte, '08b') for byte in struct.pack('>I', value))})")
        else:
            print(f"Variable {name} not found")

    def print_all_variables(self):
        for var, value in self.variables.items():
            print(f"{var} = {value}")

    def change_variable_value(self):
        name = input("Enter variable name: ").strip()
        if name in self.variables:
            value = int(input("Enter new value (hex): ").strip(), 16)
            self.variables[name] = value
        else:
            print(f"Variable {name} not found")

    def declare_new_variable(self):
        name = input("Enter new variable name: ").strip()
        if name in self.variables:
            print(f"Variable {name} already exists")
            return
        value = self.read_special_number()
        self.variables[name] = value

    def read_special_number(self):
        print("Choose number format:")
        print("1. Zeckendorf representation")
        print("2. Roman numerals")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            return self.read_zeckendorf()
        elif choice == "2":
            return self.read_roman()
        else:
            print("Invalid choice")
            return self.read_special_number()

    def read_zeckendorf(self):
        zeckendorf = input("Enter Zeckendorf representation: ").strip()
        fibonacci = [1, 2]
        while fibonacci[-1] < 1 << 32:
            fibonacci.append(fibonacci[-1] + fibonacci[-2])
        return sum(fibonacci[i] for i, char in enumerate(reversed(zeckendorf)) if char == '1')

    def read_roman(self):
        roman = input("Enter Roman numerals: ").strip().upper()
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        value = 0
        prev = 0
        for char in reversed(roman):
            curr = roman_map[char]
            if curr >= prev:
                value += curr
            else:
                value -= curr
            prev = curr
        return value

    def undefine_variable(self):
        name = input("Enter variable name: ").strip()
        if name in self.variables:
            del self.variables[name]
        else:
            print(f"Variable {name} not found")
    def run(self, options_name, filename):
        try:
            stack = 0
            l_or_r = 0
            op = 0
            if filename:
                with open(options_name, "r") as o:
                    for line in o:

                        line1 = ''
                        for symbol in line:
                            if symbol == '[':
                                stack += 1
                            elif symbol == ']':
                                stack -= 1
                            elif symbol == '#':
                                break
                            if stack == 0:
                                line1 += symbol

                        if '()op' in line1: op = 1
                        elif 'op()' in line1: op = 0
                        elif '(op)' in line1: op = 2
                        elif 'right=' in line1: l_or_r = 1
                        elif 'left=' in line1:  l_or_r = 0
                        elif line1.split(' ')[0] in self.commands_binary:
                            args = line1.split(' ')
                            self.commands_binary[args[0]].append(args[1].strip())
                        elif line1.split(' ')[0] in self.commands_unary:
                            args = line1.split(' ')
                            self.commands_unary[args[0]].append(args[1].strip())

    
                        else:
                            print(traceback.format_exc())
    
                    with open(filename) as f:
                        for line1 in f:
                            line = ''
                            for symbol in line1:
                                if symbol == '[':
                                    stack += 1
                                elif symbol == ']':
                                    stack -= 1
                                elif symbol == '#':
                                    break
                                if stack == 0:
                                    line += symbol

                            line = line.strip().split(';')
                            for n, v in self.commands_unary.items():
                                syn = '$##'
                                if len(v)>0:
                                    syn = v[0]
                                if line[0].startswith(n) or line[0].startswith(syn):
                                    arg = 0
                                    if op == 0:
                                        string = line[0].split('(')
                                        arg = string[1].split(')')[0]
                                    else:
                                        string = line[0].split(')')
                                        arg = string[0].strip('(')
                                    self.execute_unary(n, arg)

                            if '=' in line[0]:
                                res1 = 'a'
                                res2 = 'b'
                                string = line[0].split('=')
                                arg = string[1] if l_or_r == 0 else string[0]
                                operand = string[0] if l_or_r == 0 else string[1]
                                com = ''
                                for i, m in self.commands_binary.items():
                                    if op == 0:
                                        if arg.split('(')[0] in m:
                                            com = i
                                    else:
                                        if arg.split(')')[1] in m:
                                            com = i
                                for i, m in self.commands_unary.items():
                                    if op == 0:
                                        if arg.split('(')[0] in m:
                                            com = i
                                    else:
                                        if arg.split(')')[1] in m:
                                            com = i

                                if len(com) == 0: com = arg.split('(')[0] if op == 0 else arg.split(')')[1]

                                if com in self.commands_binary:
                                    if op == 0:
                                        arg = arg.split('(')
                                        command = arg[1] if len(arg[1].split(',')) < 2 else arg[1].split(',')[1]

                                        for i, m in self.commands_binary.items():
                                            if command in m:
                                                command = i
                                            else:
                                                for n, v in self.commands_unary.items():
                                                    if command in v:
                                                        command = n

                                        if command in self.commands_binary or command in self.commands_unary:
                                            arguments = arg[2].split(')')[0].split(',') if len(arg[2].split(')')[0]) > 1 else arg[2].split(')')[0]
                                            if arg[2].replace(',','').split(')')[1] in self.commands_binary or arg[2].split(')')[1] in self.commands_unary:
                                                command2 = arg[2].replace(',','').split(')')[1]
                                                arguments2 = arg[3].split(')')[0].split(',')
                                                for num, ar in enumerate(arguments2):
                                                    if ar in self.variables:
                                                        arguments2[num] = str(self.variables[ar])
                                                res1 = self.execute_binary(command2, f'{arguments2[0]},{arguments2[1]}') if command2 in self.commands_binary else self.execute_unary(command2, arguments2[0])
                                            for n,a in enumerate(arguments):
                                                if a in self.variables:
                                                    arguments[n] = str(self.variables[a])
                                            res2 = self.execute_binary(command, f'{arguments[0]},{arguments[1]}') if command in self.commands_binary else self.execute_unary(command, int(arguments[0]))
                                            if res1 == 'a':
                                                if command in self.commands_binary:
                                                    res1 = arg[2].split(',')[2].replace(')','')
                                                else:
                                                    res1 = arg[2].replace(')','').split(',')[1] if len(arg[1].split(',')) < 2 else arg[1].split(',')[0]
                                        args = arg[1].strip(')').split(',') if res1 =='a' and res2 == 'b' else [res1, res2]
                                    else:
                                        arg = arg.split(')')
                                        args = arg[0].strip('(').split(',')
                                    for i in range(len(args)):
                                        if args[i] in self.variables:
                                            args[i] = self.variables[args[i]]
                                    self.variables[operand] = self.execute_binary(arg[0], f'{args[0]},{args[1]}') if op == 0 else self.execute_binary(arg[1], f'{args[0]},{args[1]}')
                                elif com in self.commands_unary:
                                    args = arg.split('(')
                                    self.variables[operand] = self.execute_unary(args[0], args[1].strip(')'))
                                else:
                                    self.assign(operand, arg)
                            elif line[0].startswith('BREAKPOINT') and self.debug in {'--debug','-d', '/debug'}:
                                self.interactive_mode()
                                continue

                                        
                                
        except Exception:
            print(traceback.format_exc())

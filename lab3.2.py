
class interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def assign(self, name, value):
        self.variables[name] = value

    def define(self, name, params, body):
        self.functions[name] = {params: body}

    def execute(self, name, params):
        if name in self.functions:
            function_info = self.functions[name]
            keys = ','.join(function_info.keys())
            values = ''.join(function_info.values())

            # Если params - это число, создаем из него список
            if not isinstance(params, list):
                params = [params]

            for i in range(len(params)):
                try:
                    if params[i].split('(')[0] in self.functions:
                        func = self.functions[params[i].split('(')[0]]
                        keys1 = ','.join(func.keys())
                        values1 = ','.join(func.values())

                        if not isinstance(params, list):
                            params = [params]
                        try:
                            param = params[i].split('(')[1].split(')')

                            parameters = dict(zip(keys1.split(','), param[0].split(',')))
                        except:
                            param = params[i+1]
                            parameters = dict(zip(keys1.split(','), param.split(',')))

                        for val in parameters.values():
                            if val in self.variables:
                                for k, valu in parameters.items():
                                    if valu == val:
                                        values1 = values1.replace(k, str(self.variables[val]))
                        params = params[0].split(',')
                        for i in range(len(params)):
                            if params[i].split('(')[0] in self.functions:
                                params[i] = self.calc(self.poland_notation(values1))
                except:
                    continue

            parameters = dict(zip(keys.split(','), params))

            for param, value in parameters.items():
                values = values.replace(param, str(value))
            return self.calc(self.poland_notation(values))

    def poland_notation(self, string):
        try:
            out = []
            stack = []
            for i in range(len(string)):
                if string[i].isalpha() or string[i].isdigit():
                    out.append(string[i])
                elif string[i] == '(':
                    stack.append('(')
                elif string[i] == ')':
                    while stack[-1] != '(':
                        out.append(stack.pop())
                    stack.pop()
                elif string[i] == '*' or string[i] == '/':
                    if len(stack) > 0:
                        if stack[-1] == '*' or stack[-1] == '/':
                            out.append(stack.pop())
                            stack.append(string[i])
                        else:
                            stack.append(string[i])
                    else:
                        stack.append(string[i])

                elif string[i] == '+' or string[i] == '-':
                    while len(stack) > 0 and stack[-1] != '(':
                        out.append(stack.pop())
                    stack.append(string[i])

            if len(stack) > 0:
                for i in range(len(stack)):
                    out.append(stack.pop())


            return ''.join(out)

        except Exception as e:
            print('Exception is ', e)


    def calc(self, string) -> int:
        try:
            stack = []
            for i in range(len(string)):
                if string[i].isdigit():
                    stack.append(int(string[i]))
                elif string[i] == '+':
                    stack.append(stack.pop() + stack.pop())
                elif string[i] == '-':
                    stack.append(-stack.pop() + stack.pop())
                elif string[i] == '*':
                    stack.append(stack.pop() * stack.pop())
                elif string[i] == '/':
                    stack.append(stack.pop() / stack.pop())

            return stack[-1]
        except Exception as e:
            print(f'Error: {e}')

    def parce(self, filename):
        if filename:
            with open(filename) as f:
                for line in f:
                    line = line.strip().split(';')
                    if '=' in line[0]:
                        new_line = line[0].split('=')
                        self.assign(new_line[0].split('(')[0], new_line[1])
                    elif ':' in line[0]:
                        new_line = line[0].split(':')
                        function_info = new_line[0].split('(')
                        function = function_info[0]
                        arguments = function_info[1].strip(')')
                        func_body = new_line[1]
                        self.define(function, arguments, func_body)

                    elif 'print' in line[0]:
                        for key, value in self.variables.items():
                            try:
                                if value.split('(')[0] in self.functions.keys():
                                    args = value.strip(')').split('(')
                                    self.variables[key] = self.execute(args[0], [args[i] for i in range(1, len(args))])

                                elif '+' in value or '-' in value or '*' in value or '/' in value:
                                    self.variables[key] = self.calc(self.poland_notation(value))

                            except Exception as e:
                                print(f'Error: {e}')
                        print(self.variables, self.functions)


        else:
            raise Exception('No filename provided')





inter = interpreter()

inter.parce('lab3.2.txt')
print(inter.calc(inter.poland_notation('(2+4+5)*4-5')))

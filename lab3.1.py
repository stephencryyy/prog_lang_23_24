class Scope:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def SetVar(self, name, value):
        self.vars[name] = value

    def GetVar(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent is not None:
            return self.parent.GetVar(name)
        else:
            raise Exception("Variable " + name + " not found")

    def ShowVar(self):
        print(self.vars)

    def interpreter(self, filename):
        global_scope = Scope()
        current_scope = global_scope
        scope_stack = [global_scope]

        with open(filename) as f:
            if f:
                for line in f:
                    line = line.strip().split(";")
                    for command in line:
                        if command == "{":
                            new_scope = Scope(current_scope)
                            scope_stack.append(new_scope)
                            current_scope = new_scope
                        elif command == "}":
                            current_scope = scope_stack.pop()
                            current_scope = scope_stack[-1]
                        elif command == 'ShowVar':
                            current_scope.ShowVar()
                        elif '=' in command:
                            var, value = command.split('=')
                            current_scope.SetVar(var.strip(), value.strip())
            else:
                raise Exception("File not found")


inter = Scope()
inter.interpreter("lab3.txt")

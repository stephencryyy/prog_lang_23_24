import numpy as np
from scipy import stats
import random

class ArrayInterpreter:
    def __init__(self):
        self.arrays = {}

    def load_array(self, name, filename):
        try:
            with open(filename, 'r') as f:
                data = f.read()
                data1 = list(data)
                arr = [x for x in data1 if x.isdigit()]
                self.arrays[name] = arr
                print(f"Array {name} loaded")
        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error {e}")

    def print_array(self, name):
        if name in self.arrays:
            print(f'Array {name}: {self.arrays[name]}')
        else:
            print(f'Array {name} not found')

    def save_array(self, name, filename):
        if name in self.arrays:
            try:
                with open(filename, 'w') as f:
                    for i in self.arrays[name]:
                        f.write(str(i) + ' ')
                    print(f'Array {name} saved to {filename}\n')
            except FileNotFoundError:
                print(f"File {filename} not found")
            except Exception as e:
                print(f"Error {e}")
        else: print(f'Array {name} not found')

    def rand(self, name, count, lb, rb):
        if name in self.arrays:
            try:
                for _ in range(count):
                    self.arrays[name].append(str(random.randint(lb,rb)))
                print(f'Array {name} filed successfully\n')
            except Exception as e:
                print(f"Error {e}")
        else: print(f'Array {name} not found')

    def concatenate(self, name1, name2):
        if name1 in self.arrays and name2 in self.arrays:
            try:
                self.arrays[name1] = np.concatenate((self.arrays[name1], self.arrays[name2]))
                print(f'Array {name1} and {name2} concatenated successfully\n')
            except Exception as e:
                print(f"Error {e}")
        elif name1 not in self.arrays:
            print(f"Array {name1} not found")
        elif name2 not in self.arrays:
            print(f"Array {name2} not found")

    def free(self, name):

        if name in self.arrays:
            try:
                for i in range(len(self.arrays[name])):
                    self.arrays[name][i] = 0
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name} not found")

    def remove(self, name, a, count):
        if name in self.arrays:
            try:
                del self.arrays[name][a:a+count]
                print(f'Removed {count} elements from index {a} in array {name}\n')
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name} not found")

    def copy(self, name1, a, b, name2):
        if name1 in self.arrays and name2 in self.arrays:
            try:
                self.arrays[name2].extend(self.arrays[name1][a : b+1])
                print(f'Copied elements from index {a} to {b} from array {name1} to array {name2}\n')
            except Exception as e:
                print(f"Error {e}")
        elif name1 not in self.arrays:
            print(f"Array {name1} not found")
        elif name2 not in self.arrays:
            print(f"Array {name2} not found")

    def sort_up(self, name1):
        if name1 in self.arrays:
            try:
                self.arrays[name1].sort()
                print(f'Array {name1} sorted in ascending')
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

    def sort_down(self, name1):
        if name1 in self.arrays:
            try:
                self.arrays[name1].sort(reverse=True)
                print(f'Array {name1} sorted in descending')
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

    def shuffle(self, name1):
        if name1 in self.arrays:
            try:
                random.shuffle(self.arrays[name1])
                print(f'Array {name1} is shuffled')
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

    def stats(self, name1):
        if name1 in self.arrays:
            try:
                array = np.array(self.arrays[name1], dtype=float)  # Преобразуем строки в числа
                mean = np.mean(array)
                median = np.median(array)
                std_deviation = np.std(array)
                length = np.size(array)
                max_val = array.max()
                min_val = array.min()
                index_min, index_max = np.argmin(array), np.argmax(array)
                mode = stats.mode(array)
                arr = np.abs(array - mean)
                max_deviation = np.max(arr)
                print(
                    f"Information about array {name1}:\n mean: {mean}, median: {median}, max element: {max_val}, min element: {min_val}, "
                    f"std deviation: {std_deviation}, length: {length}, index of min: {index_min}, index of max: {index_max}, mode is {mode}, max deviation: {max_deviation}")
            except Exception as e:
                print(f"Error {e}")
            except RuntimeWarning as run:
                print(f"Error {run}")
        else:
            print(f"Array {name1} not found")

    def print_stats(self, name1, a):
        if name1 in self.arrays:
            try:
                print(self.arrays[name1][a])
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

    def print_stats2(self, name1, a, b):
        if name1 in self.arrays:
            try:
                print(self.arrays[name1][a:b+1])
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

    def print_all(self, name1):
        if name1 in self.arrays:
            try:
                print(self.arrays[name1])
            except Exception as e:
                print(f"Error {e}")
        else:
            print(f"Array {name1} not found")

intepreter = ArrayInterpreter()

intepreter.load_array("A", "scratch.txt")
intepreter.load_array("B", "scratch.txt")
intepreter.shuffle("B")
intepreter.print_all("A")
intepreter.print_all("B")
intepreter.concatenate("A", "B")
intepreter.print_all("A")
intepreter.save_array("B", "scratch.txt")
intepreter.rand("B", 8, 2, 9)
intepreter.print_all("B")
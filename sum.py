def solve(int a, int b):
    return a / b


try:    
    print(solve(5, 0))
except ZeroDivisionError:
    print('Cant devide by zero')
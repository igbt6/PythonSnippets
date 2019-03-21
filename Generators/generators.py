#!/usr/bin/env/python3



#1# - function generator
def all_divisible_by_7(n):
    for i in range(n):
        if i % 7 == 0:
            yield i



###################### main ####################
if __name__ == '__main__':

##1# - function generator
    for num in all_divisible_by_7(100000000):
        print(num, end=', ')
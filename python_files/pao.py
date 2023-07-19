import numpy as np
from datetime import datetime as dt
import random as rd
import math
import sys

table = np.genfromtxt("/home/simon/.shell_files/input_files/pao.csv", delimiter=',', dtype= str)[:,1:]
BLD = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

def get_seconds(time):
    time_digits = list(str(time))
    return int(time_digits[0])*60*60+int(time_digits[2])*10*60+int(time_digits[3])*60+int(time_digits[5])*10+int(time_digits[6])+int(time_digits[8])*0.1+int(time_digits[9])*0.01

def average(values):
    length = len(values)
    number = math.ceil(0.05*length)
    if length <= 2:
        return "To short for an average."
    values.sort()
    for i in range(number):
        values.pop(-1)
    for i in range(number):
        values.pop(0)
    return round(sum(values)/len(values),2)

def ask_rows(column_start = "A", column_end = "X"):
    i = 1
    total = 0
    total_2 = 1
    times = []
    ask_BLD = BLD[BLD.index(column_start):BLD.index(column_end)+1]
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        while i>0:
            if i != 1:
                for j in range(3):
                    print(table[4*n1+j+1, n2])
                print(" ")
            if total_2 == total:
                stop = dt.now()
                print("In", round(get_seconds(stop-start),2), "seconds.\n")
                total_2 += 1
                times.append(round(get_seconds(stop-start),2))
            i = len(inp)
            if i != 0:
                break
            i = 2
            l1 = rd.choice(ask_BLD)
            l2 = rd.choice(BLD)
            n1 = BLD.index(l1)
            n2 = BLD.index(l2)
            pair = l1 + l2
            start = dt.now()
            print(pair)
            total += 1
            inp = input()
    else: return print("Attempt aborted!")
    stop_global = dt.now()
    print("You reviewd", total, "pairs.")
    print("You took", str(stop_global-start_global) + ".")
    print("Average of", len(times), "is", average(times), "seconds.")

def ask_columns(column_start = "A", column_end = "X"):
    i = 1
    total = 0
    total_2 = 1
    times = []
    ask_BLD = BLD[BLD.index(column_start):BLD.index(column_end)+1]
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        while i>0:
            if i != 1:
                for j in range(3):
                    print(table[4*n1+j+1, n2])
                print(" ")
            if total_2 == total:
                stop = dt.now()
                print("In", round(get_seconds(stop-start),2), "seconds.\n")
                total_2 += 1
                times.append(round(get_seconds(stop-start),2))
            i = len(inp)
            if i != 0:
                break
            i = 2
            l1 = rd.choice(BLD)
            l2 = rd.choice(ask_BLD)
            n1 = BLD.index(l1)
            n2 = BLD.index(l2)
            pair = l1 + l2
            start = dt.now()
            print(pair)
            total += 1
            inp = input()
    else: return print("Attempt aborted!")
    stop_global = dt.now()
    print("You reviewd", total, "pairs.")
    print("You took", str(stop_global-start_global) + ".")
    print("Average of", len(times), "is", average(times), "seconds.")

def ask_pao(start, end, line):
    if start == "A" and end == "X":
        return ask_columns(start, end)
    if line == "c":
        return ask_columns(start, end)
    elif line == "r":
        return ask_rows(start, end)
    else: help()

def help():
    print("""Arguments must be passed in the order as shown:    [letter_1] [letter_2] [column/row]
             - [letter_1] is a char in BLD (default=A).
             - [letter_2] is a char in BLD (default=X).
             - [column/row] is a char in {c,r} (default=c).""")

if(len(sys.argv) == 4 and sys.argv[1] in BLD and sys.argv[2] in BLD and sys.argv[3] in ["c", "r"]):
    ask_pao(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    help()


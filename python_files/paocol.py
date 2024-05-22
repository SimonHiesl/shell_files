import numpy as np
from datetime import datetime as dt
import random as rd
import math
import sys

table = np.genfromtxt("/home/hiesl/shell_files/input_files/pao.csv", delimiter=',', dtype= str)[:,1:]
BLD = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

def get_seconds(time):
    time_digits = list(str(time))
    return int(time_digits[0])*60*60+int(time_digits[2])*10*60+int(time_digits[3])*60+int(time_digits[5])*10+int(time_digits[6])+int(time_digits[8])*0.1+int(time_digits[9])*0.01

def get_minutes(time):
    time_digits = list(str(time))
    if time_digits[5] == "1" and time_digits[2] == "0":
        return time_digits[3] + " minute and " + time_digits[5] + time_digits[6] + " seconds"
    elif time_digits[2] == "0":
        return time_digits[3] + " minutes and " + time_digits[5] + time_digits[6] + " seconds"
    else:
        return time_digits[2] + time_digits[3] + " minutes and " + time_digits[5] + time_digits[6] + " seconds"

def count_list(lst, x):
    count = 0
    for ele in lst:
        if ele == x:
            count += 1
    return count

def average(values):
    length = len(values)
    number = math.ceil(0.05*length)
    num_dnf = count_list(values, "DNF")
    if num_dnf > number:
        return "DNF"
    if len(values) <= 2:
        return "To short for average."
    num_bad = number - num_dnf
    for i in range(num_dnf):
        values.remove("DNF")
    values.sort()
    for i in range(num_bad):
        values.pop(-1)
    for i in range(number):
        values.pop(0)
    return round(sum(values)/len(values),2)

def get_column(letter):
    column = []
    for i in range(23):
        column.append(BLD[i]+str(letter))
    rd.shuffle(column)
    return column

def ask_pao(letter):
    ask_column = get_column(letter)
    times = []
    total = 0
    dnf_count = 0
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        for i in range(23):
            print(ask_column[i])
            start = dt.now()
            total += 1
            inp = input()
            stop = dt.now()
            time = round(get_seconds(stop-start),2)
            if len(inp) != 0 and inp != "n":
                for j in range(3):
                    print(str(table[4*BLD.index(ask_column[i][0])+j+1, BLD.index(str(letter))]))
                print(" ")
                break
            if inp == "n" or time >= 15.0:
                for j in range(3):
                    print("\033[31m" + str(table[4*BLD.index(ask_column[i][0])+j+1, BLD.index(str(letter))]) + "\033[0m")
                dnf_count += 1
                times.append("DNF")
            elif time >= 10.0:
                for j in range(3):
                    print("\033[33m" + str(table[4*BLD.index(ask_column[i][0])+j+1, BLD.index(str(letter))]) + "\033[0m")
                times.append(time)
            else:
                for j in range(3):
                    print("\033[32m" + str(table[4*BLD.index(ask_column[i][0])+j+1, BLD.index(str(letter))]) + "\033[0m")
                times.append(time)
            print(" ")
            print("In", time, "seconds.\n")
    else: return print("Attempt aborted!")
    stop_global = dt.now()
    print("You reviewed", total, "pairs and got", total-dnf_count, "correct.")
    print("You took " + get_minutes(stop_global-start_global) + ".")
    if average(times) == "DNF":
        print("The average is a DNF!")
    elif average(times) == "To short for average.":
        print("To short for average.")
    else:
        print("Average of", total, "is", average(times), "seconds.")

def help():
    print("""Arguments must be passed in the order as shown:    [letter]
             - [letter] is a char in BLD (default=A).""")

if(len(sys.argv) == 2 and sys.argv[1] in BLD):
    ask_pao(sys.argv[1])
else:
    help()

import numpy as np
from datetime import datetime as dt
import random as rd
import math
import sys

table = np.genfromtxt("/home/simon/.shell_files/input_files/pao.csv", delimiter=',', dtype= str)[:,1:]
BLD = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

def save_list_to_txt(input_list):
    with open("/home/simon/.shell_files/input_files/incorrect_pao.txt", 'a') as file:
        for item in input_list:
            file.write(str(item) + '\n')

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

def ask_rows(column_start, column_end, max_attempts):
    total = 0
    dnf_count = 0
    times = []
    incorrect = []
    ask_BLD = BLD[BLD.index(column_start):BLD.index(column_end)+1]
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        for i in range(max_attempts):
            lp1 = rd.choice(ask_BLD)
            lp2 = rd.choice(BLD)
            n1 = BLD.index(lp1)
            n2 = BLD.index(lp2)
            pair = lp1 + lp2
            print(pair)
            start = dt.now()
            inp = input()
            stop = dt.now()
            total += 1
            time = round(get_seconds(stop-start),2)
            if len(inp) != 0 and inp != "n":
                for j in range(3):
                    print(str(table[4*n1+j+1, n2]))
                print(" ")
                break
            if inp == "n" or time >= 15.0:
                for j in range(3):
                    print("\033[31m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                dnf_count += 1
                times.append("DNF")
                incorrect.appen(pair)
            elif time >= 10.0:
                for j in range(3):
                    print("\033[33m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                times.append(time)
            else:
                for j in range(3):
                    print("\033[32m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                times.append(time)
            print(" ")
            print("In", round(get_seconds(stop-start),2), "seconds.\n")
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
    save_list_to_txt(incorrect)

def ask_columns(column_start, column_end, max_attempts):
    total = 0
    dnf_count = 0
    times = []
    incorrect = []
    ask_BLD = BLD[BLD.index(column_start):BLD.index(column_end)+1]
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        for i in range(max_attempts):
            lp1 = rd.choice(BLD)
            lp2 = rd.choice(ask_BLD)
            n1 = BLD.index(lp1)
            n2 = BLD.index(lp2)
            pair = lp1 + lp2
            print(pair)
            start = dt.now()
            inp = input()
            stop = dt.now()
            total += 1
            time = round(get_seconds(stop-start),2)
            if len(inp) != 0 and inp != "n":
                for j in range(3):
                    print(str(table[4*n1+j+1, n2]))
                print(" ")
                break
            if inp == "n" or time >= 15.0:
                for j in range(3):
                    print("\033[31m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                dnf_count += 1
                times.append("DNF")
                incorrect.append(pair)
            elif time >= 10.0:
                for j in range(3):
                    print("\033[33m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                times.append(time)
            else:
                for j in range(3):
                    print("\033[32m" + str(table[4*n1+j+1, n2]) + "\033[0m")
                times.append(time)
            print(" ")
            print("In", round(get_seconds(stop-start),2), "seconds.\n")
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
    save_list_to_txt(incorrect)

def ask_pao(start, end, max_attempts, line):
    if line == "c":
        return ask_columns(start, end, int(max_attempts))
    elif line == "r":
        return ask_rows(start, end, int(max_attempts))
    else: help()

def help():
    print("""Arguments must be passed in the order as shown:    [max_attempts] [letter_1] [letter_2] [column/row]
             - [max_attempts] is a int (default=100)
             - [letter_1] is a char in BLD (default=A).
             - [letter_2] is a char in BLD (default=X).
             - [column/row] is a char in {c,r} (default=c).""")

if(len(sys.argv) == 5 and sys.argv[1].isdigit() and sys.argv[2] in BLD and sys.argv[3] in BLD and sys.argv[4] in ["c", "r"]):
    ask_pao(sys.argv[2], sys.argv[3], sys.argv[1], sys.argv[4])
else:
    help()


import numpy as np
from datetime import datetime as dt
import random as rd
import math
import sys

table = np.genfromtxt("/home/hiesl/shell_files/input_files/pao.csv", delimiter=',', dtype= str)[:,1:]
BLD = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

def read_list_from_txt():
    output_list = []
    with open("/home/hiesl/shell_files/input_files/incorrect_pao.txt", 'r') as file:
        for line in file:
            output_list.append(line.strip())
    return output_list

def clear_txt_file():
    with open("/home/hiesl/shell_files/input_files/incorrect_pao.txt", 'w') as file:
        pass

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

def ask_incorrects():
    total = 0
    dnf_count = 0
    times = []
    inc_list = read_list_from_txt()
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        for i in range(len(inc_list)):
            pair = inc_list[i]
            n1 = BLD.index(pair[0])
            n2 = BLD.index(pair[1])
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
    clear_txt_file()

def help():
    print("""No arguments can be passed. This command just asks the incorrect pao pairs found in ~/.shell_files/input_files/incorrect_pao.txt.""")

if(len(sys.argv) == 1):
    ask_incorrects()
else:
    help()

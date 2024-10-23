from datetime import datetime as dt
import random as rd
import math
import sys
import csv

with open('/home/hiesl/shell_files/input_files/letterpairs.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    row = next(reader)

pairs = [(row[i], row[i+1]) for i in range(0, len(row), 2)]
rd.shuffle(pairs)

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
    for _ in range(num_dnf):
        values.remove("DNF")
    values.sort()
    for _ in range(num_bad):
        values.pop(-1)
    for _ in range(number):
        values.pop(0)
    return round(sum(values)/len(values),2)

def ask_pairs(max_attempts):
    total = 0
    dnf_count = 0
    times = []
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.now()
        for i in range(max_attempts):
            print(pairs[i][0])
            start = dt.now()
            inp = input()
            stop = dt.now()
            total += 1
            time = round(get_seconds(stop-start),2)
            if len(inp) != 0 and inp != "n":
                print(pairs[i][1])
                print(" ")
                break
            if inp == "n" or time >= 6.0:
                print("\033[31m" + pairs[i][1] + "\033[0m")
                dnf_count += 1
                times.append("DNF")
            elif time >= 3.0:
                print("\033[33m" + pairs[i][1] + "\033[0m")
                times.append(time)
            else:
                print("\033[32m" + pairs[i][1] + "\033[0m")
                times.append(time)
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

def help():
    print("""Arguments must be passed in the order as shown:    [max_attempts]
             - [max_attempts] is a int (default=378)""")

if(len(sys.argv) == 2 and sys.argv[1].isdigit()):
    ask_pairs(int(sys.argv[1]))
else:
    help()

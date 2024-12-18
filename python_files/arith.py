import random as rd
import datetime as dt
import math
import sys

def get_seconds(time):
    time_digits = list(str(time))
    return int(time_digits[0])*60*60+int(time_digits[2])*10*60+int(time_digits[3])*60+int(time_digits[5])*10+int(time_digits[6])+int(time_digits[8])*0.1+int(time_digits[9])*0.01

def calculate(a, b, operation):
    if operation == "x": return a*b
    if operation == "+": return a+b
    if operation == "-": return a-b
    if operation == "^": return a**b
    #if operation == "/": return a/b

def calculation(operation, digit_1, digit_2, max_attempts):
    d_1 = "1"
    d_2 = "1"
    if digit_1 != 1:
        for _ in range(digit_1-1):
            d_1 += "0"
    if digit_2 != 1:
        for _ in range(digit_2-1):
            d_2 += "0"
    d_1 = int(d_1)
    d_2 = int(d_2)
    if operation == "^":
        d_2 = digit_2
    i=1
    times = []
    print("Push ENTER to start the timer!")
    inp = input()
    if len(inp) == 0:
        start_global = dt.datetime.now()
        count = 0
        global_count = 0
        while i>0:
            a = rd.randint(d_1+1, d_1*10-1)
            if operation != "^":
                b = rd.randint(d_2+1, d_2*10-1)
            else:
                b = digit_2
            print(a, operation, b)
            start = dt.datetime.now()
            inp = input()
            try:
                int(inp)
            except:
                return print("Attempt abortet! The correct answer would have been:", str(calculate(a,b,operation))+".")
            if len(inp) == 0:
                break
            if int(inp) == calculate(a,b,operation):
                stop = dt.datetime.now()
                times.append(round(get_seconds(stop-start),2))
                count+=1
                global_count += 1
                print("Correct! You took", round(get_seconds(stop-start),2), "seconds.")
            else:
                stop = dt.datetime.now()
                times.append("DNF")
                global_count += 1
                print("Wrong! Answer:", str(calculate(a,b,operation))+".","You took", round(get_seconds(stop-start),2), "seconds.")
            if  global_count == max_attempts:
                break
        stop_global = dt.datetime.now()
        print("\n")
        print("You got", count, "of", global_count, "correct in", stop_global-start_global)
        if count != 0:
            print("Ratio:", round(get_seconds(stop_global-start_global)/count, 2))
            print("Average of", len(times), "is:", average(times))
    else: return print("Attempt aborted!")

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
    if len(values) < 2:
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

def help():
    print("""Arguments must be passed in the order as shown:    [operation] [digit_1] [digit_2] [attempts]
             - [operation] is a char in {+,-,x,^} (default=x).
             - [digit_1] is the number of digits (default=2).
             - [digit_2] is the number of digits (default=1).
             - [attempts] is the number of attempts (default=5).""")

if(len(sys.argv) == 5 and sys.argv[1] in ["+","-","x","^"] and sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit()):
    calculation(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
else:
    help()

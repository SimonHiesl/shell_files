from datetime import datetime as dt
import random as rd
import math
import sys
import csv

input_file = "/home/hiesl/shell_files/input_files/letterpairs.csv"
save_file = "/home/hiesl/shell_files/input_files/incorrect_letterpairs.txt"

WHITE = 37
RED = 31
GREEN = 32
YELLOW = 33

def ask_letterpairs(max_attempts):
    if not prompt_start():
        return print("Attempt aborted!")
    start_global = dt.now()
    total_pairs, dnf_count, times, incorrect = process_pairs(max_attempts)
    stop_global = dt.now()
    total_time = stop_global - start_global
    print_stats(total_pairs, dnf_count, times, total_time)
    save_list_to_txt(incorrect)

def prompt_start():
    print("Push ENTER to start the timer!")
    inp = input()
    return len(inp) == 0

def process_pairs(max_attempts):
    total_pairs, dnf_count = 0, 0
    times, incorrect = [], []
    for index in range(max_attempts):
        total_pairs += 1
        result = process_single_pair(index)
        if result is None:
            break
        dnf_count += result['dnf']
        times.append(result['time'])
        if result['incorrect']:
            incorrect.append(pairs[index][0])
    return total_pairs, dnf_count, times, incorrect

def process_single_pair(index):
    print(pairs[index][0])
    start = dt.now()
    inp = input()
    stop = dt.now()
    if inp and inp != "n":
        print_table(index, WHITE, 0)
        return None
    time = round(get_seconds(stop - start), 2)
    return evaluate_pair(index, time, inp)

def evaluate_pair(index, time, inp):
    if inp == "n" or time >= 7.0:
        print_table(index, RED, time)
        return {"time": "DNF", "dnf": 1, "incorrect": True}
    elif time >= 4.0:
        print_table(index, YELLOW, time)
        return {"time": time, "dnf": 0, "incorrect": False}
    else:
        print_table(index, GREEN, time)
        return {"time": time, "dnf": 0, "incorrect": False}

def print_table(index, color, time):
    print(f"\033[{color}m" + str(pairs[index][1]) + "\033[0m")
    print(f"In {time} seconds.\n")

def print_stats(total_pairs, dnf_count, times, total_time):
    print(f"You reviewed {total_pairs} pairs.")
    print(f"Of which {total_pairs-dnf_count} were correct.")
    print(f"You took {format_time(get_seconds(total_time))}.")
    avg = average(times)
    if avg == "DNF":
        print("The average is a DNF!")
    elif avg == "To short for average.":
        print("To short for average.")
    else:
        print("Average of", total_pairs, "is", avg, "seconds.")

def save_list_to_txt(input_list):
    with open(save_file, 'a') as file:
        rd.shuffle(input_list)
        for item in input_list:
            file.write(str(item) + '\n')

def get_seconds(time):
    digits = [int(c) for c in str(time) if c.isdigit()]
    seconds = (
        digits[0] * 3600 +
        digits[1] * 600 +
        digits[2] * 60 +
        digits[3] * 10 +
        digits[4] +
        digits[5] * 0.1 +
        digits[6] * 0.01
    )
    return seconds

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"

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
    return round(sum(values)/len(values), 2)

def help():
    print("""Arguments must be passed in the order as shown:    [max_attempts]
             - [max_attempts] is a int (default=378)""")

if __name__ == "__main__":
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
    pairs = [(row[i], row[i+1]) for i in range(0, len(row), 2)]
    rd.shuffle(pairs)

    if(len(sys.argv) == 2 and sys.argv[1].isdigit()):
        ask_letterpairs(int(sys.argv[1]))
    else:
        help()

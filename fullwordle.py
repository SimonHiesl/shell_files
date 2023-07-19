import numpy as np
import sys
import random as rd

words = np.genfromtxt("/home/simon/.shell_files/input_files/valid-wordle-words.txt", dtype=str)
#rd.shuffle(words)

def remove_letters(word_list, letter, pos):
    return [string for string in word_list if string[int(pos)] != str(letter)]

def green_letters(word_list, letter, pos):
    return [string for string in word_list if string[int(pos)] == str(letter)]

def yellow_letters(word_list, letter_to_include, pos):
    return [string for string in word_list if all(letter in string for letter in letter_to_include) and string[int(pos)] != str(letter_to_include)]

def find_doubles(word_list, letter, count):
    return [string for string in word_list if string.count(str(letter)) > count]

def remove_doubles(word_list, letter, count):
    return [string for string in word_list if string.count(str(letter)) <= count]

def a_word(word, color_encoding):
    global words
    temp_list = list(word)
    for j,i in enumerate(color_encoding):
        if i == 1:
            indices = [i for i in range(5) if temp_list[i] == word[j]]
            count_green = 0
            for index in indices:
                if color_encoding[index] == 2:
                    count_green += 1
            if count_green > 0:
                words = find_doubles(words, word[j], count_green)
            count_black = 0
            for index in indices:
                if color_encoding[index] == 0:
                    count_black += 1
            if count_black > 0:
                words = remove_doubles(words, word[j], count_black)
            words = yellow_letters(words, word[j], j)
        elif i == 2:
            words = green_letters(words, word[j], j)
        elif i == 0:
            if temp_list.count(word[j]) == 1:
                for n in range(5):
                    words = remove_letters(words, word[j], n)
            else:
                indices = [i for i in range(5) if temp_list[i] == word[j]]
                two_list = []
                for index in indices:
                    if color_encoding[index] == 2:
                        two_list.append(index)
                if two_list:
                    remove_indices = list(set(range(5)) - set(two_list))
                    for index in remove_indices:
                        words = remove_letters(words, word[j], index)
                else:
                    for m in indices:
                        words = remove_letters(words, word[m], m)
        else:
            help()

def wordle(word_list, enc_list):
    global words
    for i in range(len(word_list)):
        a_word(word_list[i], enc_list[i])
    return words

def make_word_list(input_string):
    word_list = []
    for i in range(len(input_string)//5):
        word_list.append(input_string[5*i:5*i+5])
    return word_list

def make_int_list(input_string):
    int_list = []
    for i in range(len(input_string)//5):
        sub_list = []
        for j in range(5):
            sub_list.append(int(input_string[5*i:5*i+5][j]))
        int_list.append(sub_list)
    return int_list

def check_word_list(input_string):
    try:
        make_word_list(input_string)
    except:
        return False
    else:
        return True

def check_int_list(input_string):
    try:
        make_int_list(input_string)
    except:
        return False
    else:
        return True

def order_words(word_list):
    word_unique_counts = {}
    for word in word_list:
        word_unique_counts[word] = len(set(word))
    ordered_words = sorted(word_list, key=lambda x: word_unique_counts[x])
    print("There are", len(word_list), "possible words:")
    return ordered_words[::-1]

def help():
    print("""Arguments must be passed in the order as shown:    [words] [pos]
             - [words] in string, no spaces (no default).
             - [pos] in string, no spaces, 0 for grey, 1 for yellow, 2 for green (no default).""")

if(len(sys.argv) == 3 and check_word_list(str(sys.argv[1])) and check_int_list(str(sys.argv[2]))):
    print(order_words(wordle(make_word_list(str(sys.argv[1])), make_int_list(str(sys.argv[2])))))
else:
    help()

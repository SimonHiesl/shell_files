import numpy as np
import sys

wordsstring = ''.join(np.genfromtxt("/home/simon/.shell_files/input_files/2309-wordle-words.txt", delimiter = " ", dtype=str))
full_words = np.genfromtxt("/home/simon/.shell_files/input_files/valid-wordle-words.txt", dtype=str)
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
green = []
yellow = []

def convert_string_to_list(string):
    substring_list = []
    for i in range(0, len(string), 5):
        substring = string[i:i+5]
        substring_list.append(substring)
    return substring_list

words = convert_string_to_list(wordsstring)

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

def gby(word_list, letter, count_green, pos):
    return [string for string in word_list if string.count(str(letter)) == count_green + 1 and string[int(pos)] != str(letter)]

def a_word(word, color_encoding):
    global words
    global green
    global yellow
    temp_list = list(word)
    veto_letter = ""
    for j,i in enumerate(color_encoding):
        if i == 1:
            yellow.append(temp_list[j])
            indices = [i for i in range(5) if temp_list[i] == word[j]]
            count_green = 0
            for index in indices:
                if color_encoding[index] == 2:
                    count_green += 1
            count_black = 0
            for index in indices:
                if color_encoding[index] == 0:
                    count_black += 1
            if count_green > 0 and not count_black > 0:
                words = find_doubles(words, word[j], count_green)
            elif count_black > 0 and not count_green > 0:
                words = remove_doubles(words, word[j], count_black)
            elif count_green > 0 and count_black > 0:
                veto_letter = word[j]
                for index in indices:
                    if color_encoding[index] != 2 and word[j] != temp_list[i]:
                        words = remove_letters(words, word[j], index)
                words = gby(words, word[j], count_green, j)
            words = yellow_letters(words, word[j], j)
        elif i == 2:
            words = green_letters(words, word[j], j)
            green.append(temp_list[j])
        elif i == 0:
            if temp_list.count(word[j]) == 1:
                for n in range(5):
                    words = remove_letters(words, word[j], n)
            else:
                if word[j] == veto_letter:
                    continue
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

def wordle(word_list, enc_list):
    global green
    global yellow
    green = []
    yellow = []
    for i in range(len(word_list)):
        a_word(word_list[i], enc_list[i])
    return words

def count_letters(word_list):
    words_string = ''.join(word_list)
    letter_counts = []
    for i in abc:
        letter_counts.append(words_string.count(i))
    letter_dict = {k: v for k, v in zip(abc, letter_counts)}
    return letter_dict

def find_word_impossible(word_list):
    global green
    global yellow
    letter_dict = count_letters(word_list)
    weigth_dict = {}
    for word in full_words:
        count = 0
        if len(set(word)) == 5:
            for letter in word:
                if letter in green:
                    count -= 50
                if letter in yellow:
                    count -= 10
                else:
                    count += letter_dict.get(letter)
        weigth_dict[word] = count
    key_with_largest_value = sorted(weigth_dict, key=lambda x: weigth_dict[x])[-1]
    return key_with_largest_value

def find_word(word_list):
    letter_dict = count_letters(word_list)
    weigth_dict = {}
    for word in word_list:
        count = 0
        if len(set(word)) == 5:
            for letter in word:
                count += letter_dict.get(letter)
        else:
            for letter in word:
                count += letter_dict.get(letter)//2
        weigth_dict[word] = count
    key_with_largest_value = sorted(weigth_dict, key=lambda x: weigth_dict[x])[-1]
    return key_with_largest_value

def find_all_char_positions(word: str, char: str):
    positions = []
    pos = word.find(char)
    while pos != -1:
        positions.append(pos)
        pos = word.find(char, pos + 1)
    return positions

def compare(expected: str, guess: str):
    output = [0] * len(expected)
    counted_pos = set()
    for index, (expected_char, guess_char) in enumerate(zip(expected, guess)):
        if expected_char == guess_char:
            output[index] = 2
            counted_pos.add(index)
    for index, guess_char in enumerate(guess):
        if guess_char in expected and \
                output[index] != 2:
            positions = find_all_char_positions(word=expected, char=guess_char)
            for pos in positions:
                if pos not in counted_pos:
                    output[index] = 1
                    counted_pos.add(pos)
                    break
    return output

def calculate_mean(numbers):
    total = sum(numbers)
    mean = total / len(numbers)
    return round(mean,5)

def give_mean(target_word_list, start_word, imp_pos):
    global words
    attempt_list = []
    for word in target_word_list:
        words = convert_string_to_list(wordsstring)
        attempt_count = 0
        word_list = [start_word]
        enc_list = []
        target = [0,0,0,0,0]
        while target != [2,2,2,2,2]:
            attempt_count += 1
            if attempt_count == imp_pos:
                enc_list.append(compare(word, word_list[attempt_count-1]))
                word_list.append(find_word_impossible(wordle(word_list, enc_list)))
            else:
                enc_list.append(compare(word, word_list[attempt_count-1]))
                word_list.append(find_word(wordle(word_list, enc_list)))
            target = enc_list[-1]
        attempt_list.append(attempt_count)
    num_failed = sum(1 for num in attempt_list if num > 6)
    print(f"With the start word {start_word.upper()}, the calculated mean of attempts was {calculate_mean(attempt_list)}.")
    print(f"The Bot failed {num_failed} times out of {len(target_word_list)}.")

def help():
    print("""Arguments must be passed in the order as shown:    [starting_word] [imp_pos]
             - [starting_word] in string (default = trace).
             - [imp_pos] in [0,1,2,3,4,5,6] (default = 0).""")

if(len(sys.argv) == 3 and str(sys.argv[1]) in full_words and int(sys.argv[2]) in [0,1,2,3,4,5,6]):
    give_mean(words,str(sys.argv[1]),int(sys.argv[2]))
else:
    help()

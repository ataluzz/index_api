from collections import Counter
from statistics import median
import docx
import os
import re

vowels = 'аеёиоуыэюяaeiouy'

def find_files_with_extensions(ext, list_of_files):
    list_of_ext = ext.split(', ')
    sorted_list_of_files = []
    for extension in list_of_ext:
        for file in list_of_files:
            if file.endswith(extension):
                sorted_list_of_files.append(file)
            else:
                continue
    return sorted_list_of_files

def find_words(file):
    if file.endswith('.txt') or file.endswith('.py') or file.endswith('.md'):
        with open (file, 'r') as f:
            r = f.read()
            text = re.findall('[a-zа-яё]+', r, flags=re.IGNORECASE)
            return text
    elif file.endswith('.docx'):
        with open (file, 'rb') as f:
            doc = docx.Document(f)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            t = '\n'.join(fullText)
            text = re.findall('[a-zа-яё]+', t, flags=re.IGNORECASE)
            return text
    else:
        raise TypeError("Wrong type of file")
        
def syllables(word):
    syllable_count = 0
    word = word.lower()
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e') or word.endswith('ая') or word.endswith('ое') or word.endswith('оя'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

def dirs_files_text(directory, ext=''):
    list_of_directories = []
    list_of_files = []
    whole_text = []
    tree = os.walk(directory)
    for root, dirs, files in tree:
        for d in dirs:
            list_of_directories.append(d)
        for file in files:
            list_of_files.append(file)
        if ext:
            list_of_files = find_files_with_extensions(ext, list_of_files)
        for file in list_of_files:
            path = root + '/' + file
            try:
                text = find_words(path)
                whole_text.extend(text)
            except:
                continue
    return list_of_directories, list_of_files, whole_text

def count_vowels_and_consonants(word):
    vowels_count = 0
    consonants_count = 0
    for letter in word:
            if letter in vowels:
                vowels_count += 1
            else:
                consonants_count += 1
    return vowels_count, consonants_count

def stats_for_directory(directory, ext=''):
    frequent_words = ''
    rare_words = ''
    vowels_count = 0
    consonants_count = 0
    len_of_words = []
    whole_text = []
    num_of_syllables = 0
    res = dirs_files_text(directory, ext)
    count_files = len(res[1])
    count_words = Counter(res[2]).most_common()
    for word in res[2]:
        len_of_words.append(len(word))
        num_of_syllables += syllables(word)
        result_vc = count_vowels_and_consonants(word)
        vowels_count += int(result_vc[0])
        consonants_count += int(result_vc[1])
    medium_len = median(len_of_words)
    num_of_letters = sum(len_of_words)
    vowels_stats = (vowels_count / num_of_letters) * 100
    consonants_stats = (consonants_count / num_of_letters) * 100
    for element in count_words[0:5]:
        frequent_words += element[0] + ' - ' + str(element[1]) + "; "
    for element in count_words[-6:-1]:
        rare_words += element[0] + ' - ' + str(element[1]) + "; "
    result_dict = {
        "List of directories" : tuple(res[0]),
        "List of files" : tuple(res[1]),
        "Number of files" : count_files,
        "5 most frequent words" : frequent_words[:-2],
        "5 most rare words" : rare_words[:-2],
        "Medium length of word" : medium_len,
        "Percent of vowels" : round(vowels_stats),
        "Percent of consonants" : round(consonants_stats),
        "Number of syllables" : num_of_syllables
    }
    return result_dict

def stats_for_file(path_to_file):
    frequent_words = ''
    rare_words = ''
    vowels = 0
    consonants = 0
    len_of_words = []
    num_of_syllables = 0
    
    text = find_words(path_to_file)
    count_words = Counter(text).most_common()
    for word in text:
        len_of_words.append(len(word))
        num_of_syllables += syllables(word)
        result_vc = count_vowels_and_consonants(word)
    medium_len = median(len_of_words)
    num_of_letters = sum(len_of_words)
    vowels_stats = (int(result_vc[0]) / num_of_letters) * 100
    consonants_stats = (int(result_vc[1]) / num_of_letters) * 100
    for element in count_words[0:5]:
        frequent_words += element[0] + ' - ' + str(element[1]) + "; "
    for element in count_words[-6:-1]:
        rare_words += element[0] + ' - ' + str(element[1]) + "; "
    result_dict = {
        "5 most frequent words" : frequent_words[:-2],
        "5 most rare words" : rare_words[:-2],
        "Medium length of word" : medium_len,
        "Percent of vowels" : round(vowels_stats),
        "Percent of consonants" : round(consonants_stats),
        "Number of syllables" : num_of_syllables
    }
    return result_dict

def stats_for_word(path, ext='', word=''):
    vowels = 0
    consonants = 0
    res = dirs_files_text(path, ext)
    count = res[2].count(word)
    result_vc = count_vowels_and_consonants(word)
    num_of_syllables = syllables(word)
    result_dict = {
        "Number of times word is found": count,
        "Vowels": result_vc[0],
        "Consonants": result_vc[1],
        "Syllables": num_of_syllables
    }
    return result_dict

def stats(path, extensions='', word=''):
    if os.path.exists(path):
            if word:
                return stats_for_word(path, extensions, word)
            else:
                if os.path.isdir(path):
                    return stats_for_directory(path, extensions)
                elif os.path.isfile(path):
                    return stats_for_file(path)
    else:
        raise OSError("No such file or directory")
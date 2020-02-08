from bs4 import UnicodeDammit
from collections import Counter
from pathlib import Path
from statistics import median
import docx
import io
import json
import os
import re
import sys


def dirs(path):
    subfolders = [sf.name for sf in os.scandir(path) if sf.is_dir()]
    for sf in subfolders:
            subfolders.extend(dirs(Path(path,sf)))
    return subfolders

def files_with_specific_ext(path, *extensions):
    for obj in os.scandir(path):
        if obj.is_dir():
            yield from files_with_specific_ext(Path(obj.path), *extensions)
        elif obj.is_file():
            for ext in list(extensions):
                if obj.name.endswith(ext):
                    yield obj
        else:
            continue
            
def files(path):
    for obj in os.scandir(path):
        if obj.is_file():
            yield obj
        else:
            yield from files(Path(obj.path))

def find_words(file):
    if file.endswith('.txt') or file.endswith('.py') or file.endswith('.md'):
        with open(file, 'r') as f:
            r = UnicodeDammit(f.read())
            r = r.unicode_markup
            text = re.findall('[a-zа-яё]+', r, re.I)
            return text
    elif file.endswith('.docx'):
        with open(file, 'rb') as f:
            doc = docx.Document(f)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            t = '\n'.join(fullText)
            text = re.findall('[a-zа-яё]+', t, re.I)
            return text
    else:
        raise TypeError("Wrong type of file")
        
def count_vowels(word):
    vowels = re.findall('[aeiouyаеёиоуыэюя]', word, re.I)
    return len(vowels)

def count_syllables(word):
    syll = len(
        re.findall('(?!e$)[aeiouy]+', word, re.I) +
        re.findall('^[^aeiouy]*e$', word, re.I)
    )
    if not syll:
        syll = len(re.findall('[аеёиоуыэюя]', word, re.I))
    return syll
        
def stats_for_file(file):
    vowels = 0
    num_of_letters = 0
    num_of_syllables = 0
    text = find_words(file)
    num_of_words = len(text)
    count_words = Counter(text).most_common()
    for word in text:
        num_of_letters += len(word)
        vowels += count_vowels(word)
        num_of_syllables += count_syllables(word)
    freq_words = {element[0]: element[1] for element in count_words[0:5]}
    rare_words = {element[0]: element[1] for element in count_words[-6:-1]}
    return freq_words, rare_words, num_of_letters, \
            num_of_words, vowels, count_words, num_of_syllables
        
def stats_for_directory(path, *extensions):
    freq_words = {}
    rare_words = {}
    file_names = []
    num_of_letters = 0
    num_of_syllables = 0
    num_of_words = 0
    vowels = 0
    sf = dirs(path)
    f = None
    if extensions:
        f = files_with_specific_ext(path, *extensions)
    else:
        f = files(path)
    for elem in f:
        file_names.append(elem.name)
        try:
            res = stats_for_file(elem.path)
            freq_words.update(res[0])
            rare_words.update(res[1])
            num_of_letters += res[2]
            num_of_words += res[3]
            vowels += res[4]
            num_of_syllables += res[6]
        except TypeError:
            continue
    freq_words = Counter(freq_words).most_common(5)
    rare_words = Counter(rare_words).most_common()[-6:-1]
    return freq_words, rare_words, num_of_letters, \
            num_of_words, vowels, sf, file_names, num_of_syllables

def stats_for_word(path, *extensions, word=''):
    count = 0
    vowels = count_vowels(word)
    syllables = count_syllables(word)
    if os.path.isfile(path):
        try:
            res = stats_for_file(path)
            count = dict(res[5]).get(word, 0)
        except TypeError:
            return("Can't be done for this type of file")
    elif os.path.isdir(path):
        f = None
        if extensions:
            f = files_with_specific_ext(path, *extensions)
        else:
            f = files(path)
        for elem in f:
            try:
                res = stats_for_file(elem.path)
                count += dict(res[5]).get(word, 0)
            except TypeError:
                continue
    result_dict = {
        "Number of times word is found": count,
        "Vowels": vowels,
        "Consonants": len(word) - vowels,
        "Syllables": syllables
    }
    return result_dict
    
def whole_stats(path, *extensions, word=''):
    if os.path.exists(path):
        if word:
            return stats_for_word(path, *extensions, word=word)
        else:
            if os.path.isdir(path):
                res = stats_for_directory(path, *extensions)
                result_dict = {
                    "List of directories": res[5],
                    "List of files": res[6],
                    "5 most frequent words": res[0],
                    "5 most rare words": res[1],
                    "Medium length of word": round(res[2] / res[3]),
                    "Percent of vowels": round((res[4] / res[2])*100),
                    "Percent of consonants": round(((res[2] - res[4]) / res[2])*100),
                    "Number of syllables": res[7]
                }
                return result_dict
            elif os.path.isfile(path):
                res = stats_for_file(path)
                result_dict = {
                    "5 most frequent words": res[0],
                    "5 most rare words": res[1],
                    "Medium length of word": round(res[2] / res[3]),
                    "Percent of vowels": round((res[4] / res[2])*100),
                    "Percent of consonants": round(((res[2] - res[4]) / res[2])*100),
                    "Number of syllables": res[6]
                }
                return result_dict
    else:
        raise OSError("No such file or directory")

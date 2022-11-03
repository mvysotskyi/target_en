"""
Target En Game
"""

from typing import List
from random import randint
from collections import Counter

def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    grid = []
    for __ in range(3):
        grid_row = []
        for _ in range(3):
            grid_row.append(chr(ord("A") + randint(0, 25)))
        grid.append(grid_row)

    return grid

def word_division(word):
    """
    Count letters in word
    >>> word_division("lovering")
    [('e', 1), ('g', 1), ('i', 1), ('l', 1), ('n', 1), ('o', 1), ('r', 1), ('v', 1)]
    """
    result = []
    for ch in range(ord('a'), ord('z')):
        if chr(ch) in word:
            result.append((chr(ch), word.count(chr(ch))))

    return result

def word_contains(word1, word2):
    """
    >>> word_contains("word", "world")
    True
    >>> word_contains("some", "some")
    True
    >>> word_contains("any", "room")
    False
    """
    w1_div = word_division(word1.lower())
    w2_div = word_division(word2.lower())

    try:
        for key in w1_div:
            if w1_div[key] > w2_div[key]:
                return False
    except KeyError:
        return False

    return True

def check_word(word, letters):
    """
    >>> check_word("addtrgo", 'wumrovkif')
    False
    """
    assert len(letters) == 9
    if len(word) < 4 or (letters[4] not in word):
        return False
    if not word_contains(word, ''.join(letters)):
        return False

    return True

def get_words(dict_filename: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    >>> get_words("en", ["a", "i", "n", "a", "a", "a", "0", "0", "0"])
    ['aani']
    """
    assert len(letters) == 9

    result_set = set()

    try:
        with open(dict_filename, "r", encoding="utf-8") as file:
            for word in file.readlines()[2:]:
                word = word.strip().lower()
                if check_word(word, letters):
                    result_set.add(word)
    except FileNotFoundError:
        print(dict_filename + " is not found.")

    return list(result_set)


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish for *nix or Ctrl-Z+Enter
    for Windows.
    Note: the user presses the enter key after entering each word.
    """
    words = []
    while inp := input(">>> "):
        if len(inp) == 0:
            break
        words.append(inp)

    return words


def get_pure_user_words(user_words: List[str],
    letters: List[str], words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    >>> get_pure_user_words(["set", "tet", "eest"], ["s", "e", "t", "t", "e"\
    , "e", "r", "t", "s"], ["set", "tet"])
    ['eest']
    """
    user_words = {word for word in user_words if check_word(word, letters)}
    return list(user_words - set(words_from_dict))


def results():
    """
    Main game function.
    """
    result = ""
    letters = ""

    for row in generate_grid():
        letters += "".join(row).lower()
        print(" ".join(row))

    print("\nType words")
    user_words = get_user_words()
    dict_words = get_words("en", letters)

    result += ("Entered words: " + ', '.join(user_words) + '\n')
    result += ("Valid words that was not presented in dictionary: " +
    ', '.join(get_pure_user_words(user_words, letters, dict_words)))

    print(result)
    with open("results.txt", "w", encoding="utf-8") as file:
        file.write(result)

if __name__ == "__main__":
    # results()
    import doctest
    print(doctest.testmod())

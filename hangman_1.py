import os
import json
from typing import Final
from random import choice

from template import get_template


RU_LETTERS: Final = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def get_word() -> str:
    """Функция получения случайного слова"""
    with open("hangman/words.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
        return choice(data["words"])

def print_people(errors: int) -> None:
    """Фунция вывода персонажа в консоль"""
    print("Ваш персонаж сейчас выглядит так")
    print(get_template(errors), end = "")

def check_win_or_loose(word: str, player_word: str, errors: int) -> bool | None:
    """Функция для проверки победы или поражения"""
    if ''.join(player_word) == word:
        return True
    elif errors == 6:
        return False
    return None

def update_word(word: str, player_word: str, char: str) -> list[str]:
    """Функция для обновления отгаданых букв"""
    for i, ch in enumerate(word):
        if ch == char:
            player_word[i] = char  
    return player_word

def check_char(word: str, player_word: str, errors: int, char: str) -> tuple[list[str], str, int]:
    """Функция для проверки символа"""
    if char in word:
        player_word = update_word(word, player_word, char)
        text =  f"Вы отгадали букву. Ваше слово выглядит так - {''.join(player_word)}"
    else:
        errors += 1
        text =  f"Увы..., Вы совершили свою {errors} ошибку, Ваше слово выгядит так - {''.join(player_word)}"
    return player_word, errors, text

def logic_game() -> tuple[str, bool, int]:
    """Логика игры"""
    errors = 0
    word = get_word()
    print(word)
    player_word = ["_" for _ in range(len(word))]
    
    while True:
        char = input("Введите букву: ").lower()
        os.system('cls||clear')
        
        if char in RU_LETTERS:
            player_word, errors, text = check_char(word, player_word, errors, char)
            win_or_no = check_win_or_loose(word, player_word, errors)
            
            if isinstance(win_or_no, bool):
                return word, player_word, win_or_no, errors
            
            print(text)
            print_people(errors)
        else:
            print("Вы ввели некоректный символ")


def play():    
    print(
"""\nПриветствую Тебя, в игре 'Виселица'!
Цель игры угадать слово, пока от твоего персонажа не казнили
Приятной игры!!!\n""")
    
    word, player_word, result, errors = logic_game()
    text = (f"К сожалению вы проиграли :(\nСлово было - {word}, Вы отгадали - {"".join(player_word)}", f"Поздравляю! Вы выйграли :). Ваше количество ошибок - {errors}")
    print(text[result])
    print_people(errors)

while True:
    play()
    replay = input("Введите '+' чтобы сыграть еще, или любой символ чтобы выйти: ")
    if replay == "+":
        continue
    else:
        print("Досвидание!")
        break
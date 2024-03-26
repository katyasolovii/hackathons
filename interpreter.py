#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Модуль призначено для виконання коду, який згенеровано генератором коду.
Генератор коду повертає список команд.
Кожна команда - це кортеж: (<код_команди>, <операнд>)

Інтрепретатор виконує обчислення з використанням стеку.
Стек - це список, у який ми можемо додавати до кінця та брати з кінця числа.
Щоб додати число до стеку, можна використати
_stack.append(number)
Щоб взяти число зі стеку, можна використати
number = _stack.pop()

Для виконання арифметичної операції інтерпретатор бере два останніх числа зі стеку,
обчислює результат операції та додає результат до стеку.

Допустимі команди:
("LOADC", <число>) - завантажити число у стек
("LOADV", <змінна>) - завантажити значення змінної у стек (використовується storage)
("ADD", None) - обчислити суму двох верхніх елементів стеку
("SUB", None) - обчислити різницю двох верхніх елементів стеку
("MUL", None) - обчислити добуток двох верхніх елементів стеку
("DIV", None) - обчислити частку від ділення двох верхніх елементів стеку
("SET", <змінна>) - встановити значення змінної у пам'яті (storage)
"""
from storage import (get, clear, is_in, set as storage_set,
                    input_var, add)


_stack = []         # стек інтерпретатора для виконання обчислень
_last_error = 0     # код помилки останньої операції

# словник, що співставляє коди помилок до їх описи
ERRORS = {
    0: "",
    1: "Недопустима команда",
    2: "Змінна не існує",
    3: "Ділення на 0"
}


def _loadc(number):
    """Функція завантажує число у стек.
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: встановлює значення _last_error у 0
    :param number: число
    :return: None
    """
    global _last_error
    num = float(number)
    _stack.append(num)
    _last_error = 0
    return None


def _loadv(variable):
    """Функція завантажує значення змінної з пам'яті у стек.
    
    Використовує модуль storage.
    
    Якщо змінної не існує, то встановлює відповідну помилку.
    
    Якщо змінна не визначена, вводить значення зміної
    за допомогою storage.
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: змінює значення _last_error
    
    :param variable: ім'я змінної
    :return: None
    """
    global _last_error
    # змінна не існує
    if not is_in(variable):
        _last_error = 2
    # не визначена
    elif get(variable) is None:
        _last_error = input_var(variable)
        value = get(variable)
        _stack.append(value)
        _last_error = 0
    else:
        value = get(variable)
        _stack.append(value)
        _last_error = 0
    return None


def _add(_=None):
    """Функція бере 2 останніх елемента зі стеку,
    обчислює їх суму та додає результат у стек.
    
    Щоб взяти значення зі стеку, використовує _stack.pop()
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _last_error
    # останній 
    num1 = _stack.pop()
    # переостанній
    num2 = _stack.pop()
    summ = num1 + num2
    _last_error = 0
    _stack.append(float(summ))
    return None


def _sub(_=None):
    """Функція бере 2 останніх елемента зі стеку,
    обчислює їх різницю та додає результат у стек.
    
    Щоб взяти значення зі стеку, використовує _stack.pop()
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: встановлює значення _last_error у 0
    
    :param _: ігнорується
    :return: None
    """
    global _last_error
    num1 = _stack.pop()
    num2 = _stack.pop()
    subb = num2 - num1
    _last_error = 0
    _stack.append(subb)
    return None


def _mul(_=None):
    """Функція бере 2 останніх елемента зі стеку,
    обчислює їх добуток та додає результат у стек.
    
    Щоб взяти значення зі стеку, використовує _stack.pop()
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _last_error
    num1 = _stack.pop()
    num2 = _stack.pop()
    mull = num1 * num2
    _last_error = 0
    _stack.append(mull)
    return None


def _div(_=None):
    """Функція бере останнй та передостанній елементи зі стеку,
    обчислює частку від ділення передостаннього елемента на останній
    та додає результат у стек.
    
    Якщо дільник - 0, то встановлює помилку.
    
    Щоб взяти значення зі стеку, використовує _stack.pop()
    
    Щоб додати у стек, використовує _stack.append(...)
    
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _last_error
    num1 = _stack.pop()
    num2 = _stack.pop()
    if num1 == 0:
        _last_error = 3
    else:
        divv = num2 / num1
        _last_error = 0
        _stack.append(divv)
    return None


def _set(variable):
    """Функція бере останній елемент зі стеку
    та встановлює значення змінної рівним цьому елементу.
    
    Якщо змінної не існує, то встановлює відповідну помилку.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    
    Побічний ефект: змінює значення _last_error
    
    :param variable: ім'я змінної
    :return: None
    """
    global _last_error
    value = _stack.pop()
    if not is_in(variable):
        _last_error = 2
    else:
        storage_set(variable, value)
        _last_error = 0
    return None


COMMAND_FUNCS = {
    "LOADC": _loadc,
    "LOADV": _loadv,
    "ADD": _add,
    "SUB": _sub,
    "MUL": _mul,
    "DIV": _div,
    "SET": _set
}


def execute(code):
    """Функція виконує код програми, записаний у code.
    
    Повертає код останньої помилки або 0, якщо помилки немає.
    Якщо є помилка, то показує її.
    
    Використовує словник функцій COMMAND_FUNCS.

    :param code: код програми - список кортежів (<команда>, <операнд>)
    :return: код останньої помилки або 0, якщо помилки немає
    """
    global _last_error
    for command, operand in code:
        if command in COMMAND_FUNCS:
            f = COMMAND_FUNCS[command]
            f(operand)
            if _last_error != 0:
                break
        else:
            _last_error = 1
            break
    return _last_error


if __name__ == "__main__":
    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADV', 'x'),
            ('LOADV', 'a'),
            ('MUL', None),
            ('SET', 't'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    add('x')
    add('y')
    add('a')
    add('t')
    add('z')
    last_error = execute(code)

    assert last_error == 3

    code = [('XXX', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    clear()
    last_error = execute(code)

    assert last_error == 1

    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    clear()
    last_error = execute(code)
    assert last_error == 2

    code = [('LOADC', 2.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    clear()
    add('x')
    add('y')
    add('z')
    last_error = execute(code)

    z = get('z')
    assert last_error == 0 and z == 1.0

    print("Success = True")
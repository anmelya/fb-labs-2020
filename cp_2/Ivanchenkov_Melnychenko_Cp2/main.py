from viginer_lib import algorithm1, conformity_index, decrypt_file, conformity_index_file, \
    shift_text, build_key, exclude_letters, crypt
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.ticker as ticker

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def demoindex():
    """ построение зависимости индекса соответствия от длины ключа/количества блоков разбиения текста """
    ci_file = conformity_index_file('text.txt')
    x, y1, y2 = [], [], []
    for i in range(2, 25):
        Y_blocks = algorithm1('to_decrypt.txt', i)
        np_res = np.array([conformity_index(Y_blocks[item]) for item in Y_blocks])
        x.append(i)
        y1.append(ci_file)
        y2.append(np.mean(np_res))
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()


def task1_2():
    ci_file = conformity_index_file('text.txt')
    x, y1, y2 = [], [], []
    with open('text1.txt', 'r', encoding='utf-8') as f:
        text = ''.join([exclude_letters(line) for line in f])
    for i in range(2, 21):
        key = ''.join([random.choice(alphabet) for j in range(0, i)])
        crypted = crypt(text, key)
        x.append(i)
        y1.append(ci_file)
        y2.append(conformity_index(crypted))
    fig, ax = plt.subplots()
    ax.plot(x, y1)
    ax.plot(x, y2)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.show()


def task3():
    demoindex()
    Y_blocks = algorithm1('to_decrypt.txt', 15)
    len_y = min(np.array([len(Y_blocks[item]) for item in Y_blocks]))
    crypted_freq = []
    for item in Y_blocks:
        Y_blocks[item] = Y_blocks[item][0:len_y]
        crypted_freq.append(shift_text(Y_blocks[item]))

    # комбинация элементов и частотных словарей каждого интервала разбиения
    combo_1 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    # построение ключа и расшифровка текста
    key = build_key(combo_1, crypted_freq)
    print(key)
    decrypt_file('to_decrypt.txt', 'decrypted0.txt', key)

    # комбинация элементов и частотных словарей каждого интервала разбиения
    combo_2 = (0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0)

    # построение ключа и расшифровка текста
    key = build_key(combo_2, crypted_freq)
    print(key)
    decrypt_file('to_decrypt.txt', 'decrypted.txt', key)

    count = 0
    for item in zip(combo_1, combo_2):
        if item[0] != item[1]:
            count += 1

    print('Частоти по блокам, де символи ключа не було відновлено відразу ', count)


if __name__ == '__main__':
    task3()


import random
import secrets
import math
from itertools import product


def random_s(n_bytes=256):
    """ генерация случайного числа и проверка его алгоритмом Миллера - Рабина """
    # инициализация генератора, генерация числа
    n = secrets.randbits(n_bytes)
    while not is_Prime(n):
        n = secrets.randbits(n_bytes)
    return n


def is_Prime(n):
    """ тестирование на простоту методом Миллера - Рабена """
    if n != int(n):
        return False
    n = int(n)

    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(math.floor(math.log(n, 2))):  # количество тестов (рекомендованное)
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True


def pair_generator():
    """ генерирует набор из 4 простых чисел заданной длины, удовлетворяющих условию p1*q1 < p2*q2 """
    case = True
    while case:
        pq = [random_s(n_bytes=8) for i in range(0, 4)]
        for case in product(pq, repeat=4):
            if (case[0] * case[1] < case[2] * case[3]) & ((case[0] != case[1]) & (case[2] != case[3])):
                return case


def gen_key(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = pow(2, 16) + 1
    while math.gcd(phi_n, e) != 1:
        e = random.randint(3, phi_n - 1)
    d = pow(e, -1, phi_n)
    return (d, p, q), (e, n)


def generateKeyPair():
    pq = [random_s(n_bytes=256) for i in range(0, 2)]
    return gen_key(pq[0], pq[1])


def encrypt(M, key):
    encd = pow(M, key[0], key[1])
    return hex(encd)


def decrypt(M, key):
    try:
        Md = int(M[2:], 16)
    except:
        Md = M
    n = key[1] * key[2]
    return pow(Md, key[0], n)


def sign(M, key):
    n = key[1] * key[2]
    encd = pow(M, key[0], n)
    return hex(encd)


def verify(M, S, key):
    try:
        Sd = int(S[2:], 16)
    except:
        Sd = S
    M_check = pow(Sd, key[0], key[1])
    return M == M_check


def sendKey(k, A_keys, B_key):
    e1 = B_key[0]
    n1 = B_key[1]
    d = A_keys[0][0]
    n = A_keys[1][1]
    S = pow(k, d, n)
    S1 = pow(S, e1, n1)
    k1 = pow(k, e1, n1)
    return hex(k1), hex(S1)


def receiveKey(message, A_key, B_keys):
    d1 = B_keys[0][0]
    n1 = B_keys[1][1]
    try:
        k1 = int(message[0][2:], 16)
        S1 = int(message[1][2:], 16)
    except:
        k1 = message[0]
        S1 = message[1]
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    return k == pow(S, A_key[0], A_key[1])

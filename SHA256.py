H_HEX = [
    '6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a',
    '510e527f', '9b05688c', '1f83d9ab', '5be0cd19'
]
K_HEX = [
    '428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
    'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
    'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
    '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
    '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',
    'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',
    '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
    '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2'
]


def fillZerosBefore(string, length):
    """
    Заполняет строку нулями слева до определенной длины
    :param string: строка
    :param length: длина возвращаемой строки
    :return: заполненная нулями строка
    """
    if len(str(string)) != length:
        for i in range(length - len(str(string))):
            string = '0' + string
    return string


def xor(a, b):
    """
    Исключающее ИЛИ
    :param a: строка 1
    :param b: строка 2
    :return: результат операции
    """
    if len(a) > len(b):
        b = fillZerosBefore(b, len(a))
    elif len(a) < len(b):
        a = fillZerosBefore(a, len(b))
    out = ''
    for i in range(len(a)):
        out += '1' if a[i] != b[i] else '0'
    return out


def and_(a, b):
    """
    Логическое И
    :param a: строка 1
    :param b: строка 2
    :return: результат операции
    """
    if len(a) > len(b):
        b = fillZerosBefore(b, len(a))
    elif len(a) < len(b):
        a = fillZerosBefore(a, len(b))
    out = ''
    for i in range(len(a)):
        out += '1' if a[i] == '1' and b[i] == '1' else '0'
    return out


def not_(a):
    """
    Логическое НЕ
    :param a: строка
    :return: результат операции
    """
    out = ''
    for i in range(len(a)):
        out += '1' if a[i] == '0' else '0'
    return out


def addMod(nums, w=32):
    """
    Сложение по модулю 2**w
    :param nums: кортеж с битовыми строками для сложения
    :param w: модуль w, по умолчанию 32
    :return: результат операции
    """
    summ = 0
    for i in range(len(nums)):
        summ += int(nums[i], 2)
    result = summ % (2 ** w)
    return fillZerosBefore(bin(result)[2:], w)


def SHR(x, n):
    """
    Сдвиг вправо
    :param x: битовая строка
    :param n: количество сдвинутых битов
    :return: итоговая строка
    """
    return '0' * n + x[:-n]


def ROTR(x, n):
    """
    Круговой сдвиг вправо
    :param x: битовая строка
    :param n: количество сдвинутых битов
    :return: итоговая строка
    """
    return x[-n:] + x[:-n]


def Ch(x, y, z):
    """
    Логическая операция Ch
    :param x: 32-битная строка
    :param y: 32-битная строка
    :param z: 32-битная строка
    :return: результат операции
    """
    return xor(and_(x, y), and_(not_(x), z))


def Maj(x, y, z):
    """
    Логическая операция Maj
    :param x: 32-битная строка
    :param y: 32-битная строка
    :param z: 32-битная строка
    :return: результат операции
    """
    return xor(xor(and_(x, y), and_(x, z)), and_(y, z))


def SIGMA0(x):
    """
    Логическая операция Σ0
    :param x: 32-битная строка
    :return: результат операции
    """
    return xor(xor(ROTR(x, 2), ROTR(x, 13)), ROTR(x, 22))


def SIGMA1(x):
    """
    Логическая операция Σ1
    :param x: 32-битная строка
    :return: результат операции
    """
    return xor(xor(ROTR(x, 6), ROTR(x, 11)), ROTR(x, 25))


def sigma0(x):
    """
    Логическая операция σ0
    :param x: 32-битная строка
    :return: результат операции
    """
    return xor(xor(ROTR(x, 7), ROTR(x, 18)), SHR(x, 3))


def sigma1(x):
    """
    Логическая операция σ1
    :param x: 32-битная строка
    :return: результат операции
    """
    return xor(xor(ROTR(x, 17), ROTR(x, 19)), SHR(x, 10))


def padding(M):
    """
    Дополняет битовую строку так, чтобы ее длина была кратна 512 бит
    :param M: сообщение в виде битовой строки
    :return: дополненная битовая строка
    """
    l: int = len(M)
    k = (448 - (l + 1)) % 512
    M += '1' + '0' * k + fillZerosBefore(bin(l)[2:], 64)
    return M


def parsing(M, size):
    """
    Разбиение на блоки
    :param M: битовая строка
    :param size: размер блока
    :return: массив блоков
    """
    n = len(M) // size
    M_arr = []
    for i in range(n):
        start = i * size
        end = start + size
        M_arr.append(M[start:end])
    remainder = len(M) % size
    if remainder != 0:
        M_arr.append(M[-remainder:])
    return M_arr


def preprocessing(M):
    """
    Выполняет функции препроцессинга
    :param M: битовая строка
    :return: массив блоков
    """
    M = padding(M)
    M = parsing(M, 512)
    return M


def messageSchedule(M):
    """
    Генерирует расписание сообщений
    :param M: массив блоков
    :return: массив с расписанием
    """
    W = []
    for i in range(64):
        if i < 16:
            W.append(M[i])
        else:
            w_i = addMod((sigma1(W[i - 2]), W[i - 7], sigma0(W[i - 15]), W[i - 16]))
            W.append(w_i)
    return W


def SHA256(M):
    """
    Хеширует сообщение согласно алгоритму
    :param M: битовая строка
    :return: хеш
    """
    H, K = [], []
    for i in H_HEX:
        H.append(fillZerosBefore(bin(int(i, 16))[2:], 32))
    for i in K_HEX:
        K.append(fillZerosBefore(bin(int(i, 16))[2:], 32))
    M_arr = preprocessing(M)
    N = len(M_arr)
    for i in range(N):
        W = messageSchedule(parsing(M_arr[i], 32))
        a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]
        for t in range(64):
            T1 = addMod((h, SIGMA1(e), Ch(e, f, g), K[t], W[t]))
            T2 = addMod((SIGMA0(a), Maj(a, b, c)))
            h, g, f, e, d, c, b, a = g, f, e, addMod((d, T1)), c, b, a, addMod((T1, T2))
        H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7] = (
            addMod((a, H[0])), addMod((b, H[1])), addMod((c, H[2])), addMod((d, H[3])),
            addMod((e, H[4])), addMod((f, H[5])), addMod((g, H[6])), addMod((h, H[7]))
        )
    return hex(int(''.join(H), 2))[2:]


def digestView(H):
    """
    Преобразует хеш в необходимый вид
    :param H: хеш
    :return: хеш
    """
    digest = ''
    H = H.upper()
    for i in range(0, len(H), 8):
        digest += H[i: i + 8] + ' '
    return digest[:-1]

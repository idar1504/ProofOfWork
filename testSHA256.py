import SHA256


def readTextFileLines(path):
    """
    Читает текстовый файл, генерируя массив, каждый элемент которого - строка из файла
    :param path: путь до файла
    :return: массив строк
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines


def binify(message):
    """
    Преобразует строку в битовую строка
    :param message: строка
    :return: битовая строка
    """
    return SHA256.fillZerosBefore(bin(int.from_bytes(message.encode(), 'big'))[2:], len(message) * 8)


def testSamples():
    """
    Прогоняет содержимое "SHA-256 samples" в качестве тестов и выводит, все ли захешировалось верно
    :return: None
    """
    print('\nTest results:')
    messageSamples = 'SHA-256 samples/messages.txt'
    digestSamples = 'SHA-256 samples/digests.txt'
    messages = readTextFileLines(messageSamples)
    digests = readTextFileLines(digestSamples)
    for i in range(len(messages)):
        Hash = SHA256.digestView(SHA256.SHA256(binify(messages[i])))
        print(Hash)
        print(Hash == digests[i])
    print('\n')

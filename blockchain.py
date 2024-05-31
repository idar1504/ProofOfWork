import SHA256
import testSHA256
import time
import numpy as np


def MerkleTreeRoot(transactions):
    """
    Рассчитывает корень древа Меркла
    :param transactions: транзакции в виде массива байтовых строк
    :return: корень Меркла в виде хеша
    """
    Hash = []
    for i in range(len(transactions)):
        Hash.append(SHA256.SHA256(testSHA256.binify(SHA256.SHA256(testSHA256.binify(transactions[i])))))
    if len(Hash) == 1:
        return Hash[0]
    if len(Hash) % 2 == 1:
        Hash.append(Hash[-1])
    recurrentHash = []
    for i in range(0, len(Hash), 2):
        recurrentHash.append(Hash[i] + Hash[i + 1])
    return MerkleTreeRoot(recurrentHash)


class BlockHeader:
    def __init__(self, previousHash, transactions, nonce):
        """
        Конструктор класса
        :param previousHash: хеш предыдущего блока, битовая строка 256 бит
        :param transactions: массив строк с транзакциями
        :param nonce: 32 бит
        """
        self.blockSize = np.uint32(self.CalculateSize(transactions))
        self.previousHash = previousHash
        self.MerkleRoot = MerkleTreeRoot(transactions)
        self.timestamp = np.uint32(time.time())
        self.nonce = np.uint32(nonce)

    @staticmethod
    def CalculateSize(transactions):
        """
        Рассчитывает размер блока
        :param transactions: массив транзакций
        :return: размер блока
        """
        size = 80
        for i in transactions:
            size += len(i)
        return size

    def to_0608b(self):
        """
        Преобразует хеддер блока в строку длиной 608 бит
        :return: строка 608 бит
        """
        size = format(self.blockSize, '032b')
        previousH = SHA256.fillZerosBefore(format(int(self.previousHash, 16), '0b'), 256)
        merkleRoot = SHA256.fillZerosBefore(format(int(self.MerkleRoot, 16), '0b'), 256)
        timestamp = format(self.timestamp, '032b')
        nonce = format(self.nonce, '032b')
        return size + previousH + merkleRoot + timestamp + nonce

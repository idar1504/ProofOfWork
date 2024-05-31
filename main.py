import SHA256
import testSHA256
import blockchain
import numpy as np


if __name__ == '__main__':
    # print(SHA256.digestView(blockchain.MerkleTreeRoot(testSHA256.readTextFileLines('Transactions.txt'))))
    bh1 = blockchain.BlockHeader('427E3533BE054175B116CC1F5EF21CB7C6A1FB73B23243AFDAF0347450D04586', testSHA256.readTextFileLines('Transactions.txt'), 0)
    Hash = SHA256.fillZerosBefore(format(int(SHA256.SHA256(testSHA256.binify(bh1.to_0608b())), 16), '0b'), 256)
    while Hash[0:4] != '0000':
        bh1.nonce += np.uint(1)
        Hash = SHA256.fillZerosBefore(format(int(SHA256.SHA256(testSHA256.binify(bh1.to_0608b())), 16), '0b'), 256)
    print(bh1.nonce)

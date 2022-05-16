import uuid

from Crypto.Hash import SHA256


def updatHash(*args):
    hashingText = ""
    h = SHA256.new()
    for arg in args:
        hashingText+=str(arg)
    h.update(hashingText.encode())
    return h.hexdigest()



class Block:
    transactions = None
    blockHash = None

    def __init__(self):
        self.ID = uuid.uuid4().hex
        self.transactions = []
        self.previousBlockHash = "0"*64


    def hash(self):
        return updatHash(self.ID,self.transactions,self.previousBlockHash)

    def add_transaction(self,transaction):
        self.transactions.append(transaction)

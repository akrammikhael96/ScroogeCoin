import uuid
import User
import Coin
from Crypto.Hash import SHA256

def updatHash(*args):
    hashingText = ""
    h = SHA256.new()
    for arg in args:
        hashingText+=str(arg)
    h.update(hashingText.encode())
    return h.hexdigest()

class Transaction:
    transactionHash=None

    def __init__(self,sender,receiver,coin):
        self.ID = uuid.uuid4().hex
        assert isinstance(coin, Coin.Coin)
        self.coin = coin
        assert isinstance(sender, User.User)
        self.sender = sender
        assert isinstance(receiver, User.User)
        self.receiver = receiver
        self.previousTransactionHash = "0"*64

    def signedText(self):
        l = [self.ID,self.sender,self.receiver,self.coin,self.hash()]
        signedText = ""
        for i in l:
            signedText += str(i)
        return signedText

    def senderSignature(self):
        return self.sender.sk.sign(self.signedText().encode())

    def hash(self):
        return updatHash(self.ID,self.sender,self.receiver,self.previousTransactionHash)

    def getOriginalSignature(self):
            signature = self.sender.sk.sign(self.signedText().encode())
            return signature

    def verifySignature(self,senderSignature):
        try:
            if(self.sender.vk.verify(senderSignature,self.signedText().encode())):
                return True
        except:
                return False






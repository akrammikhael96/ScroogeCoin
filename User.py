import binascii


from ecdsa import SigningKey

class User:
    def __init__(self,virtualName):
        self.virtualName = virtualName
        self.coinsOwned = []
        self.sk = SigningKey.generate()
        self.vk = self.sk.verifying_key
        self.privateKey = binascii.b2a_hex(self.sk.to_string()).decode()
        self.publicKey = binascii.b2a_hex(self.sk.get_verifying_key().to_string()).decode()

    def add_coin(self,coin):
        self.coinsOwned.append(coin)

    def remove_coin(self,coin):
        self.coinsOwned.remove(coin)





import uuid
class Coin:
    previousTransactionHash = None
    def __init__(self):
        self.ID = uuid.uuid4().hex


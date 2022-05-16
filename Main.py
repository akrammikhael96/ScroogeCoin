#Coin -> new coin = Coin() ---- ID
#User -> new user = User("u1") ---- PublicKey , PrivateKey , coinsOwned[] , add_coin() , remove_coin()
#Transaction -> new transaction = Transaction(u1,u2,c1) ---- ID , Coin , sender , receiver , PreviousTransactionHash , hash() , senderSignature() , verifySignature(signature)
#Block -> new block = Block() ---- ID , transactions[] , previousBlockHash , hash()
#BlockChain -> new blockChain = BlockChain()---- blocks[] , add_block()
import random
from ecdsa import SigningKey

import keyboard
import Coin
import User
import Transaction
import Block
import BlockChain
import time

#Generate Coins
coins = []
for i in range(1000):
    coins.insert(i,Coin.Coin())

#Generate Users
users = []
for i in range(1,101):
    users.insert(i,User.User("user"+ str(i)))

#Give each user 10 coins
for user in users:
    for i in range(10):
        user.add_coin(coins[i])
        coins[i].previousTransactionHash ="0"*64
    del coins[0:10]

#Scrooge Signature
signedString = ""
scrooge_sk = SigningKey.generate()
scrooge_vk = scrooge_sk.verifying_key
scrooge_signature = scrooge_sk.sign(signedString.encode())

#wrong Signature
signedString2 = ""
wrong_sk = SigningKey.generate()
wrong_vk = wrong_sk.verifying_key
wrong_signature = wrong_sk.sign(signedString2.encode())

#Generate Transactions
validTransactions =[]
invalidTransactions = []
blockUnderConstructionTransactions =[]
blocks = []
blockChain = BlockChain.BlockChain()
allTransactions = []

def generateTransactions():
    random_index = random.randrange(len(users))
    sender = users[random_index]
    receiver  = random.choice(users)
    if(len(users[random_index].coinsOwned)==0 or sender == receiver):
        generateTransactions()
    coin = random.choice(users[random_index].coinsOwned)
    transaction = Transaction.Transaction(sender,receiver,coin)
    print(transaction)
    allTransactions.append(transaction)
    if(checkTransactionValidity(transaction)):
        validTransactions.append(transaction)
        transaction.previousTransactionHash = coin.previousTransactionHash
        coin.previousTransactionHash=transaction.hash()
        sender.remove_coin(coin)
        receiver.add_coin(coin)
        if(len(blockUnderConstructionTransactions)<9):
             blockUnderConstructionTransactions.append(transaction)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction)
            createBlock()
    else:
        invalidTransactions.append(transaction)

def generateWrongSignatureTransactions():
    random_index = random.randrange(len(users))
    sender = users[random_index]
    sender.sk =wrong_sk
    receiver  = random.choice(users)
    if(len(users[random_index].coinsOwned)==0 or sender == receiver):
        generateTransactions()
    coin = random.choice(users[random_index].coinsOwned)
    transaction = Transaction.Transaction(sender,receiver,coin)
    print(transaction)
    allTransactions.append(transaction)
    if(checkTransactionValidity(transaction)):
        validTransactions.append(transaction)
        transaction.previousTransactionHash = coin.previousTransactionHash
        coin.previousTransactionHash = transaction.hash()
        sender.remove_coin(coin)
        receiver.add_coin(coin)
        if(len(blockUnderConstructionTransactions)<9):
             blockUnderConstructionTransactions.append(transaction)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction)
            createBlock()
    else:
        invalidTransactions.append(transaction)

def generateDoubleSpendingTransactions():
    random_index = random.randrange(len(users))
    sender = users[random_index]
    receiver  = random.choice(users)
    sender2 = sender
    receiver2 = random.choice(users)
    if(len(users[random_index].coinsOwned)==0 or sender == receiver):
        generateDoubleSpendingTransactions()
    coin = random.choice(users[random_index].coinsOwned)
    coin2 = coin
    transaction = Transaction.Transaction(sender,receiver,coin)
    transaction2 = Transaction.Transaction(sender2, receiver2, coin2)
    print(transaction)
    allTransactions.append(transaction)
    allTransactions.append(transaction2)

    if(checkTransactionValidity(transaction)):
        validTransactions.append(transaction)
        transaction.previousTransactionHash = coin.previousTransactionHash
        coin.previousTransactionHash=transaction.hash()
        sender.remove_coin(coin)
        receiver.add_coin(coin)
        if(len(blockUnderConstructionTransactions)<9):
             blockUnderConstructionTransactions.append(transaction)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction)
            createBlock()
    else:
        invalidTransactions.append(transaction)

    if (checkTransactionValidity(transaction2)):
        validTransactions.append(transaction2)
        transaction2.previousTransactionHash = coin2.previousTransactionHash
        coin2.previousTransactionHash = transaction2.hash()
        print(len(validTransactions))
        if (len(blockUnderConstructionTransactions) < 9):
            blockUnderConstructionTransactions.append(transaction2)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction2)
            createBlock()
    else:
        invalidTransactions.append(transaction2)

def generateBranchingCoinTransactions():
    random_index = random.randrange(len(users))
    sender = users[random_index]
    receiver  = random.choice(users)
    sender2 = receiver
    receiver2 = random.choice(users)
    if(len(users[random_index].coinsOwned)==0 or sender == receiver):
        generateBranchingCoinTransactions()
    coin = random.choice(users[random_index].coinsOwned)
    coin2 = coin
    transaction = Transaction.Transaction(sender,receiver,coin)
    transaction2 = Transaction.Transaction(sender2, receiver2, coin2)
    print(transaction)
    allTransactions.append(transaction)
    allTransactions.append(transaction2)

    if(checkTransactionValidity(transaction)):
        validTransactions.append(transaction)
        transaction.previousTransactionHash = coin.previousTransactionHash
        coin.previousTransactionHash=transaction.hash()
        sender.remove_coin(coin)
        receiver.add_coin(coin)
        if(len(blockUnderConstructionTransactions)<9):
             blockUnderConstructionTransactions.append(transaction)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction)
            createBlock()
    else:
        invalidTransactions.append(transaction)

    if (checkTransactionValidity(transaction2)):
        validTransactions.append(transaction2)
        transaction2.previousTransactionHash = coin2.previousTransactionHash
        coin2.previousTransactionHash = transaction2.hash()
        print(len(validTransactions))
        if (len(blockUnderConstructionTransactions) < 9):
            blockUnderConstructionTransactions.append(transaction2)
        elif (len(blockUnderConstructionTransactions) == 9):
            blockUnderConstructionTransactions.append(transaction2)
            createBlock()
    else:
        invalidTransactions.append(transaction2)

def checkTransactionValidity(transaction):
    senderSignature = transaction.senderSignature()
    if(transaction.verifySignature(senderSignature)):
        if(checkDoubleSpending(validTransactions,transaction)):
            return False
        else:
            return True
    else:
        return False

def checkDoubleSpending(validTransactions , transaction):
    checkPreviousHash = transaction.previousTransactionHash
    checkCoin = transaction.coin.ID
    checkSender = transaction.sender
    for x in validTransactions:
        if(str(x.previousTransactionHash) == str(checkPreviousHash) and str(x.coin.ID) == str(checkCoin)and str(x.sender)==str(checkSender)):
            return True

    return False

def createBlock():
    b1 = Block.Block()
    for transaction in blockUnderConstructionTransactions:
        b1.add_transaction(transaction)
    if(len(blockChain.blocks) >0):
        b1.previousBlockHash = blockChain.blocks[len(blockChain.blocks)-1].hash()

    b1.hash()
    blockChain.add_block(b1)
    blockUnderConstructionTransactions.clear()


#Writing Output
def printUsers():
    result=""
    title = "Users Current Data : "
    H1 = '----------------------------------------------------'
    data =""
    for i in range(len(users)):
        data +='\n'+"Virtual Name : "+users[i].virtualName+'\n'+"Public Key : "+users[i].publicKey+'\n'+"Coins Owned : "+str(len(users[i].coinsOwned))+'\n'
    result = title+'\n'+H1 + '\n' + data + '\n'+'----------------------------------------------------'
    return result

def printTransaction(transaction):
    result = ""
    TH = ("Transaction Hash : " + transaction.hash())
    PTH = ("Previous Transaction Hash : " + transaction.previousTransactionHash)
    TID =("Transaction ID : " + transaction.ID)
    S =("From : " + transaction.sender.virtualName)
    R=("To : " + transaction.receiver.virtualName)
    CID =("Coin ID : " + transaction.coin.ID)
    result = TH+'\n'+PTH+'\n'+TID+'\n'+S+'\n'+R+'\n'+CID
    return result

def printBlock(block):
    result=""
    H1 = "***********************"
    BN =("Block Number : "+ str(blockChain.blocks.index(block)+1))
    H2 = "***********************"
    BH = ("Block Hash : " + block.hash())
    PBH = ("Previous Block Hash : " + block.previousBlockHash)
    T = ""
    for i in range(len(block.transactions)):
        T +='\n'+printTransaction(block.transactions[i])+'\n'
    result = H1+'\n'+BN+'\n'+H2+'\n'+'\n'+BH+'\n'+PBH+'\n'+T+'\n'
    return result

def printBlockChain(blockchain):
    result =""
    title = "Blockchain : "
    H1 = '----------------------------------------------------'+'\n'
    end = "End Of Blockchain"+'\n'
    for i in range(len(blockchain.blocks)):
        result += '\n'+'\n'+printBlock(blockchain.blocks[i])+'\n'+'\n'+'----------------------------------------------------'

    return title+'\n'+H1 +'\n'+result +'\n'+end

def printBlockUnderConstructionTransactions():
    result =""
    title ="Block Under Construction : "
    H1 = '----------------------------------------------------'
    data = ""
    if ((len(blockUnderConstructionTransactions) == 0)):
        data = '\n' +"No Transactions"+ '\n'
    else:
        for i in range(len(blockUnderConstructionTransactions)):
            data += '\n' + printTransaction(blockUnderConstructionTransactions[i]) + '\n'
    result = '\n'+title+'\n'+H1 + '\n' + data + '\n'+'----------------------------------------------------'
    return result

def printInvalidTransactions():
    title = "Invalid Transactions : "
    H1 = '----------------------------------------------------'
    data = ""
    if ((len(invalidTransactions) == 0)):
        data = '\n' +"No Invalid Transactions"+ '\n'
    else:
        for i in range(len(invalidTransactions)):
             data += '\n' + printTransaction(invalidTransactions[i]) + '\n'

    result = '\n' + title+'\n'+H1 + '\n' + data +'\n'+'----------------------------------------------------'
    return result


def writeToFile ():
    f = open("Output.txt", "w")
    f.write(printUsers())
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write(printInvalidTransactions())
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write(printBlockUnderConstructionTransactions())
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write(printBlockChain(blockChain))
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("Final Hash Pointer Signature : " +lastBlockSignature)
    f.write("\n")
    f.close()


#Stimulation
def stimulation():
    generatedTransactions = 0
    generatedWrongSignatureTransactions = 0
    generatedDoubleSpendingTransactions = 0
    while(True):
         if keyboard.is_pressed('space'):
             time.sleep(0.1)
             generateTransactions()
             generatedTransactions += 1
             print("Generated Transactions : "+ str(generatedTransactions))
         if keyboard.is_pressed('s'):
             time.sleep(0.1)
             generateWrongSignatureTransactions()
             generatedWrongSignatureTransactions += 1
             print("Generated Wrong Signature Transactions : "+ str(generatedWrongSignatureTransactions))
         if keyboard.is_pressed('d'):
             time.sleep(0.1)
             generateDoubleSpendingTransactions()
             generatedDoubleSpendingTransactions += 1
             print("Generated Douple Spending Transactions : "+ str(generatedDoubleSpendingTransactions))
         if keyboard.is_pressed('a'):
             time.sleep(0.1)
             generateBranchingCoinTransactions()
         if keyboard.is_pressed('esc'):
             break



#main
stimulation()

#Scrooge sign last block hash pointer
if(len(blockChain.blocks)>0):
    lastBlock = blockChain.blocks[len(blockChain.blocks)-1]
    lastBlockSignature = str(scrooge_sk.sign(str(lastBlock.hash()).encode()))
else:
    lastBlockSignature = "Undefined"


writeToFile()


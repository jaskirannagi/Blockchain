import hashlib, json, sys
import copy
import random
#import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(17,GPIO.OUT) #blue
#GPIO.setup(27,GPIO.OUT) #green
#GPIO.setup(22,GPIO.OUT)#red
#GPIO.setup(4,GPIO.IN) #switch
setup=0
buffcount=0
transaction=-1
start_time = 0
txnBuffer = [0 for x in range(15)]
state = {u'raspA':50, u'raspB':50,u'raspC':50}  # Define the initial state
genesisBlockTxns = [state]  #initial block transactions is equal to the sum of all initial transactions
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns} #dictionary for all the block details
    
def hashMe(msg=""): #hashing function for the 256 SHA- algorithm
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str: #if the msg is not a string (public or private keys)
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability! 
        #other nodes may not have the block info in chronolgical order, order then execute. This means it is accurate to repeat.
        
    if sys.version_info.major == 2: #python version
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8') #sha256 hash on the block msg
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()#sha256 hash on the block msg

genesisHash = hashMe( genesisBlockContents ) #hash of the block for the first chain
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents} #hash of first block with block hash (hash to test changes, block to continue chain)
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True) #orgaise the dictionary in chronological order so that the hash is the same each time it is done.
chain = [genesisBlock] #chain is the genisis block and hash. (can change and check the chain with the two array entries)

    
def maketestBlock(txns,chain): #make the first block to add to the chain
    parentBlock = chain[-1]#parentblock is last element in the chain 
    parentHash  = parentBlock[u'hash'] #parent hash is last hash in last chain element
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1 #the block number is block number in the contents of the latest chain element +1.
    txnCount    = len(txns)#count the amount of transactions happend so far
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                     u'txnCount':len(txns),'txns':txns} #update the block contents
    blockHash = hashMe( blockContents ) #hash the block contents
    block = {u'hash':blockHash,u'contents':blockContents} # block is equal to a 2d dictionary of the hash and hash contents.
    
    return block    



def makeTransaction(maxValue=3):#randomly generate a transaction to test the system
    # This will create valid transactions in the range of (1,maxValue)
    sign      = int(random.getrandbits(1))*2 - 1   # This will randomly choose -1 or 1
    amount    = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays   = -1 * alicePays
    # By construction, this will always return transactions that respect the conservation of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
   
    return {u'Alice':alicePays,u'Bob':bobPays}
    
    
    
    
def flooddetect(nodee,flooded,node1,flooded1,node2,flooded2):#randomly generate a transaction to test the system

    return {nodee:flooded,node1:flooded1,node2:flooded2}    
    
def updateState(txn): # state (number of transactions, users, etc)
    # Inputs: txn, state: dictionaries keyed with account names, holding numeric values for transfer amount (txn) or account balance (state)
    # Returns: Updated state, with additional users added to state if necessary
    # NOTE: This does not not validate the transaction- just updates the state!
    
    # If the transaction is valid, then update the state
   
    for key in txn:
        if key in state.keys(): #.keys refers to json, i.e. cell positions in an array
            state[key] += txn[key]#if state  corect, make it = chain + next transactions
        else:
            state[key] = txn[key] #if state not corect, make it = to the chain state
    return state
    
    

def transactionbuffer(): #call every loop, will reset tranasaction buffer when enough transactions can generate a block
    blockSizeLimit = 5  # Arbitrary number of transactions per block- 
                   #  this is chosen by the block miner, and can vary between blocks!
    while len(txnBuffer) > 0: # for the length of the buffer
        bufferStartSize = len(txnBuffer) #get size of array
    
        ## Gather a set of valid transactions for inclusion
        txnList = [] # empty the list
        u=0;
        while (txnBuffer[u] > 0) & (len(txnList) < blockSizeLimit): # while there is transactions and the transaction list (array to be added to the block) is less than 5
            newTxn = txnBuffer.pop() #take trasnaction off the array and set it equal to new transaction variable
            validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
            u=u+1
            if validTxn:           # If we got a valid state, not 'False'
                txnList.append(newTxn) #add transaction to new transactiion list
                updateState(newTxn) #update the state of the the ledger
            else:
                print("ignored transaction")
                sys.stdout.flush()
                continue  # This was an invalid transaction; ignore it and move on
        
        ## Make a block
        myBlock = maketestBlock(txnList,chain) #create the bock from the details
        chain.append(myBlock) #add the block to the chain
    return
        


def isValidTxn(txn,state): #check the transaction (or switch signal) is OK.
    # Assume that the transaction is a dictionary keyed by account names

    # Check that the sum of the deposits and withdrawals is 0
   
    
    return True






def checkBlockHash(block):
    # Raise an exception if the hash does not match the block contents
    expectedHash = hashMe( block['contents'] )
    if block['hash']!=expectedHash:
        raise Exception('Hash does not match contents of block %s'%
                        block['contents']['blockNumber'])
    return



def checkBlockValidity(block,parent,state):    
    # We want to check the following conditions:
    # - Each of the transactions are valid updates to the system state
    # - Block hash is valid for the block contents
    # - Block number increments the parent block number by 1
    # - Accurately references the parent block's hash
    parentNumber = parent['contents']['blockNumber']
    parentHash   = parent['hash']
    blockNumber  = block['contents']['blockNumber']
    
    # Check transaction validity; throw an error if an invalid transaction was found.
    for txn in block['contents']['txns']:
        if isValidTxn(txn,state):
            state = updateState(txn,state)
        else:
            raise Exception('Invalid transaction in block %s: %s'%(blockNumber,txn))

    checkBlockHash(block) #Check hash integrity; raises error if inaccurate

    if blockNumber!=(parentNumber+1): #check correct block number
        raise Exception('Hash does not match contents of block %s'%blockNumber)

    if block['contents']['parentHash'] != parentHash: #check corrent hash
        raise Exception('Parent hash not accurate at block %s'%blockNumber)
    
    return state




def checkChain(chain):
    # Work through the chain from the genesis block (which gets special treatment), 
    #  checking that all transactions are internally valid,
    #    that the transactions do not cause an overdraft,
    #    and that the blocks are linked by their hashes.
    # This returns the state as a dictionary of accounts and balances,
    #   or returns False if an error was detected

    
    ## Data input processing: Make sure that our chain is a list of dicts
    if type(chain)==str:
        try:
            chain = json.loads(chain)
            assert( type(chain)==list)
        except:  # This is a catch-all, admittedly crude
            return False
    elif type(chain)!=list:
        return False
    
    state = {}
    ## Prime the pump by checking the genesis block
    # We want to check the following conditions:
    # - Each of the transactions are valid updates to the system state
    # - Block hash is valid for the block contents

    for txn in chain[0]['contents']['txns']:
        state = updateState(txn,state)
    checkBlockHash(chain[0])
    parent = chain[0]
    
    ## Checking subsequent blocks: These additionally need to check
    #    - the reference to the parent block's hash
    #    - the validity of the block number
    for block in chain[1:]:
        state = checkBlockValidity(block,parent,state)
        parent = block
        
    return state







while(1):
    
   
    nodeBchain = copy.copy(chain) 
    
   # if (GPIO.input(4)!=transaction) #if the switch has changed state 
    #    if (GPIO.input(4)): #if flood detection is on
    
    txnBuffer[14-buffcount] = flooddetect('raspA',50,'raspB',0,'raspC',0) #send the id number 50 (flooded) to the chain.
    buffcount=buffcount+1 #increment once to update the transaction buffer
        
   #     else (!GPIO.input(4)) #if flood detection is off
    txnBuffer[buffcount] = flooddetect('raspA',100,'raspB',0,'raspC',0) #send the id number 100 (not flooded) to the chain.
    buffcount=buffcount+1 #increment once to update the transaction buffer
        #transaction=GPIO.input(4)# the transaction is only recorded if the switch state has been changed.
        
    if (time.time()-start_time>10):#every 10 seconds
        transactionbuffer() #check if number of transactions/block is complete and then if so, generate a new block and add to the chain.
        #every 10 seconds the state changes are recorded, the transaction will be read and added to the block chain. if more than 5 transaction
        #in the time period are set off, only 5 transactions / block will be added to the chain (queue the transactions.)
        buffcount=0
        start_time = time.time()#present time
    
    ############ test code to test block generation (randomizes payment from two people) 
   # nodeBtxns  = [makeTransaction() for i in range(5)] #create an array to store the transactions that happen. the buffer will check and create the block when ready and empty
   # newBlock   = maketestBlock(nodeBtxns,nodeBchain)#adds the transactions to the current block
    ########## it will add the transaction to the block.
    
   
   
    ### broadcast chain to all nodes
    ### recieve chain from all nodes

  #  newBlock= #recieve block from other nodes


    print("Blockchain on Node A is currently %s blocks long"%len(chain))

    try:
        print("New Block Received; checking validity...")
        state = checkBlockValidity(newBlock,chain[-1],state) # Update the state- this will throw an error if the block is invalid!
        chain.append(newBlock)
    except:
        print("Invalid block; ignoring and waiting for the next block...")

        print("Blockchain on Node A is now %s blocks long"%len(chain))


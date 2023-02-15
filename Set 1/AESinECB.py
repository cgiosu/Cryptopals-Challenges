import os , sys , codecs , base64
from Galois import rijndael

### XOR sum of two lists of the same length
def XOR(list1, list2):
    return [a ^ b for (a,b) in zip(list1,list2)]

### AES Key Schedule
def KeySchedule(key):
    ### Round Constants
    rcon = [[2 ** (i-1), 0, 0, 0] for i in range(9)]
    rcon += [[27, 0, 0, 0] , [54, 0, 0, 0]]

    ### RotWord
    def RotWord(word):
        return word[1:] + word[0:1]
    
    ### SubWord
    def SubWord(word):
        return [sbox(word[i]) for i in range(4)]
    
    ### Generating Round Keys
    roundkeys = [key]
    for i in range(10):
        next_1 = XOR(XOR(roundkeys[i][0:4], SubWord(RotWord(roundkeys[i][12:]))), rcon[i+1])
        next_2 = XOR(roundkeys[i][4:8], next_1)
        next_3 = XOR(roundkeys[i][8:12], next_2)
        next_4 = XOR(roundkeys[i][12:] , next_3)
        roundkeys.append(next_1 + next_2 + next_3 + next_4)
    return roundkeys

### sbox
def sbox(a: int):
    b, constant, s = rijndael(a).inv().val , 31, 99
    for i in range(5):
        s ^= (constant & 1 == 1) * b
        constant >>= 1
        b = (b << 1) ^ ((b & 128 == 128) * 257)
    return s

### Inverse of sbox    
def sbox_inv(s: int):
    b, constant = 5, 74
    for i in range(7):
        b^= (constant & 1 == 1) * s
        constant >>= 1
        s = (s << 1) ^ ((s & 128 == 128) * 257)
    return rijndael(b).inv().val

### Inverse of SubBytes
def SubBytes_inv(state):
    return [sbox_inv(state[i]) for i in range(16)]

### Inverse of ShiftRows
order = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]
def ShiftRows_inv(state):
    return [state[order[i]] for i in range(16)]

### Inverse of MixColumns for a single column
mixer = [rijndael(14),rijndael(11),rijndael(13),rijndael(9),rijndael(14),rijndael(11),rijndael(13),rijndael(9)]
def MixOneColumn_inv(state):
    return [(mixer[4-i]*rijndael(state[0]) + mixer[5-i]*rijndael(state[1]) + mixer[6-i]*rijndael(state[2]) + mixer[7-i]*rijndael(state[3])).val for i in range(4)]

### Inverse of MixColumns
def MixColumns_inv(state):
    newstate = []
    for i in range(4):
        newstate += MixOneColumn_inv(state[4 * i : 4 * (i+1)])
    return newstate

def dec_AEC(state , keys):
    ### Decrypring the final round
    state = SubBytes_inv(ShiftRows_inv(XOR(state, keys[10])))
    ### Decrypting the middle rounds
    for i in range(9,0,-1):
        state = SubBytes_inv(ShiftRows_inv(MixColumns_inv(XOR(state, keys[i]))))
    ### Decrypting the first round
    return XOR(state, keys[0])

### Initial Key and Generating Round Keys
key = [ord(x) for x in 'YELLOW SUBMARINE']
keys = KeySchedule(key)

### Encrypted message partitioned into blocks of size 16 and decoded
with open(os.path.join(sys.path[0], "7.txt"), "r") as f:
    state_64 = f.read()
state = base64.b64decode(state_64)
n = len(state) // 16
decrypted = ''
for i in range(n):
    block = dec_AEC(state[16*i : 16*(i+1)] , keys)
    for j in range(16):
        decrypted += chr(block[j])
print(decrypted)


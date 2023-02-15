import os , sys , codecs , base64
from SingleByteXOR import best_decryption
from RepeatingKeyXOR import rep_XOR

### Hamming distance function, counts the number of differing bits in two given bytes of the same length
def hamming(bytes_1,bytes_2):
    ### Initialize distance as 0
    distance , n = 0 , len(bytes_1)
    ### We will compare corresponding bytes and count the differing bits
    for i in range(n):
        ### Number of differing bits is just the number of ones in the binary representation of XOR sum
        xor_sum = bytes_1[i] ^ bytes_2[i]
        for digit in bin(xor_sum)[2:]:
            distance+= int(digit)
    return distance

### Function to find the correct keysize by minimizing the Hamming distance between the blocks of size 'keysize'
def keysize(message_bytes):
    ### Initialize the (correct) key as 1 and its score 8 (maximum possible)
    keysize , score = 1 , 8
    for guess in range(2,40):
        ### Evaluate 'guess' by looking at the average Hamming distance between the consecutive blocks of size 'guess'
        num_blocks = len(message_bytes) // (2 * guess)
        new_score = sum(hamming(message_bytes[2*i*guess:(2*i+1)*guess] , message_bytes[(2*i+1)*guess:(2*i+2)*guess]) for i in range(num_blocks))/(num_blocks*guess)
        ### Update the key if we achieved a smaller score with our guess
        if new_score < score:
            keysize , score = guess, new_score
    return keysize

### Function to group the bytes of the messages based on the specific part of the key used on them for a given keysize
def partition(message_bytes , keysize):
    partitioned = [b''] * keysize
    for i in range(len(message_bytes)):
        partitioned[i % keysize] += bytes([message_bytes[i]])
    return partitioned

### Read the file line by line and put them together
"""
with open(os.path.join(sys.path[0], "6.txt"), "r") as f:
    lines = f.read().split('\n')
secret_64 = ''.join(lines)
secret_bytes = base64.b64decode(secret_64)   
"""

### Determine the best key for each partition using the expected frequency of the characters in an English text
"""
keysize = keysize(secret_bytes)
partitioned_bytes = partition(secret_bytes, keysize)
key_bytes = b''
for i in range(keysize):
    key_bytes += bytes([best_decryption(partitioned_bytes[i])[1]])
"""
### Decryption
"""
decrypted_bytes = rep_XOR(key_bytes , secret_bytes)
decrypted_text = codecs.decode(decrypted_bytes , 'latin-1')
print(decrypted_text)
"""
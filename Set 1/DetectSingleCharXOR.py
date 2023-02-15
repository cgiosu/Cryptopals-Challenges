import codecs
import os , sys
from SingleByteXOR import best_decryption

### Read the file line by line
with open(os.path.join(sys.path[0], "4.txt"), "r") as f:
    lines = f.readlines()
    n = len(lines)
### For each line, look at the most likely decryption and their Englishness scores
for i in range(n):
    ### Ignore the last character of each line, which is just '\n'
    secret_hex = lines[i].strip()
    secret_bytes = codecs.decode(secret_hex , 'hex')
    lines[i] = best_decryption(secret_bytes)
### Sort the strings by their Englishness scores and choose the decrypted message with the best(lowest) score
lines.sort()
decrypted_text = codecs.decode(lines[0][2] , 'latin-1')

"""
print(decrypted_text)
"""
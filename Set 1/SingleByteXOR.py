
from collections import defaultdict
import codecs

### Estimated frequency of each letter (and whitespace character) in English texts, used for determining if a text might be English or not
freq_table = {'a': 0.082, 'b': 0.15, 'c': 0.28, 'd': 0.43, 'e': 0.13, 'f': 0.022, 'g': 0.02, 'h': 0.061, 'i': 0.07, 'j': 0.0015, 'k': 0.0077, 'l': 0.04,
'm': 0.024, 'n': 0.067, 'o': 0.075,'p': 0.019, 'q': 0.00095, 'r': 0.06, 's': 0.063, 't': 0.091, 'u': 0.028, 'v': 0.0098, 'w': 0.024, 'x': 0.024,
'y': 0.02, 'z': 0.00074, ' ': 0.13} 

### Function measuring 'Englishness' of a text using chi-square statistic (a larger score means it cannot be English)
def englishness(text : str):
    ### To utilize the frequency table, convert everything to lower case characters
    text = text.lower()
    ### Check the frequency sparately for the digits, and other rare characters which are not covered in the frequency table.
    n, rare, digits= len(text) , 0 , 0
    ### Store the number of occurrences of each (type of) character in dictionary count
    count = defaultdict(int)
    for char in text:
        if char in freq_table:
            count[char] += 1
        elif char.isnumeric():
            digits += 1
        ### Punctuations might have lots of appearances, ignore them
        elif char not in (["." , "," , "?", "!" , "-" , "_" , "'" , "\n" , '"']):
            rare += 1
    ### It is reasonable to think that at most 1 of 20 characters will be a 'rare' character and at most 1 of 5 characters will be a digit
    if 20* rare > n or 5 * digits > n:
        return 1000
    else:
        ### chi-square statistic for the lower case (and whitespace character) letter frequency
        chi_score = sum(((count[char]/n - freq_table[char]) ** 2) / freq_table[char] for char in freq_table)
        return chi_score

### Function returning the decrypted message as bytes object using the given key (int between 0 and 256) for a single-byte XOR 
def decrypt(key : int , secret_bytes):
    n = len(secret_bytes)
    ### Take the XOR sum of each byte of text_bytes and key, store the results in bytes_decrypted
    bytes_decrypted = b''
    for i in range(n):
        bytes_decrypted += bytes([secret_bytes[i] ^ key])
    return bytes_decrypted

### Function returning the most likely decrypted message together with the best key and the Englishness score of the message
def best_decryption(secret_bytes):
    best_key , best_score = 0 , 1000
    for key in range(256):
        if englishness(codecs.decode(decrypt(key , secret_bytes) , 'latin-1')) < best_score:
            best_key , best_score = key , englishness(codecs.decode(decrypt(key , secret_bytes) , 'latin-1'))
    return [best_score , best_key , decrypt(best_key , secret_bytes)]

"""
secret_hex= input('Please enter the encrypted, hex encoded string: \n')
secret_bytes = codecs.decode(secret_hex , 'hex')
decrypted_bytes = best_decryption(secret_bytes)[2]
decrypted_text = codecs.decode(decrypted_bytes , 'latin-1')
print(decrypted_text)
"""
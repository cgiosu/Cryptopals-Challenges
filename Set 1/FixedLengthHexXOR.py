import codecs

### Function to find the XOR sum of to bytes obejcts of the same length
def XOR(bytes_1 , bytes_2):
    n = len(bytes_1)
    ### Take the XOR sum for the corresponding bytes in bytes_1 and bytes_2 and use bytes_summed to store the results
    bytes_summed = b''
    for i in range(n):
        bytes_summed += bytes([bytes_1[i] ^ bytes_2[i]])
    return bytes_summed

"""
hex_1 = input('Please enter the first hexadecimal number: \n')
hex_2 = input('Please enter the second hexadecimal number: \n')
bytes_1 = codecs.decode(hex_1 , 'hex')
bytes_2 = codecs.decode(hex_2 , 'hex')
XOR_bytes = XOR(bytes_1 , bytes_2)
XOR_hex = codecs.encode(XOR_bytes , 'hex')
XOR_hex_text = codecs.decode(XOR_hex)
print(XOR_hex_text)
"""
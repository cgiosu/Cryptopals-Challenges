import codecs

### Function converting a given hexadecimal string to base 64
def hex_to_64 (str_hex : str):
    ### decode the hex string as bytes
    x = codecs.decode(str_hex , 'hex')
    ### encode the bytes as base64
    y = codecs.encode(x , 'base64')
    ### decode the bytes encoded in base 64 as a string
    z = codecs.decode(y)
    return z

"""
str_hex = input('Please enter the hexadecimal that will be converted to base 64: \n')
print(hex_to_64(str_hex))
"""
import codecs

### Function encrypting the given text with the given key using repeating-key XOR
def rep_XOR(key_bytes , message_bytes):
    m , n , bytes_summed = len(key_bytes) , len(message_bytes) , b''
    for i in range(n):
        bytes_summed += bytes([message_bytes[i] ^ key_bytes[i % m]])
    return bytes_summed

"""
message_text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key_text = input('Please enter the key: \n')
message_bytes = codecs.encode(message_text)
key_bytes = codecs.encode(key_text)
encrypted_bytes = rep_XOR(key_bytes , message_bytes)
encrypted_hex = codecs.encode(encrypted_bytes , 'hex')
encrypted_hex_text = codecs.decode(encrypted_hex)
print(encrypted_hex_text)
"""
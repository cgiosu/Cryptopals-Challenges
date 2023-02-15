### Class for doing arithmetic in the Rijndael Field GF(2^8)
class rijndael:
    ### View the every elements of the Rijndael field as integers from 0 to 255
    def __init__(self, val: int):
        self.val = val
    
    ### Summation in the the Rijndael Field
    def __add__(self, other):
        return rijndael(self.val ^ other.val)
    
    ### Multiplication in the Rijndael Field
    def __mul__(self, other):
        x, y, prod = self.val, other.val, 0
        for i in range(8):
            prod ^= (y & 1 == 1) * x
            y >>= 1
            x = (x << 1) ^ ((x & 128 == 128) * 283)
        return rijndael(prod)

    ### Multiplicative inverse in the Rijndael Field
    def inv(self):
        x, inverse = self , rijndael(1)
        for i in range(7):
            x *= x
            inverse *= x
        return inverse
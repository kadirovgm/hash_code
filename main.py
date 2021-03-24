import hashlib
import math

# A = ...
#
# T = ...
# def hash_generate(n):
#     R = []
#     for i in range(n):
#         x = R[i] # записываем в Х очередной 256-битный блок
#         # сохраним начальные значения A, B, C, D
#         # AA = A
#         # BB = B
#         # CC = C
#         # DD = D
#
#
# def MDbuffer():
#     A = '0x67452301'
#     B = '0xEFCDAB89'
#     C = '0x98BADCFE'
#     D = '0x10325476'
#
#     for i in range(64):
#         T[i] = (math.pow(2,32)*math.fabs(math.sin(float(i+1))))
def Mod512(input):
    tmp = input.encode('utf-8')
    if (tmp[len(tmp) - 1] == 10):
        text_byte = tmp[0:len(tmp)-1]
    else:
        text_byte = tmp[0:len(tmp)]
        text_bit = [bin(text_byte[i])[2:] for i in range(0, len(text_byte))]
        text_bit.append('10000000')
    while ((len(text_bit) * 8) % 512 != 448):
        text_bit.append('00000000')

    tmp = list(bin(len(text_byte * 8))[2:].zfill(64))
    part1 = tmp[0:32]
    part2 = tmp[32:64]
    text_bit.append(''.join(part2[24:32]))
    text_bit.append(''.join(part2[16:24]))
    text_bit.append(''.join(part2[8:16]))
    text_bit.append(''.join(part2[0:8]))

    text_bit.append(''.join(part1[24:32]))
    text_bit.append(''.join(part1[16:24]))
    text_bit.append(''.join(part1[8:16]))
    text_bit.append(''.join(part1[0:8]))

    part512 = [''.join(text_bit[i + j] for i in range(0, 64)) for j in range(0, len(text_bit), 64)]
    return part512



def BlockTo16word(binPart):
    word16 = []
    for i in range(0, 512,32):
        bit1 = ''.join(binPart[i:i+8])
        bit2 = ''.join(binPart[i + 8:i + 16])
        bit3 = ''.join(binPart[i + 16:i + 24])
        bit4 = ''.join(binPart[i + 24:i + 32])
        tmp = bit4 + bit3 + bit2 + bit1
        word16.append(int(tmp, 2))
def FF(A, B, C, D, x, y, X):
    return 0

def GG(A, B, C, D, x, y, X):
    return 0

def HH(A, B, C, D, x, y, X):
    return 0

def MD4_hash_generate(input):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    block_512 = Mod512(input) # расширение и деление на блоки по 512 бит

    for i in range(0, len(block_512)):
        X = BlockTo16word(block_512[i]) # деление блока на слова (16)
        AA = A
        BB = B
        CC = C
        DD = D
        A = FF(A, B, C, D, 0, 3, X)
        D = FF(D, A, B, C, 1, 7, X)
        C = FF(C, D, A, B, 2, 11, X)
        B = FF(B, C, D, A, 3, 19, X)
        A = FF(A, B, C, D, 4, 3, X)
        D = FF(D, A, B, C, 5, 7, X)
        C = FF(C, D, A, B, 6, 11, X)
        B = FF(B, C, D, A, 7, 19, X)
        A = FF(A, B, C, D, 8, 3, X)
        D = FF(D, A, B, C, 9, 7, X)
        C = FF(C, D, A, B, 10, 11, X)
        B = FF(B, C, D, A, 11, 19, X)
        A = FF(A, B, C, D, 12, 3, X)
        D = FF(D, A, B, C, 13, 7, X)
        C = FF(C, D, A, B, 14, 11, X)
        B = FF(B, C, D, A, 15, 19, X)
        #############################
        A = GG(A, B, C, D, 0, 3, X)
        D = GG(D, A, B, C, 4, 5, X)
        C = GG(C, D, A, B, 8, 9, X)
        B = GG(B, C, D, A, 12, 13, X)
        A = GG(A, B, C, D, 1, 3, X)
        D = GG(D, A, B, C, 5, 5, X)
        C = GG(C, D, A, B, 9, 9, X)
        B = GG(B, C, D, A, 13, 13, X)
        A = GG(A, B, C, D, 2, 3, X)
        D = GG(D, A, B, C, 6, 5, X)
        C = GG(C, D, A, B, 10, 9, X)
        B = GG(B, C, D, A, 14, 13, X)
        A = GG(A, B, C, D, 3, 3, X)
        D = GG(D, A, B, C, 7, 5, X)
        C = GG(C, D, A, B, 11, 9, X)
        B = GG(B, C, D, A, 15, 13, X)
        ############################
        A = HH(A, B, C, D, 0, 3, X)
        D = HH(D, A, B, C, 8, 9, X)
        C = HH(C, D, A, B, 4, 11, X)
        B = HH(B, C, D, A, 12, 15, X)
        A = HH(A, B, C, D, 2, 3, X)
        D = HH(D, A, B, C, 10, 9, X)
        C = HH(C, D, A, B, 6, 11, X)
        B = HH(B, C, D, A, 14, 15, X)
        A = HH(A, B, C, D, 1, 3, X)
        D = HH(D, A, B, C, 9, 9, X)
        C = HH(C, D, A, B, 5, 11, X)
        B = HH(B, C, D, A, 13, 15, X)
        A = HH(A, B, C, D, 3, 3, X)
        D = HH(D, A, B, C, 11, 9, X)
        C = HH(C, D, A, B, 7, 11, X)
        B = HH(B, C, D, A, 15, 15, X)

        A = (A+AA)%(pow(2,32))
        B = (B+BB)%(pow(2,32))
        C = (C+CC)%(pow(2,32))


    temp = A.to_bytes(4,'big')
    oneA = str(hex(temp[3])[2:].zfill(2))
    twoA = str(hex(temp[2])[2:].zfill(2))
    threeA = str(hex(temp[1])[2:].zfill(2))
    fourA = str(hex(temp[0])[2:].zfill(2))
    a_hex = oneA + twoA + threeA + fourA

    temp = B.to_bytes(4, 'big')
    oneB = str(hex(temp[3])[2:].zfill(2))
    twoB = str(hex(temp[2])[2:].zfill(2))
    threeB = str(hex(temp[1])[2:].zfill(2))
    fourB = str(hex(temp[0])[2:].zfill(2))
    b_hex = oneB + twoB + threeB + fourB

    temp = C.to_bytes(4, 'big')
    oneC = str(hex(temp[3])[2:].zfill(2))
    twoC = str(hex(temp[2])[2:].zfill(2))
    threeC = str(hex(temp[1])[2:].zfill(2))
    fourC = str(hex(temp[0])[2:].zfill(2))
    c_hex = oneC + twoC + threeC + fourC

    temp = D.to_bytes(4, 'big')
    oneD = str(hex(temp[3])[2:].zfill(2))
    twoD = str(hex(temp[2])[2:].zfill(2))
    threeD = str(hex(temp[1])[2:].zfill(2))
    fourD = str(hex(temp[0])[2:].zfill(2))
    d_hex = oneD + twoD + threeD + fourD

    hash = a_hex + b_hex + c_hex + d_hex

    return hash
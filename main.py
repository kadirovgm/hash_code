import hashlib
import math

# расширение и деление на блоки
# def Mod512(input):
#     tmp = input.encode('utf-8') # UTF-8 кодирование
#     if (tmp[len(tmp) - 1] == 10): # если последний символ 10: то срезаем этот элемент
#         text_byte = tmp[0:len(tmp)-1]
#     else:
#         text_byte = tmp[0:len(tmp)]
#
#     text_bit = [bin(text_byte[i])[2:] for i in range(0, len(text_byte))]
#     text_bit.append('10000000')
#     while ((len(text_bit) * 8) % 512 != 448):
#         text_bit.append('00000000')
#
#     tmp = list(bin(len(text_byte * 8))[2:].zfill(64))
#
#     part1 = tmp[0:32]
#     part2 = tmp[32:64]
#
#     text_bit.append(''.join(part2[24:32]))
#     text_bit.append(''.join(part2[16:24]))
#     text_bit.append(''.join(part2[8:16]))
#     text_bit.append(''.join(part2[0:8]))
#
#     text_bit.append(''.join(part1[24:32]))
#     text_bit.append(''.join(part1[16:24]))
#     text_bit.append(''.join(part1[8:16]))
#     text_bit.append(''.join(part1[0:8]))
#
#     part512 = [''.join(text_bit[i + j] for i in range(0, 64)) for j in range(0, len(text_bit), 64)]
#     return part512
#
#
#
# def BlockTo16word(binPart):
#     word16 = []
#     for i in range(0, 512, 32):
#         bit1 = ''.join(binPart[i:i+8])
#         bit2 = ''.join(binPart[i + 8:i + 16])
#         bit3 = ''.join(binPart[i + 16:i + 24])
#         bit4 = ''.join(binPart[i + 24:i + 32])
#         tmp = bit4 + bit3 + bit2 + bit1
#         word16.append(int(tmp, 2))
#
#
# def FF(A, B, C, D, x, y, X):
#     return 0
#
# def GG(A, B, C, D, x, y, X):
#     return 0
#
# def HH(A, B, C, D, x, y, X):
#     return 0
#
# def MD4_hash_generate(input):
#     A = 0x67452301
#     B = 0xefcdab89
#     C = 0x98badcfe
#     D = 0x10325476
#
#     block_512 = Mod512(input) # расширение и деление на блоки по 512 бит
#
#     for i in range(0, len(block_512)):
#         X = BlockTo16word(block_512[i]) # деление блока на слова (16)
#         AA = A
#         BB = B
#         CC = C
#         DD = D
#
#         A = FF(A, B, C, D, 0, 3, X)
#         D = FF(D, A, B, C, 1, 7, X)
#         C = FF(C, D, A, B, 2, 11, X)
#         B = FF(B, C, D, A, 3, 19, X)
#
#         A = FF(A, B, C, D, 4, 3, X)
#         D = FF(D, A, B, C, 5, 7, X)
#         C = FF(C, D, A, B, 6, 11, X)
#         B = FF(B, C, D, A, 7, 19, X)
#
#         A = FF(A, B, C, D, 8, 3, X)
#         D = FF(D, A, B, C, 9, 7, X)
#         C = FF(C, D, A, B, 10, 11, X)
#         B = FF(B, C, D, A, 11, 19, X)
#
#         A = FF(A, B, C, D, 12, 3, X)
#         D = FF(D, A, B, C, 13, 7, X)
#         C = FF(C, D, A, B, 14, 11, X)
#         B = FF(B, C, D, A, 15, 19, X)
#         #############################
#         A = GG(A, B, C, D, 0, 3, X)
#         D = GG(D, A, B, C, 4, 5, X)
#         C = GG(C, D, A, B, 8, 9, X)
#         B = GG(B, C, D, A, 12, 13, X)
#
#         A = GG(A, B, C, D, 1, 3, X)
#         D = GG(D, A, B, C, 5, 5, X)
#         C = GG(C, D, A, B, 9, 9, X)
#         B = GG(B, C, D, A, 13, 13, X)
#
#         A = GG(A, B, C, D, 2, 3, X)
#         D = GG(D, A, B, C, 6, 5, X)
#         C = GG(C, D, A, B, 10, 9, X)
#         B = GG(B, C, D, A, 14, 13, X)
#
#         A = GG(A, B, C, D, 3, 3, X)
#         D = GG(D, A, B, C, 7, 5, X)
#         C = GG(C, D, A, B, 11, 9, X)
#         B = GG(B, C, D, A, 15, 13, X)
#         ############################
#         A = HH(A, B, C, D, 0, 3, X)
#         D = HH(D, A, B, C, 8, 9, X)
#         C = HH(C, D, A, B, 4, 11, X)
#         B = HH(B, C, D, A, 12, 15, X)
#
#         A = HH(A, B, C, D, 2, 3, X)
#         D = HH(D, A, B, C, 10, 9, X)
#         C = HH(C, D, A, B, 6, 11, X)
#         B = HH(B, C, D, A, 14, 15, X)
#
#         A = HH(A, B, C, D, 1, 3, X)
#         D = HH(D, A, B, C, 9, 9, X)
#         C = HH(C, D, A, B, 5, 11, X)
#         B = HH(B, C, D, A, 13, 15, X)
#
#         A = HH(A, B, C, D, 3, 3, X)
#         D = HH(D, A, B, C, 11, 9, X)
#         C = HH(C, D, A, B, 7, 11, X)
#         B = HH(B, C, D, A, 15, 15, X)
#
#         A = (A+AA)%(pow(2,32))
#         B = (B+BB)%(pow(2,32))
#         C = (C+CC)%(pow(2,32))
#         D = (D+DD)%(pow(2,32))
#
#
#     temp = A.to_bytes(4,'big')
#     oneA = str(hex(temp[3])[2:].zfill(2))
#     twoA = str(hex(temp[2])[2:].zfill(2))
#     threeA = str(hex(temp[1])[2:].zfill(2))
#     fourA = str(hex(temp[0])[2:].zfill(2))
#     a_hex = oneA + twoA + threeA + fourA
#
#     temp = B.to_bytes(4, 'big')
#     oneB = str(hex(temp[3])[2:].zfill(2))
#     twoB = str(hex(temp[2])[2:].zfill(2))
#     threeB = str(hex(temp[1])[2:].zfill(2))
#     fourB = str(hex(temp[0])[2:].zfill(2))
#     b_hex = oneB + twoB + threeB + fourB
#
#     temp = C.to_bytes(4, 'big')
#     oneC = str(hex(temp[3])[2:].zfill(2))
#     twoC = str(hex(temp[2])[2:].zfill(2))
#     threeC = str(hex(temp[1])[2:].zfill(2))
#     fourC = str(hex(temp[0])[2:].zfill(2))
#     c_hex = oneC + twoC + threeC + fourC
#
#     temp = D.to_bytes(4, 'big')
#     oneD = str(hex(temp[3])[2:].zfill(2))
#     twoD = str(hex(temp[2])[2:].zfill(2))
#     threeD = str(hex(temp[1])[2:].zfill(2))
#     fourD = str(hex(temp[0])[2:].zfill(2))
#     d_hex = oneD + twoD + threeD + fourD
#
#     hash = a_hex + b_hex + c_hex + d_hex
#
#     return hash


def rotate_bytes(num, col):
    # побитовый сдвиг 4 байтового числа, col положительный -> сдвиг вправо, отрицательный <- влево
    num_bit = list(bin(num)[2:].zfill(32))
    while (len(num_bit) != 32):
        num_bit.pop(0)
    while col!=0:
        if col >= 0:
            tmp = num_bit[31]
            for i in range(31,0,-1):
                num_bit[i] = num_bit[i-1]
            num_bit[0] = tmp
            col -=1
        elif col <0:
            tmp = num_bit[0]
            for i in range(0,31,1):
                num_bit[i] = num_bit[i+1]
            num_bit[31] = tmp
            col +=1
    num_byte = [ int(''.join(num_bit[i+j] for i in range(0,8,1)),2) for j in range(0,32,8)]
    result = int.from_bytes(num_byte,'big')
    return result


def Mod512(text):
    # расширяет текст и делит на блоки по 512 бит
    tmp = text.encode('utf-8')
    if (tmp[len(tmp)-1] == 10):
        text_byte = tmp[0:len(tmp)-1]
    else:
        text_byte = tmp[0:len(tmp)]
    text_bit = [bin(text_byte[i])[2:].zfill(8) for i in range(0, len(text_byte))]
    text_bit.append('10000000')
    while ((len(text_bit)*8) % 512 != 448):
        text_bit.append('00000000')
    tmp = list(bin(len(text_byte*8))[2:].zfill(64))
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

    part512 = [''.join(text_bit[i+j] for i in range(0,64)) for j in range(0,len(text_bit),64)]
    return part512


def BlockTo16word(binpart):
    word16 = []
    for i in range(0,512,32):
        bit1 = ''.join(binpart[i:i+8])
        bit2 = ''.join(binpart[i+8:i+16])
        bit3 = ''.join(binpart[i+16:i+24])
        bit4 = ''.join(binpart[i+24:i+32])
        tmp = bit4 + bit3 + bit2 + bit1
        word16.append(int(tmp, 2))
    return word16


def F(X,Y,Z):
    return ( (X&Y)|((~X)&Z) )


def FF(a,b,c,d,k,s,X):
    a = rotate_bytes((a+F(b,c,d) + X[k]), -s)
    return a


def G(X,Y,Z):
    return ( (X&Y)|(X&Z)|(Y&Z) )


def GG(a,b,c,d,k,s,X):
    a = rotate_bytes((a+G(b,c,d)+X[k]+0x5a827999),-s)
    return a


def H(X,Y,Z):
    return ( X^Y^Z )


def HH(a, b, c, d, k, s, X):
    a = rotate_bytes((a+H(b, c, d)+X[k]+0x6ed9eba1), -s)
    return a


def MD4_generate(text):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    word512 = Mod512(text)
    for i in range(0, len(word512)):

        X = BlockTo16word(word512[i])
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
        #----------------------------------------------------
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
        #-------------------------------------------
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

        A = (A + AA)%(pow(2,32))
        B = (B + BB)%(pow(2,32))
        C = (C + CC)%(pow(2,32))
        D = (D + DD)%(pow(2,32))
    # end -----------------------------------------------------


    tmp = A.to_bytes(4,'big')
    oneA = str(hex(tmp[3])[2:].zfill(2))
    twoA = str(hex(tmp[2])[2:].zfill(2))
    threeA = str(hex(tmp[1])[2:].zfill(2))
    fourA = str(hex(tmp[0])[2:].zfill(2))
    a_hex = oneA + twoA + threeA + fourA

    tmp = B.to_bytes(4, 'big')
    oneB = str(hex(tmp[3])[2:].zfill(2))
    twoB = str(hex(tmp[2])[2:].zfill(2))
    threeB = str(hex(tmp[1])[2:].zfill(2))
    fourB = str(hex(tmp[0])[2:].zfill(2))
    b_hex = oneB + twoB + threeB + fourB

    tmp = C.to_bytes(4, 'big')
    oneC = str(hex(tmp[3])[2:].zfill(2))
    twoC = str(hex(tmp[2])[2:].zfill(2))
    threeC = str(hex(tmp[1])[2:].zfill(2))
    fourC = str(hex(tmp[0])[2:].zfill(2))
    c_hex = oneC + twoC + threeC + fourC

    tmp = D.to_bytes(4, 'big')
    oneD = str(hex(tmp[3])[2:].zfill(2))
    twoD = str(hex(tmp[2])[2:].zfill(2))
    threeD = str(hex(tmp[1])[2:].zfill(2))
    fourD = str(hex(tmp[0])[2:].zfill(2))
    d_hex = oneD + twoD + threeD + fourD

    hash = a_hex + b_hex + c_hex + d_hex
    return hash, a_hex


print(MD4_generate('word'))
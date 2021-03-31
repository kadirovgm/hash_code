import hashlib
import math


# функция для побитового сдвига
def rotate_bytes(number, shift):
    # побитовый сдвиг 4 байтового числа, col положительный -> сдвиг вправо, отрицательный <- влево
    number_bite = list(bin(number)[2:].zfill(32)) # bin преобразует число в двоичную строку и начиная с 2 бита заполняет
    while (len(number_bite) != 32):
        number_bite.pop(0)  # пока длина number_bite не равно 32 бита: считываем нулевый элемент и УДАЛЯЕМ

    while shift != 0:  # пока сдвиг не равен 0
        if shift >= 0:  # если сдвига вправо, сохраняем последний бит
            tmp = number_bite[31]
            for i in range(31, 0, -1):
                number_bite[i] = number_bite[i-1]  # сдвигаем вправо
            number_bite[0] = tmp  # первый бит равен последнему
            shift -= 1  # количество итерации сдвига уменьшается
        elif shift < 0:  # если сдвиг влево, сохраняем первый бит
            tmp = number_bite[0]
            for i in range(0, 31, 1):
                number_bite[i] = number_bite[i+1] # сдвиг влево
            number_bite[31] = tmp  # последний бит равен первому
            shift += 1 # количество итерации сдвига увеличивается
    number_byte = [int(''.join(number_bite[i+j] for i in range(0, 8, 1)), 2) for j in range(0, 32, 8)]
    result = int.from_bytes(number_byte, 'big')  # возвращает целое число, представленное данным массивом байтов
    return result


def extend_mod512(input):
    # расширяет текст и делит на блоки по 512 бит
    tmp = input.encode('utf-8') # переводим текст в кодировку utf-8

    if (tmp[len(tmp)-1] == 10):
        input_byte = tmp[0:len(tmp)-1]
    else:
        input_byte = tmp[0:len(tmp)]

    input_bit = [bin(input_byte[i])[2:].zfill(8) for i in range(0, len(input_byte))]
    input_bit.append('10000000')

    while ((len(input_bit)*8) % 512 != 448):
        input_bit.append('00000000')

    tmp = list(bin(len(input_byte*8))[2:].zfill(64))
    part1 = tmp[0:32]
    part2 = tmp[32:64]

    input_bit.append(''.join(part2[24:32]))
    input_bit.append(''.join(part2[16:24]))
    input_bit.append(''.join(part2[8:16]))
    input_bit.append(''.join(part2[0:8]))

    input_bit.append(''.join(part1[24:32]))
    input_bit.append(''.join(part1[16:24]))
    input_bit.append(''.join(part1[8:16]))
    input_bit.append(''.join(part1[0:8]))

    part512 = [''.join(input_bit[i+j] for i in range(0,64)) for j in range(0,len(input_bit),64)]
    return part512


def block_div16(binpart):
    word16 = []
    for i in range(0, 512, 32):
        bit1 = ''.join(binpart[i:i+8])
        bit2 = ''.join(binpart[i+8:i+16])
        bit3 = ''.join(binpart[i+16:i+24])
        bit4 = ''.join(binpart[i+24:i+32])
        tmp = bit4 + bit3 + bit2 + bit1
        word16.append(int(tmp, 2))
    return word16


def f_func(X, Y, Z):
    return ((X&Y)|((~X)&Z))


def FF_func(a, b, c, d, k, s, X):
    a = rotate_bytes((a + f_func(b, c, d) + X[k]), -s)
    return a


def g_func(X, Y, Z):
    return ((X&Y)|(X&Z)|(Y&Z))


def GG_func(a, b, c, d, k, s, X):
    a = rotate_bytes((a + g_func(b, c, d) + X[k] + 0x5a827999), -s)
    return a


def h_func(X, Y, Z):
    return (X^Y^Z)


def HH_func(a, b, c, d, k, s, X):
    a = rotate_bytes((a + h_func(b, c, d) + X[k] + 0x6ed9eba1), -s)
    return a


def MD4_generate(input):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    word512 = extend_mod512(input)
    for i in range(0, len(word512)):

        X = block_div16(word512[i])
        AA = A
        BB = B
        CC = C
        DD = D
        A = FF_func(A, B, C, D, 0, 3, X)
        D = FF_func(D, A, B, C, 1, 7, X)
        C = FF_func(C, D, A, B, 2, 11, X)
        B = FF_func(B, C, D, A, 3, 19, X)
        A = FF_func(A, B, C, D, 4, 3, X)
        D = FF_func(D, A, B, C, 5, 7, X)
        C = FF_func(C, D, A, B, 6, 11, X)
        B = FF_func(B, C, D, A, 7, 19, X)
        A = FF_func(A, B, C, D, 8, 3, X)
        D = FF_func(D, A, B, C, 9, 7, X)
        C = FF_func(C, D, A, B, 10, 11, X)
        B = FF_func(B, C, D, A, 11, 19, X)
        A = FF_func(A, B, C, D, 12, 3, X)
        D = FF_func(D, A, B, C, 13, 7, X)
        C = FF_func(C, D, A, B, 14, 11, X)
        B = FF_func(B, C, D, A, 15, 19, X)
        #----------------------------------------------------
        A = GG_func(A, B, C, D, 0, 3, X)
        D = GG_func(D, A, B, C, 4, 5, X)
        C = GG_func(C, D, A, B, 8, 9, X)
        B = GG_func(B, C, D, A, 12, 13, X)
        A = GG_func(A, B, C, D, 1, 3, X)
        D = GG_func(D, A, B, C, 5, 5, X)
        C = GG_func(C, D, A, B, 9, 9, X)
        B = GG_func(B, C, D, A, 13, 13, X)
        A = GG_func(A, B, C, D, 2, 3, X)
        D = GG_func(D, A, B, C, 6, 5, X)
        C = GG_func(C, D, A, B, 10, 9, X)
        B = GG_func(B, C, D, A, 14, 13, X)
        A = GG_func(A, B, C, D, 3, 3, X)
        D = GG_func(D, A, B, C, 7, 5, X)
        C = GG_func(C, D, A, B, 11, 9, X)
        B = GG_func(B, C, D, A, 15, 13, X)
        #-------------------------------------------
        A = HH_func(A, B, C, D, 0, 3, X)
        D = HH_func(D, A, B, C, 8, 9, X)
        C = HH_func(C, D, A, B, 4, 11, X)
        B = HH_func(B, C, D, A, 12, 15, X)
        A = HH_func(A, B, C, D, 2, 3, X)
        D = HH_func(D, A, B, C, 10, 9, X)
        C = HH_func(C, D, A, B, 6, 11, X)
        B = HH_func(B, C, D, A, 14, 15, X)
        A = HH_func(A, B, C, D, 1, 3, X)
        D = HH_func(D, A, B, C, 9, 9, X)
        C = HH_func(C, D, A, B, 5, 11, X)
        B = HH_func(B, C, D, A, 13, 15, X)
        A = HH_func(A, B, C, D, 3, 3, X)
        D = HH_func(D, A, B, C, 11, 9, X)
        C = HH_func(C, D, A, B, 7, 11, X)
        B = HH_func(B, C, D, A, 15, 15, X)

        A = (A + AA) % (pow(2, 32))  # остаток от деления на 2^32
        B = (B + BB) % (pow(2, 32))
        C = (C + CC) % (pow(2, 32))
        D = (D + DD) % (pow(2, 32))
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
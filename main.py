import struct
import random
import time
import binascii
import matplotlib.pyplot as plt


# функция для побитового сдвига
def rotate_bytes(number, shift):
    # побитовый сдвиг 4 байтового числа
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


def func_extend_mod512(input):
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


def block_div16(binDiv):  # слова по 32 бит (16 слов)
    word_16 = []
    for i in range(0, 512, 32):  # цикл от 0 до 512 с шагом 32 бита (4 байта)
        bite1 = ''.join(binDiv[i:i + 8])
        bite2 = ''.join(binDiv[i + 8:i + 16])
        bite3 = ''.join(binDiv[i + 16:i + 24])
        bite4 = ''.join(binDiv[i + 24:i + 32])
        tmp = bite4 + bite3 + bite2 + bite1

        word_16.append(int(tmp, 2))
    return word_16


def f_func(X, Y, Z):
    return ((X&Y)|((~X)&Z))


def F_func(a, b, c, d, count, shift, X):  # перевод в обратный порядок битов
    a = rotate_bytes((a + f_func(b, c, d) + X[count]), -shift)
    return a


def g_func(X, Y, Z):
    return ((X&Y)|(X&Z)|(Y&Z))


def G_func(a, b, c, d, count, shift, X):  # перевод в обратный порядок битов
    a = rotate_bytes((a + g_func(b, c, d) + X[count] + 0x5a827999), -shift)
    return a


def h_func(X, Y, Z):
    return (X^Y^Z)


def H_func(a, b, c, d, count, shift, X):  # перевод в обратный порядок битов
    a = rotate_bytes((a + h_func(b, c, d) + X[count] + 0x6ed9eba1), -shift)
    return a


def MD4_generate(input):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    # print("Сообщение считано с файла input[i].txt!")
    mod512_extended_word = func_extend_mod512(input) # расширение сообщения и деление на блоки по 512 бит

    for i in range(0, len(mod512_extended_word)):  # алгоритм, как в методичке: цикл от 0 до длины расширенного сообщения
        X = block_div16(mod512_extended_word[i])  # делим на 16 слов и записываем в X

        AA = A  # сохраняем начальное значение
        BB = B
        CC = C
        DD = D
        ############################################ 1 РАУНД
        A = F_func(A, B, C, D, 0, 3, X)
        D = F_func(D, A, B, C, 1, 7, X)
        C = F_func(C, D, A, B, 2, 11, X)
        B = F_func(B, C, D, A, 3, 19, X)
        A = F_func(A, B, C, D, 4, 3, X)
        D = F_func(D, A, B, C, 5, 7, X)
        C = F_func(C, D, A, B, 6, 11, X)
        B = F_func(B, C, D, A, 7, 19, X)
        A = F_func(A, B, C, D, 8, 3, X)
        D = F_func(D, A, B, C, 9, 7, X)
        C = F_func(C, D, A, B, 10, 11, X)
        B = F_func(B, C, D, A, 11, 19, X)
        A = F_func(A, B, C, D, 12, 3, X)
        D = F_func(D, A, B, C, 13, 7, X)
        C = F_func(C, D, A, B, 14, 11, X)
        B = F_func(B, C, D, A, 15, 19, X)
        ############################################## 2 РАУНД
        A = G_func(A, B, C, D, 0, 3, X)
        D = G_func(D, A, B, C, 4, 5, X)
        C = G_func(C, D, A, B, 8, 9, X)
        B = G_func(B, C, D, A, 12, 13, X)
        A = G_func(A, B, C, D, 1, 3, X)
        D = G_func(D, A, B, C, 5, 5, X)
        C = G_func(C, D, A, B, 9, 9, X)
        B = G_func(B, C, D, A, 13, 13, X)
        A = G_func(A, B, C, D, 2, 3, X)
        D = G_func(D, A, B, C, 6, 5, X)
        C = G_func(C, D, A, B, 10, 9, X)
        B = G_func(B, C, D, A, 14, 13, X)
        A = G_func(A, B, C, D, 3, 3, X)
        D = G_func(D, A, B, C, 7, 5, X)
        C = G_func(C, D, A, B, 11, 9, X)
        B = G_func(B, C, D, A, 15, 13, X)
        ############################################## 3 РАУНД
        A = H_func(A, B, C, D, 0, 3, X)
        D = H_func(D, A, B, C, 8, 9, X)
        C = H_func(C, D, A, B, 4, 11, X)
        B = H_func(B, C, D, A, 12, 15, X)
        A = H_func(A, B, C, D, 2, 3, X)
        D = H_func(D, A, B, C, 10, 9, X)
        C = H_func(C, D, A, B, 6, 11, X)
        B = H_func(B, C, D, A, 14, 15, X)
        A = H_func(A, B, C, D, 1, 3, X)
        D = H_func(D, A, B, C, 9, 9, X)
        C = H_func(C, D, A, B, 5, 11, X)
        B = H_func(B, C, D, A, 13, 15, X)
        A = H_func(A, B, C, D, 3, 3, X)
        D = H_func(D, A, B, C, 11, 9, X)
        C = H_func(C, D, A, B, 7, 11, X)
        B = H_func(B, C, D, A, 15, 15, X)

        A = (A + AA) % (pow(2, 32))  # остаток от деления на 2^32
        B = (B + BB) % (pow(2, 32))
        C = (C + CC) % (pow(2, 32))
        D = (D + DD) % (pow(2, 32))
    ################################################# КОНЕЦ ЦИКЛА

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

    hash_result = a_hex + b_hex + c_hex + d_hex
    return hash_result


def generate_random_string() -> str:
    letters = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+={}[]:"<>?/'
    length = random.randint(2, 100)
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def collision_of_2_random():
    #  Exercise #3
    print("\n------------------Задание 3------------------------")
    print("НАХОЖДЕНИЕ КОЛЛИЗИЙ")
    # hashes = [bytes(generate_random_string().encode()), bytes(generate_random_string().encode())]
    hashes = [MD4_generate(generate_random_string()),
              MD4_generate(generate_random_string())]

    print("Введите число k: ")
    k_max = int(input())
    count = 0
    times = []

    for k in range(1, k_max + 1):
        start_timing = time.time()
        while hashes[0][:k] not in hashes[1]:
            count += 1
            string1 = generate_random_string()
            string2 = generate_random_string()
            hashes = [MD4_generate(string1),
                      MD4_generate(string2)]
        print("k[" + str(k) + "] = " + str(time.time() - start_timing) + " сек.")
        times.append(time.time() - start_timing)
    print(f'Найдена коллизия для следующих хешей: \n{hashes[0]}\n{hashes[1]}\nитератор={count}')
    print("Строка 1: " + str(string1))
    print("Строка 2: " + str(string2))
    plt.plot(range(1, k_max + 1), times)
    plt.show()


def collision_of_pswd():
    #  Exercise #4
    print("\n------------------Задание 4------------------------")
    print("ПОИСК ПРООБРАЗА ДЛЯ ЗАДАННОГО ХЕША")
    print("Введите пароль: ")
    pswd = str(input())
    hash = generate_random_string()

    print(f'Случайный хеш = {MD4_generate(hash)}, \nХеш для пароля {pswd} = {MD4_generate(pswd)}')
    hash_pswd = MD4_generate(pswd)
    hash_rand = MD4_generate(hash)

    print("Введите число k: ")
    k_max = int(input())
    count = 0
    times = []

    for k in range(1, k_max + 1):
        start_timing = time.time()
        while hash_pswd[:k] not in hash_rand:
            count += 1
            proobraz = generate_random_string()
            hash_rand = MD4_generate(proobraz)
            # print(hashes)
        print("k[" + str(k) + "] = " + str(time.time() - start_timing) + " сек.")
        times.append(time.time() - start_timing)
    plt.plot(range(1, k_max + 1), times)
    plt.show()

    print(f'Найдена коллизия для пароля: {pswd}\nХеш пароля: {hash_pswd}\nХеш прообраза: {hash_rand}\nитератор={count}')
    print("Прообраз для пароля " + str(pswd) + ": " + str(proobraz))

def str2hex(s):
    return binascii.hexlify(bytes(str.encode(s)))


def lavin_eff(result, result2):
    print("\n------------------Задание 2------------------------")
    print("ПРОВЕРКА ЛАВИННОГО ЭФФЕКТА")
    print("Хешы в бинарном виде:")

    res_hex = str2hex(result)
    print(res_hex.decode('utf-8'))
    res2_hex = str2hex(result2)
    print(res2_hex.decode('utf-8'))

    res_bin = bin(int(res_hex, 16))
    res2_bin = bin(int(res2_hex, 16))
    print(res_bin)
    print(res2_bin)
    print()

    result = ''.join(format(ord(i), '08b') for i in result)
    result2 = ''.join(format(ord(i), '08b') for i in result2)
    print(result)
    print(result2)

    xor = 0
    for i, j in zip(result, result2):
        xor += int(i) ^ int(j)

    print("Количество разных " + str(xor))


# функция main()

if __name__ == '__main__':

    with open("input.txt") as text_input:
        input_text = text_input.read()
    with open("input_2.txt") as text_input2:
        input_text2 = text_input2.read()

    result = MD4_generate(input_text)  # вызов основной функции хеширования
    result2 = MD4_generate(input_text2)

    with open("hash_output.txt", mode='w') as hash_text:
        hash_text.write(str(result) + "\n" + str(result2))

    print("------------------Задание 1------------------------")
    print("ГЕНЕРАЦИЯ ХЕШЕЙ")
    print("Хеш-для сообщения '" + str(input_text) + "': ")
    print(result)
    print("Хеш-для сообщения '" + str(input_text2) + "': ")
    print(result2)

    # binary_result = [format(int.from_bytes(i.encode(), 'big'), '08b') for i in result]
    # binary_result2 = [format(int.from_bytes(i.encode(), 'big'), '08b') for i in result2]

    # binary_result = ''.join(binary_result)
    # binary_result2 = ''.join(binary_result2)

    # res_bin = "{0:08b}".format(int(result, 16))
    # res2_bin = "{0:08b}".format(int(result2, 16))
    # print(res_bin)
    # print(res2_bin)

    # Task 2
    lavin_eff(result, result2)

    # Task 3
    collision_of_2_random()

    # Task 4
    collision_of_pswd()

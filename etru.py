import random
import binascii

from EisenPolynomial import *
from eCalculate import *

# N (preferably prime)
N = 13

# |q| much larger than | p|,    relatively prime
p = EisensteinIntegers(2, 3)
q = EisensteinIntegers(41, 0)

# init_unit = [[EisensteinIntegers(1, 0), EisensteinIntegers(-1, 0)],
#              [EisensteinIntegers(0, 1), EisensteinIntegers(0, -1)],
#              [EisensteinIntegers(1, 1), EisensteinIntegers(-1, -1)]]

init_unit_pair = [[EisensteinIntegers(1, 0), EisensteinIntegers(0, 1), EisensteinIntegers(-1, -1)],
                  [EisensteinIntegers(-1, 0), EisensteinIntegers(0, -1), EisensteinIntegers(1, 1)]
                  ]

r = 0.9
s = int(r * N) - int(r * N) % 3


# L
def gen_nonzero():
    coe_list = []
    for i in range(0, int(s / 3)):
        choose = random.randint(0, 1)
        for tmp in init_unit_pair[choose]:
            coe_list.append(tmp)
    return coe_list


def Lf():
    nonzero = gen_nonzero()
    nonzero.append(EisensteinIntegers(1, 0))

    for i in range(0, N - len(nonzero)):
        nonzero.append(EisensteinIntegers(0, 0))
    random.shuffle(nonzero)

    poly_f = EisensteinPoly(nonzero)
    list_N = [EisensteinIntegers(1, 0)]
    for i in range(N - 1):
        list_N.append(EisensteinIntegers(0, 0))
    list_N.append(EisensteinIntegers(-1, 0))
    poly_N = EisensteinPoly(list_N)
    # print(ep_toStr(poly_N))

    gcd, u, Fq = ep_Extend_Euclid(poly_N, poly_f, q, N)
    gcd2, u2, Fp = ep_Extend_Euclid(poly_N, poly_f, p, N)
    # print("gcd:"+ep_toStr(gcd))
    # print("u:"+ep_toStr(u))
    # print("v:"+ep_toStr(v))

    if len(gcd) != 1 or len(gcd2) != 1:
        return print("length of gcd1/2 !=1")
    if gcd.list[0].coe_a != 1 or gcd.list[0].coe_b != 0 or gcd2.list[0].coe_a != 1 or gcd2.list[0].coe_b != 0:
        return print("other error")

    return poly_f, Fq, Fp


# Lf()

def Lgfai():
    nonzero = gen_nonzero()
    # nonzero.append(EisensteinIntegers(1, 0))

    for i in range(0, N - len(nonzero)):
        nonzero.append(EisensteinIntegers(0, 0))
    random.shuffle(nonzero)

    poly_gfai = EisensteinPoly(nonzero)

    return poly_gfai


def message_to_binary(m):
    my_bytes = m.encode('utf-8')
    my_binary_string = bin(int(binascii.hexlify(my_bytes), 16))[2:]
    return my_binary_string


def binary_to_message(b):
    return binascii.unhexlify(hex(int(b, 2))[2:]).decode('utf-8')


def poly_Mapping(m):  # M是二进制串str
    if len(m) % 2 == 1:
        m = m + "1"
    else:
        m = m + "10"
    list_coe = []
    count = 0
    while count < len(m):
        coe_a = int(m[count])
        count += 1
        if count < len(m):
            coe_b = int(m[count])
            count += 1
        else:
            coe_b = 0
        eisen = EisensteinIntegers(coe_a, coe_b)
        eisen_r = ess_mod(eisen, p)
        list_coe.append(eisen_r)
    list_coe.reverse()
    poly_M = EisensteinPoly(list_coe)
    return poly_M


def polyToCoe(poly_m):
    res = []
    coe = poly_m.list[0]
    if coe.coe_b == 1:  # 原始信息奇数长度
        res.append(str(int(coe.coe_a)))
    x = poly_m.list[1:]

    for i in range(0, len(x)):
        res.append(str(int(x[i].coe_b)))
        res.append(str(int(x[i].coe_a)))
    res.reverse()
    return ''.join(res)


# # 私钥
# poly_f, Fq, Fp = Lf()
#
# poly_g = Lgfai()
# poly_fai = Lgfai()
# poly_M = poly_Mapping("10011111")
#
# # 公钥
# h = ep_mul(Fq, poly_g, q, N)
#
# # 加密到这里
# tem = ep_mul(EisensteinPoly([p]), poly_fai, q, N)
# e = ep_add(ep_mul(tem, h, q, N), poly_M, q)
# # 加密到这里
# # a=message_to_binary("caonima")
# # print(binary_to_message(a))
#
#
# # 解密到这里
# poly_a = ep_mul(poly_f, e, q, N)
# # 原始信息的多项式
# poly_m = ep_mul(Fp, poly_a, p, N)
# print(polyToCoe(poly_m))




#sample
poly_f, Fq, Fp = Lf()
poly_g = Lgfai()
poly_fai = Lgfai()
h = ep_mul(Fq, poly_g, q, N)
print("原文：QAQ")
zzzz = message_to_binary("QAQ")
print(zzzz)
poly_M = poly_Mapping(zzzz)
tem = ep_mul(EisensteinPoly([p]), poly_fai, q, N)
e = ep_add(ep_mul(tem, h, q, N), poly_M, q)
print("密文：",ep_toStr(e))

poly_a = ep_mul(poly_f, e, q, N)
poly_m = ep_mul(Fp, poly_a, p, N)
print("明文：",ep_toStr(poly_m))


mmmm=polyToCoe(poly_m)
print(mmmm)
print(binary_to_message(mmmm))

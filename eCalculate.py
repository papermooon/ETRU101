from sympy import *


# w = Rational(1, 2) + Rational(1, 2)*sqrt(3)*I

def ess_add(x, y):
    return EisensteinIntegers(x.coe_a + y.coe_a, x.coe_b + y.coe_b)


def ess_sub(x, y):
    return EisensteinIntegers(x.coe_a - y.coe_a, x.coe_b - y.coe_b)


def ess_mul(x, y):
    # (a + bω)(c + dω) = ac − bd + (ad + bc − bd)ω
    a = x.coe_a
    b = x.coe_b
    c = y.coe_a
    d = y.coe_b
    return EisensteinIntegers(a * c - b * d, a * d + b * c - b * d)


# 参数均要为E类
def ess_div(x, y):
    # α = m + nω and q = a + bω
    m = x.coe_a
    n = x.coe_b
    a = y.coe_a
    b = y.coe_b

    e1 = 2 * a - b
    e2 = 2 * b - a
    Q = ess_alt_square(y)
    d = 2 * Q

    # Compute the closest vector on the sublattice L :
    s = m * e1 + n * e2
    t = n * a - m * b

    x0 = arrange(s, d)
    x1 = arrange(t, d)

    r1 = EisensteinIntegers(x0 + x1, 2 * x1)
    B1 = ess_sub(x, ess_mul(y, r1))

    # Compute the closest vector on the coset ω + L :
    s_prime = s + Q
    t_prime = t - Q

    y0 = arrange(s_prime, d)
    y1 = arrange(t_prime, d)

    r2 = EisensteinIntegers(y0 + y1, 2 * y1 + 1)
    B2 = ess_sub(x, ess_mul(y, r2))

    res1 = ess_alt_square(B1)
    res2 = ess_alt_square(B2)

    # print("e1", e1)
    # print("e2", e2)
    # print("Q", Q)
    # print("d", d)
    # print("s", s)
    # print("t", t)
    # print("x0", x0)
    # print("x1", x1)
    # print("r1", r1)
    # print("B1", B1)
    # print("s'", s_prime)
    # print("t'", t_prime)
    # print("y0", y0)
    # print("y1", y1)
    # print("r2", r2)
    # print("B2", B2)

    if res1 < res2:
        return r1, B1
    elif res1 > res2:
        return r2, B2
    elif x0 < y0:
        return r1, B1
    else:
        return r2, B2


def arrange(c, d):
    c_bar = c % d
    if c_bar > abs(d) / 2:
        c_bar -= abs(d)
    elif c_bar <= -abs(d) / 2:
        c_bar += abs(d)
    return (c - c_bar) / d


def ess_alt_square(q):
    c = q.coe_a
    d = q.coe_b
    return c ** 2 + d ** 2 - c * d


# a模q
def ess_mod(a, q):
    r, b = ess_div(a, q)
    return b


# a在模b下的逆元
def ess_reverse(a, b):
    x = ess_mod(a, b)
    y = EisensteinIntegers(b.coe_a, b.coe_b)
    t = EisensteinIntegers(0, 0)
    newt = EisensteinIntegers(1, 0)
    r = EisensteinIntegers(x.coe_a, x.coe_b)
    newr = EisensteinIntegers(y.coe_a, y.coe_b)
    while newr.coe_a != 0:
        quotient = ess_div(r, newr)[1];
        temp = newt;
        newt = t - quotient * newt;
        t = temp;

        temp = newr;
        newr = r - quotient * newr;
        r = temp;
    if r > 1:
        return "no1"
    if t < 0:
        t = t + x;
        return t;
    if t > 0:
        return t;
    return "no2"


# a+b*w
class EisensteinIntegers:
    def __init__(self, coefficient_a, coefficient_b):
        self.coe_a = coefficient_a
        self.coe_b = coefficient_b

    def __str__(self):
        return "%d + %d*w" % (self.coe_a, self.coe_b)

    def __bool__(self):
        if self.coe_a == 0 and self.coe_b == 0:
            return False
        return True


x1 = EisensteinIntegers(2, 1)
y1 = EisensteinIntegers(3, 2)
z1 = ess_add(x1, y1)
z2 = ess_sub(x1, y1)
z3 = ess_mul(x1, y1)
# print(round(1/4,1))
# print(z3)
# print(arrange(11, 20))

x2 = EisensteinIntegers(14, 8)
y2 = EisensteinIntegers(7, 3)
print(ess_mod(x2, y2))
print(ess_mod(ess_mod(x2, y2), y2))

rrr = ess_div(x2, y2)
# b = ess_div(x1, y1)[1]
# print(ess_div(x1, y1)[0])
# print(ess_div(x1, y1)[1])
# print(ess_add(ess_mul(r, y1), b))
#
# from nzmath import *
#
# ressss=arygcd.arygcd_w(14, 8, 7, 4)
# print(ressss)
# print(rrr[0])
# print(rrr[1])
#
# zz=EisensteinIntegers(4, -3)
# rr1=ess_div(x2, zz)
# rr2=ess_div(y2, zz)
#
# print(rr1[0])
# print(rr1[1])
# print(rr2[0])
# print(rr2[1])

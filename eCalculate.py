from nzmath import arygcd
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
    y = EisensteinIntegers(a.coe_a, a.coe_b)
    x = EisensteinIntegers(b.coe_a, b.coe_b)

    t = EisensteinIntegers(0, 0)
    newt = EisensteinIntegers(1, 0)
    r = EisensteinIntegers(x.coe_a, x.coe_b)
    newr = EisensteinIntegers(y.coe_a, y.coe_b)

    # print(x)
    # print(y)
    # print(t)
    # print(newt)
    # print(r)
    # print(newr)

    while newr.coe_a != 0 or newr.coe_b != 0:
        quotient = ess_div(r, newr)[0];

        temp = newt;
        newt = ess_sub(t, ess_mul(quotient, newt))

        t = temp;

        temp = newr;
        newr = ess_sub(r, ess_mul(quotient, newr))
        r = temp;

    print(r)
    if r.coe_b != 0 or r.coe_a > 1:
        return "no1"
    if t.coe_a >= 0:
        return t
    # return ess_add(t, x)
    return ess_mod(t, x)
    # if t < 0:
    #     t = t + x;
    #     return t;
    # if t > 0:
    #     return t;

    # return "no2"


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

x2 = EisensteinIntegers(3, 2)
y2 = EisensteinIntegers(2, 4)


# print(ess_mod(x2,y2))


def check(a, b):
    print("gcd检测：", arygcd.arygcd_w(a.coe_a, a.coe_b, b.coe_a, b.coe_b))
    res = ess_reverse(a, b)
    print(a, "在模", b, "下的逆元为：", res)
    print(ess_mod(ess_mul(res, a), b))
    print(ess_div(ess_mul(a, res), b)[0])
    print(ess_div(ess_mul(a, res), b)[1])


# ess_reverse(x2, y2)
# check(x2, y2)
# print(ess_div(EisensteinIntegers(2,4),EisensteinIntegers(3,2))[0])
# print(ess_div(EisensteinIntegers(2,4),EisensteinIntegers(3,2))[1])
#
# print(ess_div(EisensteinIntegers(3,2),EisensteinIntegers(1,1))[0])
# print(ess_div(EisensteinIntegers(3,2),EisensteinIntegers(1,1))[1])
# print(ess_div(EisensteinIntegers(2, 1), EisensteinIntegers(1, 3))[0])
# print(ess_div(EisensteinIntegers(2, 1), EisensteinIntegers(1, 3))[1])


# from nzmath import *
# ressss=arygcd.arygcd_w(14, 8, 7, 4)


def red(need, mode):
    p0 = EisensteinIntegers(0, 0)
    p1 = EisensteinIntegers(1, 0)

    yushu = EisensteinIntegers(1, 0)

    chushu = mode
    beichu = need

    while yushu.coe_a != 0 or yushu.coe_b != 0:
        last_yushu = yushu
        shang, yushu = ess_div(chushu, beichu)
        P_ans = ess_mod(ess_sub(p0, ess_mul(p1, shang)), mode)
        # P_ans=(p0-p1*shang)mod mode
        print('商：', shang, "被除数", beichu, "余数", yushu, "ans", P_ans)

        p0 = p1
        p1 = P_ans

        # print(shang,yushu)
        chushu = beichu
        beichu = yushu

    # print(yushu)
    # print(last_yushu)
    # print(p0)
    # print(p1)
    # print("最终答案",p0)
    if last_yushu.coe_b != 0:
        return print("错误1")
    if last_yushu.coe_a == 1:
        return print("最终答案", p0)

    if last_yushu.coe_a == -1:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(-1, 0)))
    return print("错误2")


# check(EisensteinIntegers(3, 2), EisensteinIntegers(7, 3))

# print(ess_mod(EisensteinIntegers(-8, - 3), EisensteinIntegers(7, 3)))
#
# re=ess_div(EisensteinIntegers(8, 3), EisensteinIntegers(7, 3))
# print(re[0])
# print(re[1])

def ess_inverse(need, mode):
    if need.coe_a == 1 and need.coe_b == 0:
        return print("最终答案", EisensteinIntegers(1, 0))
    if need.coe_a == -1 and need.coe_b == 0:
        return print("最终答案", EisensteinIntegers(-1, 0))

    if need.coe_a == 0 and need.coe_b == 1:
        return print("最终答案", EisensteinIntegers(-1, -1))
    if need.coe_a == 0 and need.coe_b == -1:
        return print("最终答案", EisensteinIntegers(1, 1))

    if need.coe_a == 1 and need.coe_b == 1:
        return print("最终答案", EisensteinIntegers(0, -1))
    if need.coe_a == -1 and need.coe_b == -1:
        return print("最终答案", EisensteinIntegers(0, 1))

    gcd = arygcd.arygcd_w(need.coe_a, need.coe_b, mode.coe_a, mode.coe_b)
    e_gcd = EisensteinIntegers(gcd[0], gcd[1])
    if ess_alt_square(e_gcd) != 1:
        return print("不可逆")

    p0 = EisensteinIntegers(0, 0)
    p1 = EisensteinIntegers(1, 0)

    yushu = EisensteinIntegers(1, 0)

    chushu = mode
    beichu = need

    while yushu.coe_a != 0 or yushu.coe_b != 0:
        last_yushu = yushu
        shang, yushu = ess_div(chushu, beichu)
        P_ans = ess_mod(ess_sub(p0, ess_mul(p1, shang)), mode)

        print('商：', shang, "被除数", beichu, "余数", yushu, "ans", P_ans)

        p0 = p1
        p1 = P_ans

        chushu = beichu
        beichu = yushu


    if last_yushu.coe_a == 1 and last_yushu.coe_b == 0:
        return print("最终答案", p0)
    if last_yushu.coe_a == -1 and last_yushu.coe_b == 0:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(-1, 0)))

    if last_yushu.coe_a == 0 and last_yushu.coe_b == 1:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(-1, -1)))
    if last_yushu.coe_a == 0 and last_yushu.coe_b == -1:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(1, 1)))

    if last_yushu.coe_a == 1 and last_yushu.coe_b == 1:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(0, -1)))
    if last_yushu.coe_a == -1 and last_yushu.coe_b == -1:
        return print("最终答案", ess_mul(p0, EisensteinIntegers(0, 1)))

    return print("错误")


from sympy import *


# w = Rational(1, 2) + Rational(1, 2)*sqrt(3)*I

def ess_add(x, y):
    return EisensteinIntegers(x.a + y.a, x.b + y.b)


def ess_sub(x, y):
    return EisensteinIntegers(x.a - y.a, x.b - y.b)


def ess_mul(x, y):
    # (a + bω)(c + dω) = ac − bd + (ad + bc − bd)ω
    a = x.a
    b = x.b
    c = y.a
    d = y.b
    return EisensteinIntegers(a * c - b * d, a * d + b * c - b * d)


# a+b*w
class EisensteinIntegers:
    def __init__(self, coefficient_a, coefficient_b):
        self.a = coefficient_a
        self.b = coefficient_b

    def __str__(self):
        return "%d + %d*w" % (self.a, self.b)


x1 = EisensteinIntegers(2, 1)
y1 = EisensteinIntegers(3, 2)
z1 = ess_add(x1, y1)
z2 = ess_sub(x1, y1)
z3 = ess_mul(x1, y1)
print(z1)
print(z3)
# print(x.b)

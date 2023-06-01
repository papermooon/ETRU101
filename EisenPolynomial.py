from sympy import *
import eCalculate as eC
import polynomial

zero = eC.EisensteinIntegers(0, 0)

class EisensteinPoly:
    def __init__(self, list1):
        self.list = list1

    def __len__(self):
        return len(self.list)


#定义系数列表等长的多项式的减法
# 要求输入Ep的list等长
# 返回结果为等长的列表的Ep。
# 计算数域为艾森斯坦数的Nq
def ep_subtraction(ep1, ep2, q):
    a = ep1.list.copy()
    b = ep2.list.copy()
    result = []
    for i in range(len(a)):
        tem = eC.ess_sub(a[i], b[i])
        q, r = eC.ess_div(tem, q)
        result.append(r)
    res_ploy = EisensteinPoly(result)
    return res_ploy


#定义多项式的减法
#不要求输入Ep的list等长
def ep_sub(ep1, ep2, q):
    a = ep1.list.copy()
    b = ep2.list.copy()
    if len(a) < len(b):
        a.list.reverse()
        a.list.extend([zero]*(len(b)-len(a)))
        a.list.reverse()
    elif len(a) > len(b):
        b.list.reverse()
        b.list.extend([zero] * (len(a) - len(b)))
        b.list.reverse()
    epa = EisensteinPoly(a)
    epb = EisensteinPoly(b)
    res_ploy = ep_subtraction(epa, epb, q)
    return res_ploy


#定义多项式的加法，默认参数Ep的list不等长
def ep_add(ep1, ep2, q):
    a = ep1.list.copy()
    b = ep2.list.copy()
    result = []
    if len(a) > len(b):
        b.reverse()
        b.extend([zero] * (len(a) - len(b)))
        b.reverse()
        max = len(a)
    else:
        a.reverse()
        a.extend([zero] * (len(b) - len(a)))
        a.reverse()
        max = len(b)
    for i in range(max):
        tem = eC.ess_add(a[i], b[i])
        q, r = eC.ess_div(tem, q)
        result.append(r)
    for j in range(len(result)):  # 除去列表最左端无意义的0
        if not result[0].bool():
            result.reverse()
            result.pop()
            result.reverse()
        else:
            break
    res_ploy = EisensteinPoly(result)
    return res_ploy


#定义多项式与数的乘法，参数list为被乘的多项式列表，
# a为爱森斯坦数。计算数域为Zq
def ep_multiplication(ep1, a, q):
    result = []
    lista = ep1.list
    for i in range(len(lista)):
        #result.append(lista[i]*a%p)
        tem = eC.ess_mul(lista[i], a)
        q, r = eC.ess_div(tem, q)
        result.append(r)
    res_ploy = EisensteinPoly(result)
    return res_ploy


#定义多项式与多项式的乘法
def ep_mul(ep1, ep2, q):
    epa = EisensteinPoly(ep1.list)
    epb = EisensteinPoly(ep2.list)
    a = epa.list
    b = epb.list
    ep_result = EisensteinPoly([zero])
    for i in range(len(b)):
        ep_product = ep_multiplication(epa, b[i], q)
        ep_product.list.extend([zero]*(len(b)-1-i))
        ep_result = ep_add(ep_result, ep_product, q)
    return ep_result



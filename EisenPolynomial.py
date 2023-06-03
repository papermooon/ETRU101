from sympy import *
import eCalculate as eC
import polynomial

zero = eC.EisensteinIntegers(0, 0)
one = eC.EisensteinIntegers(1, 0)

class EisensteinPoly:
    def __init__(self, list1):
        self.list = list1

    def __len__(self):
        return len(self.list)


def ep_toStr(ep):
    res = "["
    for i in range(len(ep.list)):
        str_tem = str(ep.list[i].coe_a) + "+" + str(ep.list[i].coe_b) + "w"
        res = res + str_tem
        if i != len(ep.list)-1:
            res = res + ","
    res = res + "]"
    return res


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
        quo, r = eC.ess_div(tem, q)
        result.append(r)
    res_ploy = EisensteinPoly(result)
    return res_ploy


#定义多项式的减法
#不要求输入Ep的list等长
def ep_sub(ep1, ep2, q):
    a = ep1.list.copy()
    b = ep2.list.copy()
    if len(a) < len(b):
        a.reverse()
        a.extend([zero]*(len(b)-len(a)))
        a.reverse()
    elif len(a) > len(b):
        b.reverse()
        b.extend([zero] * (len(a) - len(b)))
        b.reverse()
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
        quo, r = eC.ess_div(tem, q)
        result.append(r)
    for j in range(len(result)):  # 除去列表最左端无意义的0
        if not result[0].judge():
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
        quo, r = eC.ess_div(tem, q)
        result.append(r)
    res_ploy = EisensteinPoly(result)
    return res_ploy


#定义多项式与多项式的乘法
def ep_mul(ep1, ep2, q, N):
    epa = EisensteinPoly(ep1.list)
    epb = EisensteinPoly(ep2.list)
    a = epa.list
    b = epb.list
    ep_result = EisensteinPoly([zero])
    for i in range(len(b)):
        ep_product = ep_multiplication(epa, b[i], q)
        ep_product.list.extend([zero]*(len(b)-1-i))
        if len(ep_product.list) > N:
            t = len(ep_product.list) - N
            for j in range(t):
                tem = eC.ess_add(ep_product.list[j+N], ep_product.list[j])
                quo, ep_product.list[j + N] = eC.ess_div(tem, q)
            ep_product.list.reverse()
            for k in range(t):
                ep_product.list.pop()
            ep_product.list.reverse()
        ep_result = ep_add(ep_result, ep_product, q)
        #print("第"+str(i)+"次循环ep_result:"+ep_toStr(ep_result))
    # for i in range(len(ep_result)):
    #     quo, ep_result.list[i] = eC.ess_div(ep_result.list[i], q)
    #print("返回的ep_result:" + ep_toStr(ep_result))
    return ep_result


#实现多项式带余除法,参数均为多项式，(ep1次数更大，a%b的a）
# 返回多项式商q的多项式与余式r的多项式
def ep_div(ep1, ep2, q):
    #此处注意要深拷贝，浅拷贝会修改传进来的参数值
    r = ep1.list.copy()
    b = ep2.list.copy()
    #print("div开始，r："+str(r))
    #print("div开始，b："+str(b))
    if len(r) < len(b):
        return EisensteinPoly([zero]), ep1
    quo = [zero]*(len(r)-len(b)+1)
    #print("q:" + str(q))
    for i in range(len(quo)):
        if len(r) >= len(b):
            index = len(r)-len(b)+1       #确定所得商是商式的第index位
            #print("index:" + str(index))
            print("b[0]:", b[0],", q:",q)
            rev=eC.ess_inverse(b[0], q)
            print("b[0]reverse:", rev)
            tem = eC.ess_mul(r[0], rev)
            qtem, quo[-index] = eC.ess_div(tem, q)
            # 更新被除多项式
            b_tem = b.copy()
            b_tem.extend([zero] * (len(r) - len(b)))
            ep_b_tem = ep_multiplication(EisensteinPoly(b_tem), quo[i], q)
            #print("乘积 b_tem:" + str(b_tem))
            ep_r = ep_sub(EisensteinPoly(r), ep_b_tem, q)
            #print("减后 r:" + str(r))
            for j in range(len(ep_r)):     #除去列表最左端无意义的0
                if not ep_r.list[0].judge():
                    ep_r.list.reverse()
                    ep_r.list.pop()
                    ep_r.list.reverse()
                else:
                    break
            r = ep_r.list
            #print("去0后 r:" + str(r))
        else:
            break
    return EisensteinPoly(quo), EisensteinPoly(r)


#扩展欧几里得算法，输入两个多项式实例，一般ep1次数更高
# 返回二者的最大公因式列表d，以及满足d=u*ep1+v*ep2的u和v
#ep_d为1时，ep_v就是ep2的逆元
def ep_Extend_Euclid(ep1, ep2, q, N):
    epf = EisensteinPoly(ep1.list)
    epg = EisensteinPoly(ep2.list)
    ep_u_2 = EisensteinPoly([one])
    ep_u_1 = EisensteinPoly([zero])
    ep_v_2 = EisensteinPoly([zero])
    ep_v_1 = EisensteinPoly([one])
    ep_quo, ep_r = ep_div(epf, epg, q)
    if ep_r.list==[]:
        ep_d, ep_u, ep_v = epg, [0], [1]
        return ep_d, ep_u, ep_v
    while(ep_r.list!= []):
        print("循环中ep_quo:" + ep_toStr(ep_quo)+",\n循环中ep_r:" + ep_toStr(ep_r))
        tem1 = ep_mul(ep_quo, ep_u_1, q, N)
        ep_u = ep_sub(ep_u_2, tem1, q)
        print("循环中ep_u:" + ep_toStr(ep_u))
        tem2 = ep_mul(ep_quo, ep_v_1, q, N)
        ep_v = ep_sub(ep_v_2, tem2, q)
        print("循环中ep_v:" + ep_toStr(ep_v))
        epf, epg = epg, ep_r
        ep_u_2, ep_u_1 = ep_u_1, ep_u
        ep_v_2, ep_v_1 = ep_v_1, ep_v
        print("循环中epg:" + ep_toStr(epg))
        ep_quo, ep_r = ep_div(epf, epg, q)
    if len(epg)==1:
        r_inverse = eC.ess_inverse(epg.list[0], q)
        ep_u_1 = ep_multiplication(ep_u_1, r_inverse, q)
        ep_v_1 = ep_multiplication(ep_v_1, r_inverse, q)
        epg.list=[eC.EisensteinIntegers(1,0)]

    ep_d, ep_u, ep_v = epg, ep_u_1, ep_v_1
    return ep_d, ep_u, ep_v


def test():
    q1 = int(input("请输入q(形如a+bw)的a："))
    q2 = int(input("请输入q(形如a+bw)的b："))
    q = eC.EisensteinIntegers(q1, q2)
    N = int(input("请输入卷积多项式的N值："))

    # eisen1=eC.EisensteinIntegers(1,0)
    # eisen2=eC.EisensteinIntegers(0,0)
    # ep1 = EisensteinPoly([one, zero, zero, zero, zero, one])#[1,0,0,0,0,-1]
    # ep2 = EisensteinPoly([one, zero, zero, one, one])#[1,0,0,1,1]

    ep1 = EisensteinPoly([eC.EisensteinIntegers(1, 0), eC.EisensteinIntegers(0, 0),
                          eC.EisensteinIntegers(0, 0), eC.EisensteinIntegers(0, 0),
                          eC.EisensteinIntegers(0, 0), eC.EisensteinIntegers(0, 0),
                          eC.EisensteinIntegers(0, 0),eC.EisensteinIntegers(-1, 0)])  # [-1,4,0,-2,1]
    ep2 = EisensteinPoly([eC.EisensteinIntegers(0, -1), eC.EisensteinIntegers(1, 0),
                          eC.EisensteinIntegers(1, 0), eC.EisensteinIntegers(-1, 0),
                          eC.EisensteinIntegers(1, 1), eC.EisensteinIntegers(-1, -1),
                          eC.EisensteinIntegers(0, 1)])  # q=2+3w,N=7
    ep2 = EisensteinPoly([eC.EisensteinIntegers(1, 0), eC.EisensteinIntegers(0, 1),
                          eC.EisensteinIntegers(0, -1), eC.EisensteinIntegers(1, 0),
                          eC.EisensteinIntegers(-1, -1), eC.EisensteinIntegers(-1, 0),
                          eC.EisensteinIntegers(1, 1)])  # x^6+(w)x^5+(-w)x^4+x^3+(-1-w)x^2+(-1)x+1+w

    # mul = ep_mul(ep1, ep2, q, N)
    # print("mul：" + ep_toStr(mul))
    d, u, v = ep_Extend_Euclid(ep1, ep2, q, N)
    print("gcd："+ep_toStr(d))
    print("最大公因式可表示为：" + ep_toStr(d) +
          "\n=(" + ep_toStr(u) + ")(" + ep_toStr(ep1) +
          ")\n+(" + ep_toStr(v) + ")(" + ep_toStr(ep2) + ")")

    mul = ep_mul(v, ep2, q, N)
    print("mul:",ep_toStr(mul))
    #q,r=Division(mul,[1,0,0,0,0,0,0,-1],41)
    quo,r= ep_div(mul, ep1, q)
    print("r:",ep_toStr(r))


if __name__ == '__main__':
    test()
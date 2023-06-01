"""
在Zp域上实现模多项式求逆
Date:2019/12/24
@author:Zhai
"""

#提取多项式的方幂信息及对应系数，返回对应列表，形如：[2,3,1,0,1]对应多项式2x^4+3x^3+x^2+1
def extract_info(str_polynimial):
    length=len(str_polynimial)
    add=1       #记录加号位置
    for i in range(length):
        if i==0:        #获取x的最高次幂指数及其系数
            j=0
            while(j!=length and str_polynimial[j]!='x'):
                j+=1
            if j+1==length or str_polynimial[j+1]!='^':
                index_list = [0] *2
                str_coefficient = "".join([str(item) for item in str_polynimial[0:j]])
                if str_coefficient=="":
                    str_coefficient='1'
                index=1
                index_list[index] = int(str_coefficient)
            elif str_polynimial[j+1]=='^':
                k=j+2
                while(k!=length and str_polynimial[k]!='+' and str_polynimial[k]!='-'):
                    k+=1
                str_index = "".join([str(item) for item in str_polynimial[j+2:k]])
                highest_index = int(str_index)  # 获取最高次幂指数
                index_list = [0] * (highest_index + 1)
                index = highest_index
                if j == 0:  # 首项系数为1的情况下
                    index_list[index] = 1
                else:
                    str_coefficient = "".join([str(item) for item in str_polynimial[0:j]])
                    index_list[index] = int(str_coefficient)#系数为-时会报错

        elif str_polynimial[i]!='+' and str_polynimial[i]!='-':
            continue
        else:
            j = i
            while (j!=length and str_polynimial[j] != 'x'):
                j += 1
            #截取x某一方幂前的系数
            str_coefficient = "".join([str(item) for item in str_polynimial[i+1:j]])
            if str_coefficient=="":     #如果str_coefficient未截取到字符串，证明该项系数为1，令str_coefficient='1'
                str_coefficient='1'
            if str_polynimial[i]=='-':      #如若系数为负，更正系数
                str_coefficient="-"+str_coefficient
            #下面确定并截取x的方幂次数
            if j==length:       #如果已遍历至字符串末位，证明x对应方幂为0
                str_index='0'
            elif (j+1)==length or str_polynimial[j+1]=='+'or str_polynimial[j+1]=='-':        #如果x紧接着的字符为’+‘或此时x为最后一个字符，则证明该x对应的方幂次数为1
                str_index = '1'
            else:
                k=j+2
                while(k!=length and str_polynimial[k]!='+' and str_polynimial[k]!='-'):
                    k+=1
                #while语句执行完后，str_polynimial[k]='+'
                str_index="".join([str(item) for item in str_polynimial[j+2:k]])        #截取x对应的方幂次数
            #修改列表对应参数
            index_list[int(str_index)]=int(str_coefficient)
    index_list.reverse()
    return index_list

#将列表转换为多项式，如[2,1,0,12]将被转换为字符串"2x^3+x^2+12"
def translation(list):
    str_polynimial=""
    for i in range(len(list)):
        if list[i]==0:
            continue
        index=len(list)-i-1       #获取方幂次数
        coefficient=list[i]       #获取对应x某一方幂的系数
        if index==0:
            string=str(coefficient)
        elif index==1:
            if coefficient==1:
                string = 'x'
            else:
                string=str(coefficient)+'x'
        else:
            if coefficient==1:
                string = 'x' + '^' + str(index)
            else:
                string=str(coefficient)+'x'+'^'+str(index)
        if i==0 or list[i]<0:
            str_polynimial=str_polynimial+string
        elif list[i]>0:
            str_polynimial=str_polynimial+'+'+string

    if str_polynimial=="":
        str_polynimial="0"
    return str_polynimial


#定义多项式列表表示的减法，要求参数list1与list2等长，返回结果仍为等长的列表。计算数域为Zp
def Subtraction(list1,list2,p):
    a=list1.copy()
    b=list2.copy()
    result=[]
    for i in range(len(a)):
        result.append((a[i]-b[i])%p)
    return result

#计算数域为Zp
def Subtraction2(list1,list2,p):
    a=list1.copy()
    b=list2.copy()
    if len(a)<len(b):
        a.reverse()
        a.extend([0]*(len(b)-len(a)))
        a.reverse()
    elif len(a)>len(b):
        b.reverse()
        b.extend([0] * (len(a) - len(b)))
        b.reverse()
    result=Subtraction(a,b,p)
    return result

#定义多项式的加法，默认参数list1、list2不等长
def Add(list1,list2,p):
    a=list1.copy()
    b=list2.copy()
    result=[]
    if len(a)>len(b):
        b.reverse()
        b.extend([0]*(len(a)-len(b)))
        b.reverse()
        max=len(a)
    else:
        a.reverse()
        a.extend([0]*(len(b)-len(a)))
        a.reverse()
        max=len(b)
    for i in range(max):
        result.append((a[i]+b[i])%p)
    for j in range(len(result)):  # 除去列表最左端无意义的0
        if result[0] == 0:
            result.remove(0)
        else:
            break
    return result

#定义多项式列表与数的乘法，参数list为被乘的多项式列表，a为int型的乘数。计算数域为Zp
def Multiplication(list,a,p):
    result=[]
    for i in range(len(list)):
        result.append(list[i]*a%p)
    return result

#定义多项式与多项式的乘法，参数list1，list2均为多项式的列表表示法。计算数域为Zp
def Multiplication2(list1,list2,p,N):
    a=list1.copy()
    b=list2.copy()
    result=[0]
    for i in range(len(b)):
        product=Multiplication(a,b[i],p)
        product.extend([0] * (len(b) - 1 - i))
        #print("改前product[" + str(i) + "]:" + str(product))
        if len(product) > N:
            t= len(product) - N
            for j in range(t):
                product[j+N] = (product[j+N] +product[j])%p
            product.reverse()
            for k in range(t):
                product.pop()
            product.reverse()
        #print("改后product[" + str(i) + "]:" + str(product))
        result=Add(result,product,p)

    return result


#扩展欧几里得算法，输入两个多项式列表list1、list2，返回二者的最大公因式列表d，以及满足d=u*list1+v*list2的u和v
#默认list1、list2不等于0
def Extend_Euclid(list1,list2,p,N):
    f=list1.copy()
    g=list2.copy()
    u_2=[1]
    u_1=[0]
    v_2=[0]
    v_1=[1]
    while(g!=[]):
        q,r=Division(f,g,p)
        u=Subtraction2(u_2,Multiplication2(q,u_1,p,N),p)
        v=Subtraction2(v_2,Multiplication2(q,v_1,p,N),p)
        f,g=g,r
        u_2,u_1=u_1,u
        v_2,v_1=v_1,v

    d,u,v=f,u_2,v_2
    return d,u,v


def inverse_mod(a, q):
    """
    计算模q环中a的模反元素
    参数：    a: 要计算模反元素的数    q: 模数
    返回值：    a在模q环中的模反元素
    """
    for x in range(1, q):
        if (a * x) % q == 1:
            return x
    return None


#实现多项式带余除法,参数list1、list2均为列表，返回多项式商q的列表与余式r的列表
def Division(list1,list2,p):#(list1次数更大，a%b的a）
    #此处注意要深拷贝，浅拷贝会修改传进来的参数值
    r=list1.copy()
    b=list2.copy()
    #print("div开始，r："+str(r))
    #print("div开始，b："+str(b))
    length=len(r)       #记录初始被除多项式位数
    if len(r)<len(b):
        return [0],list1
    q=[0]*(len(r)-len(b)+1)
    #print("q:" + str(q))
    for i in range(len(q)):
        if len(r)>=len(b):
            index = len(r)-len(b)+1       #确定所得商是商式的第index位
            #print("index:" + str(index))
            #q[-index] = int((r[0] / b[0])%p)#  增加%p！！！
            q[-index] = (r[0] * inverse_mod(b[0], p)) % p
            # 更新被除多项式
            b_=b.copy()
            b_.extend([0] * (len(r) - len(b)))
            b_=Multiplication(b_,q[i],p)
            #print("乘积 b_:" + str(b_))
            r = Subtraction(r ,b_,p)
            #print("减后 r:" + str(r))
            for j in range(len(r)):     #除去列表最左端无意义的0
                if r[0]==0:
                    r.remove(0)
                else:
                    break
            #print("去0后 r:" + str(r))
        else:
            break
    return q,r


#整数下求gcd
#e.g.list1 = [1, 0, 0, 0, 0, -1]
# list2 = [1, 0, 2, -3]
# p=13
# gcd： [9, 4]
def gcd(list1, list2, p):
    if list2 == []:
        return list1
    else:
        q, r = Division(list1, list2, p)
        #print("商q:"+str(q)+"，余数："+str(r))
        return gcd(list2, r, p)

#整数域求list2 对list1在模p下的逆元
#e.g.list1 = [1, 0, 0, 0, 0, -1]
# list2 = [1, 0, 0, 1, 1]
# p=2
# 逆元： [1, 1, 0, 1]
def get_inverse(list1,list2,p,N): #list2的逆元
    f = list1.copy()
    g = list2.copy()
    if gcd(f, g, p) != [1]:
        print("gcd！=1,逆元不存在")
        return None
    p0 = [0]
    p1 = [1]
    p2 = [0]#不存在逆元
    while(True):
        q, r = Division(f, g, p)
        #print("q:"+str(q)+"r"+str(r))
        if r == []:
            break
        #print("开始乘")
        tem = Multiplication2(p1, q, p,N)
        p2 = Subtraction2(p0, tem, p)
        str_p2 = translation(p2)
        #print("p2:" + str_p2)
        f = g
        g = r
        p0 = p1
        p1 = p2
    if p2 == [0]:
        print("逆元不存在")
        return
    else:
        return p2




def test():
    p = int(input("请输入多项式计算数域Zp的p值："))
    N = int(input("请输入卷积多项式的N值："))
    # # str_polynimial = input("请输入模的多项式(形如2x^4+3x^3+x^2+1)：")#a%b的a
    # # list1 = extract_info(str_polynimial)
    # list1 = [1, 0, 0, 0, 0, -1]
    # str1 = translation(list1)
    # # str_modular = input("请输入被模的多项式(形如2x^4+3x^3+x^2+1)：")#a%b的b
    # # list2 = extract_info(str_modular)
    # #list2 = [1, 0, 2, -3]#p=13,gcd!=1时
    # list2 = [1, 0, 0, 1, 1]#p=2
    # #list3 = Subtraction2(list1, list2, p)
    # #print(list3)
    # str2 = translation(list2)
    # q, r = Division(list1,list2 ,p)
    # str_q = translation(q)
    # str_r = translation(r)
    # print("两式做带余除法，商式为："+str_q + "，余式为：" + str_r)
    # list_gcd = gcd(list1, list2, p)
    # str_gcd = translation(list_gcd)
    # print("上述两多项式的最大公因式为" + str_gcd)
    # list_inverse = get_inverse(list1, list2, p,N)
    # if list_inverse!=None:
    #     str_inverse = translation(list_inverse)
    #     print(str2 + "在模" + str1 + "的情况下，存在逆元：" + str_inverse)
    # d,u,v=Extend_Euclid(list1,list2,p, N)
    # str_d=translation(d)
    # str_u=translation(u)
    # str_v=translation(v)
    # print("上述两多项式的最大公因式为"+str_d )
    # print("最大公因式可表示为："+str_d+"=("+str_u+")("+str1+")+("+str_v+")("+str2+")")
    # if d==[1]:
    #     print(str2 + "在模" + str1 + "的情况下，存在逆元：" + str_v)
    # list3 = [1,0,0,1,1]#N=5,p=2,乘积应该为[1]
    # list4=[1,1,0,1]
    # res=Multiplication2(list3,list4,p,N)
    # print("乘积:" + str(res))
    # list5=[1]
    # list6=[3]
    # w,e,list7=Extend_Euclid(list5,list6,13,5)
    # print("gcd:"+str(list7))
    r=[2,0,2,-3]
    b=[3,4,6]
    t1=(r[0] * inverse_mod(b[0], p)) % p
    print("应该上:" + str(t1))


# for i in range(100):
#      test()
#      print("\n")
if __name__ == '__main__':
    test()

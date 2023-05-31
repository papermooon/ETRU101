import random
#try
# 扩展欧几里得算法
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = extended_gcd(b, a % b)
        return gcd, y, x - (a // b) * y

# 模反元素
def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("不存在模反元素.")
    return x % m

# 密钥生成
def key_generation(N):
    # 选择一个私钥 f，确保 f 是 L_f 中的可逆元素
    while True:
        f = [random.choice([0, 1, -1]) for _ in range(N)]
        if is_invertible(f, N):
            break
    # 计算公钥 h
    h = invert(f, N)
    return f, h

# 检查 f 是否为可逆元素
def is_invertible(f, N):
    # 计算 f 的范数
    f_norm = sum([abs(coeff)**2 for coeff in f])
    return f_norm % 3 != 0

# 计算 f 的逆元素
def invert(f, N):
    f_norm = sum([abs(coeff)**2 for coeff in f])  # 计算 f 的范数
    f_norm_inverse = mod_inverse(f_norm, 3)  # 计算范数的逆元素
    h = [(coeff * f_norm_inverse) % 3 for coeff in f]  # 计算逆元素 h
    return h

# 加密
def encrypt(message, h, N):
    m = binary_to_polynomial(message, N)  # 将二进制消息转换为多项式 m
    c = [random.choice([0, 1, -1]) for _ in range(N)]  # 初始化密文 c
    for i in range(N):
        c[i] += m[i] * h[i]  # 计算密文
    return c

# 解密
def decrypt(c, f, N):
    m = [(coeff % 3) for coeff in c]  # 计算明文 m
    message = polynomial_to_binary(m, N)  # 将多项式转换为二进制消息
    return message

# 将二进制消息转换为多项式
def binary_to_polynomial(message, N):
    binary_list = [int(bit) for bit in message]
    m = []
    for i in range(N):
        if i < len(binary_list):
            m.append(binary_list[i])
        else:
            m.append(0)
    return m

# 将多项式转换为二进制消息
def polynomial_to_binary(m, N):
    binary_list = []
    for coeff in m:
        if coeff == 1:
            binary_list.append('1')
        elif coeff == -1:
            binary_list.append('0')
    message = ''.join(binary_list)
    return message

# 测试
N = 8  # Eisenstein整数环的大小
message = "11011011"  # 要加密的消息
print("原始消息:", message)

# 密钥生成
f, h = key_generation(N)
print("私钥 f:", f)
print("公钥 h:", h)

# 加密
ciphertext = encrypt(message, h, N)
print("加密后的密文:", ciphertext)

# 解密
decrypted_message = decrypt(ciphertext, f, N)
print("解密后的消息:", decrypted_message)



def to_base_2_32(num):
    base = 2 ** 32
    result = []
    while num > 0:
        digit = num % base
        num //= base
        result.append(digit)
        if num == 0:
            break
    return result

def hex_to_blocks(hex_value, base=2**32):
    r = int(hex_value, 16)
    blocks = []
    while r > 0:
        blocks.append(r % base)
        r //= base
    return blocks

def blocks_to_number(blocks, base=2**32):
    num = 0
    for i, block in enumerate(blocks):
        num = num + block * (base ** i)
    return hex(num)

def LongAdd(A, B, w = 32):
    n = max(len(A), len(B))
    C = [0] * n
    carry = 0
    for i in range(n):
        a_i = A[i] if i < len(A) else 0
        b_i = B[i] if i < len(B) else 0
        temp = a_i + b_i + carry
        C[i] = temp & (2**w - 1)
        carry = temp >> w
    return C

def LongSub(A, B, w=32):
    n = max(len(A), len(B))
    C = [0] * n
    borrow = 0
    for i in range(n):
        a_i = A[i] if i < len(A) else 0
        b_i = B[i] if i < len(B) else 0
        temp = a_i - b_i - borrow
        if temp >= 0:
            C[i] = temp
            borrow = 0
        else:
            C[i] = (1 << w) + temp
            borrow = 1
    return C

def LongCmp(A, B):
    n = max(len(A), len(B))
    A = A + [0] * (n - len(A))
    B = B + [0] * (n - len(B))
    i = n - 1
    while i >= 0:
        if A[i] > B[i]:
            return 1
        elif A[i] < B[i]:
            return -1
        i -= 1
    return 0

def LongMulOneDigit(A, b):
    n = len(A)
    C = [0] * (n + 1)
    carry = 0
    for i in range(n):
        temp = A[i] * b + carry
        C[i] = temp & (2 ** 32 - 1)
        carry = temp >> 32
    C[n] = carry
    while C and C[-1] == 0:
        C.pop()
    return C

def LongShiftDigitsToHigh(A, shift):
    n = len(A)
    C = [0] * (n + shift)

    for i in range(n):
        C[i + shift] = A[i]
    return C

def LongMul(A, B):
    n = len(B)
    C = [0] * (2 * n)
    for i in range(n):
        temp = LongMulOneDigit(A, B[i])
        temp = LongShiftDigitsToHigh(temp, i)
        C = LongAdd(C, temp)
    return C

def BitLength(n):
    if n == 0:
        return 0
    return len(bin(n)) - 2

def LongShiftBitsToHigh(num, shift):
    return num << shift

def LongDivMod(A, B):
    if B == 0:
        raise ValueError("Division by zero")
    k = BitLength(B)
    R = A
    Q = 0
    while R >= B:
        t = BitLength(R)
        C = LongShiftBitsToHigh(B, t - k)
        if R < C:
            t = t - 1
            C = LongShiftBitsToHigh(B, t - k)
        R = R - C
        Q = Q + (1 << (t - k))
    return Q, R

def LongPowerWindow(A, B):
    C = [1]
    D = [[1], A]

    beta = 2**32
    for i in range(2, beta):
        D.append(LongMul(D[i - 1], A))
    m = len(B) * 32
    for i in range(m - 1, -1, -1):
        b_i = (B[i // 32] >> (i % 32)) & 1
        if b_i:
            C = LongMul(C, D[b_i])
        if i != 0:
            for j in range(beta):
                C = LongMul(C, C)
    return C

def gcd_and_lcm(A, B):
    original_A, original_B = A, B
    d = 1
    while A % 2 == 0 and B % 2 == 0:
        A //= 2
        B //= 2
        d *= 2
    while A % 2 == 0:
        A //= 2
    while B != 0:
        while B % 2 == 0:
            B //= 2
        A, B = min(A, B), abs(A - B)
    gcd = d * A
    lcm = (original_A // gcd) * original_B
    return gcd, lcm

def KillLastDigits(x, counter):
    k = len(x)
    if k < counter:
        return [0]
    return x[counter:]

def ComputeMU(n):
    """Обчислює μ для алгоритму Барретта"""
    k = len(n)
    beta_2k = [0] * (2 * k) + [1]
    beta_2k_as_number = int(blocks_to_number(beta_2k), 16)
    n_as_number = int(blocks_to_number(n), 16)
    mu = beta_2k_as_number // n_as_number
    return to_base_2_32(mu)

def BarrettReduction(x, n, mu):
    k = len(n)
    #print(f'k = {k}')
    q = KillLastDigits(x, k - 1)
    #print(f'q1 = {q}')
    q = LongMul(q, mu)
    #print(f'q2 = {q}')
    q = KillLastDigits(q, k + 1)
    #print(f'q3 = {q}')
    qn = LongMul(q, n)
    #print(f'qn = {qn}')
    if len(qn) > len(x):
        qn = qn[:len(x)]
    r = LongSub(x, qn)
    #print(f'r1 = {r}')
    while LongCmp(r, n) >= 0:
        r = LongSub(r, n)
    return r

def LongAddMod(A, B, n, mu):
    C = LongAdd(A, B)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongSubMod(A, B, n, mu):
    C = LongSub(A, B)
    if LongCmp(C, [0]) < 0:
        C = LongAdd(C, n)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongMulMod(A, B, n, mu):
    C = LongMul(A, B)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongMulSquareMod(A, n, mu):
    C = LongMul(A, A)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n


def LongModPowerBarrett1(A, B, N):
    c = [1]
    counter = 0
    if LongCmp(A, N) > 0:
        A = BarrettReduction(A, N, mu)
    for i in B:
        if i == 1:
            c = BarrettReduction(c*A, N, mu)
        A = BarrettReduction(A*A, N, mu)
        counter += 1
        print(counter)
    return c


def LongModPowerBarrett(A, B, N):
    if isinstance(N, int):
        N = to_base_2_32(N)
    if isinstance(B, int):
        B = [int(bit) for bit in bin(B)[2:]]
    mu = ComputeMU(N)
    c = [1]
    if LongCmp(A, N) > 0:
        A = BarrettReduction(A, N, mu)
    for bit in reversed(B):
        if bit == 1:
            c = LongMulMod(c, A, N, mu)
        A = LongMulSquareMod(A, N, mu)
    return c


g = 0x80307b356ca65d93e9aba1a011901a8f858da76cac9995519cc5287887fdfa8b114da61f5b3f7e0bf02a3a96d3d3711f6b8f3f7ee4387fcda20d52ddacc4cfa72cd98b6b7360d037a7c8325cc25e7450ed4eb4e7c3d75a567f982584a438028b20397fc3f0c66e6682559d669fb22d12ca72c82965701370ee6c9e556c897569
f = 0x47293d9cf232ebcbf2bfafed458903bbc8f02f9d3083bb5dc405cc0f659e833fa90d597bc79c4396fad89e16f655410de3c54caba4b2a96cf6555a05b5b6d93018b2636169522b048ebe7563e42ee2307700c87ab2935dab71431a70e34f96f46abba42cb7cf8ab6c97f1d636b2216641063c305291639a377dcc0e4af8f5e5d
m = 0xa4519ca8fba424765f1b795e4ddbbc89e022c84ded4523d54a7fb881097305a196fc85b6f4f765a97d3ff30af17824a6d6dc2a91d181065df345ceb72144ea7d310563c5b72c155850617102b3e1179b942dfc05303e314c8649698c26102f4bab2b1444a08d215e60c561ff47bc14da6a5895bbdd3b473575afadbb15d962f5
base = 2**32
gg = to_base_2_32(g)
ff = to_base_2_32(f)
mm = to_base_2_32(m)
b1 = [int(bit) for bit in bin(f)[2:]]
mu = ComputeMU(mm)
print()
#print('gcd: ' + blocks_to_number(gcd_and_lcm(gg, ff)[0]))#ok
print()
#print('lcm: ' + blocks_to_number(gcd_and_lcm(gg, ff)[1]))#ok
print()
print('barrettReduction: ' + blocks_to_number(BarrettReduction(gg, ff, mu)))#ok
print()
print('longModAddBarrett: ' + blocks_to_number(LongAddMod(gg, ff, mm, mu)))
print()
print('longModSubBarrett: ' + blocks_to_number(LongSubMod(gg, ff, mm, mu)))
print()
print('longModMulBarrett: ' + blocks_to_number(LongMulMod(gg, ff, mm, mu)))
print()
print('longModSquarePowerBarrett: ' + blocks_to_number(LongMulSquareMod(gg, mm, mu)))
print()
print('longModPowerBarrett: ' + blocks_to_number(LongModPowerBarrett(gg, ff, mm)))

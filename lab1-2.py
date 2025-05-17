import time
#беззнакові із довільною довжиною в форматі найменшої значущої цифри(little endian)
w = 32
base = 2 ** 32

def toTheSameLength(A, B):
    if len(A) < len(B):
        A = A + [0] * (len(B) - len(A))
    if len(A) > len(B):
        B = B + [0] * (len(A) - len(B)) 
    return A, B  

def deleteExtraZeros(A):
    while A and A[-1] == 0:
        A.pop() 
    if not A:  
        return [0]    
    return A

def longShiftDigitsToHigh(A, num):
    C = [0] * num + A
    return C

def bitLength(A):
    A = deleteExtraZeros(A) 
    bitlen = 32 * (len(A) - 1) + A[-1].bit_length()
    return bitlen

def longShiftBitsToHigh(num, shift):
    if shift == 0:
        return num
    zero_blocks = shift // w
    remainder = shift % w
    result = [0] * zero_blocks
    carry = 0
    for block in num:
        new_block = (block << remainder | carry) & (base - 1)
        carry = block >> (w - remainder)
        result.append(new_block)
    if carry != 0:
        result.append(carry)
    return deleteExtraZeros(result)

def hexTo2_32(hex_num):
    num_10 = int(hex_num, 16)
    num_2_32 = []
    while num_10 > 0:
        num_2_32.append(num_10 & (base - 1))
        num_10 = num_10 >> w
    if not num_2_32: 
        return [0]
    return num_2_32

def base2_32toHex(num_2_32):
    num_2_32 = deleteExtraZeros(num_2_32)
    num_10 = 0
    for i in range(len(num_2_32)-1, -1, -1):
        num_10 = (num_10 << w) + num_2_32[i]
    return hex(num_10)

def div2(A):
    if A == [0]:
        return [0]
    result = []
    carry = 0
    for i in reversed(range(len(A))):
        current = (carry << w) + A[i]
        result.append(current // 2)
        carry = current % 2
    result.reverse()
    return deleteExtraZeros(result)

def calculationU(N):
    k = len(N)
    b2k = [0] * 2 * k
    b2k.append(1)
    b2k = deleteExtraZeros(b2k)
    N = deleteExtraZeros(N)
    b2k, N = toTheSameLength(b2k, N)  
    u = longDivMod(b2k, N)[0]
    u = deleteExtraZeros(u)
    return u

def killLastDigits(X, k):
    X = deleteExtraZeros(X)
    n = len(X)
    if n < k:
        return [0]
    result = X[k:]
    return result

def longAdd(A, B):
    A, B = toTheSameLength(A, B)
    C = []
    carry = 0
    for i in range(len(A)):
        temp = A[i] + B[i] + carry
        C.append(temp & (base - 1))
        carry = temp >> w 
    if carry != 0:    
        C.append(carry)
    return deleteExtraZeros(C)

def longSub(A, B):
    A, B = toTheSameLength(A, B)
    C = []
    borrow = 0
    for i in range(len(A)):
        temp = A[i] - B[i] - borrow
        if temp >= 0:
            C.append(temp)
            borrow = 0
        else:
            C.append(base + temp)
            borrow = 1   
    if borrow == 1:
        raise Exception("Error")        
    return deleteExtraZeros(C) 
       
def longCmp(A, B):
    A, B = deleteExtraZeros(A), deleteExtraZeros(B)
    A, B = toTheSameLength(A, B)
    i = len(A) - 1
    while A[i] == B[i]:
        i = i-1
        if i == -1: 
            return 0
    else:
        if A[i] > B[i]:
            return 1
        else:
            return -1
        
def longMulOneDigit(A, b):
    n = len(A)
    C = [0] * (n + 1)
    carry = 0
    for i in range(n):
        temp = A[i] * b + carry
        C[i] = temp & (base - 1)
        carry = temp >> w
    C[n] = carry
    C = deleteExtraZeros(C)
    return C

def longMul(A, B):
    C = [0]
    for i in range(len(B)):
        temp = longMulOneDigit(A, B[i])
        temp = longShiftDigitsToHigh(temp, i)
        C = longAdd(C, temp)
    C = deleteExtraZeros(C)
    return C

def longDivMod(A, B):
    if longCmp(A, B) < 0:
        raise Exception("Error")
    k = bitLength(B)
    R = A
    Q = [0] * len(A)
    while longCmp(R, B) >= 0:
        t = bitLength(R)
        shift = t - k
        if shift < 0:
            break
        C = longShiftBitsToHigh(B, shift)
        if longCmp(R, C) < 0:
            shift -= 1
            if shift < 0:
                break
            C = longShiftBitsToHigh(B, shift)
            if longCmp(R, C) < 0:
                break
        R = longSub(R, C)
        h = shift // w
        s = shift % w
        Q, _ = toTheSameLength(Q, [0] * (h + 1))
        Q[h] = Q[h] | 1 << (s)
        Q = deleteExtraZeros(Q)
        R = deleteExtraZeros(R)
    return Q, R

def longPowerWindow(A, B):
    C = [1]
    for i in B:
        if i == 1:
            C = longMul(C, A)
        A = longMul(A, A)
    return C

def gcd(A, B):
    d = [1]
    while A[0] % 2 == 0 and B[0] % 2 == 0:
        A = div2(A)
        B = div2(B)
        d = longMulOneDigit(d, 2)
    while A[0] % 2 == 0:
        A = div2(A)
    while B != [0]:
        while B[0] % 2 == 0:
            B = div2(B)
        if longCmp(A, B) > 0:
            A, B = B, A
        B = longSub(B, A)
    return longMul(A, d)

def lcm(A, B):
    gcdAB = gcd(A, B)
    mulAB = longMul(A, B)
    gcdAB = deleteExtraZeros(gcdAB)
    mulAB = deleteExtraZeros(mulAB)
    gcdAB, mulAB = toTheSameLength(gcdAB, mulAB) 
    result = longDivMod(mulAB, gcdAB)[0]
    return result

def barrettReduction(X, N):
    X = deleteExtraZeros(X)
    N = deleteExtraZeros(N)
    if longCmp(X, N) < 0:
        return X
    k = len(N)
    u = calculationU(N)
    q = killLastDigits(X, k - 1) 
    q = longMul(q, u)
    q = killLastDigits(q, k + 1) 
    r = longSub(X, longMul(q, N))
    while longCmp(r, N) >= 0:
        r = longSub(r, N)
        r = deleteExtraZeros(r)    
    return r

def longModAddBarrett(a, b, n):
    a = barrettReduction(a, n)
    b = barrettReduction(b, n)
    sum = longAdd(a, b)
    return barrettReduction(sum, n)

def longModSubBarrett(a, b, n):
    if longCmp(a, b) < 0:
        a = longAdd(a, n)
    s = longSub(a, b)
    return barrettReduction(s, n)

def longModMulBarrett(a, b, n):
    a = barrettReduction(a, n)
    b = barrettReduction(b, n)
    s = longMul(a, b)
    return barrettReduction(s, n)

def longModSquarePowerBarrett(x, n):
    x = barrettReduction(x, n)
    s = longMul(x, x)
    return barrettReduction(s, n)

def longModPowerBarrett(A, B, N):
    B = words32_to_bit_array(B)
    C = [1]
    if longCmp(A, N) > 0:
        A = barrettReduction(A, N)
    for i in B:
        if i == 1:
            C = longModMulBarrett(C, A, N)
        A = longModSquarePowerBarrett(A, N)
    return C

def words32_to_bit_array(words):
    bit_array = []
    for word in words:
        bits = [(word >> i) & 1 for i in range(32)]
        bit_array.extend(bits)
    return bit_array


#k = 5
#c = 100
#g = '0x70307b356ca65d93e9aba1a011901a8f858da76cac9995519cc5287887fdfa8b114da61f5b3f7e0bf02a3a96d3d3711f6b8f3f7ee4387fcda20d52ddacc4cfa72cd98b6b7360d037a7c8325cc25e7450ed4eb4e7c3d75a567f982584a438028b20397fc3f0c66e6682559d669fb22d12ca72c82965701370ee6c9e556c897569'
#f = '0x37293d9cf232ebcbf2bfafed458903bbc8f02f9d3083bb5dc405cc0f659e833fa90d597bc79c4396fad89e16f655410de3c54caba4b2a96cf6555a05b5b6d93018b2636169522b048ebe7563e42ee2307700c87ab2935dab71431a70e34f96f46abba42cb7cf8ab6c97f1d636b2216641063c305291639a377dcc0e4af8f5e5d'
#m = '0x54519ca8fba424765f1b795e4ddbbc89e022c84ded4523d54a7fb881097305a196fc85b6f4f765a97d3ff30af17824a6d6dc2a91d181065df345ceb72144ea7d310563c5b72c155850617102b3e1179b942dfc05303e314c8649698c26102f4bab2b1444a08d215e60c561ff47bc14da6a5895bbdd3b473575afadbb15d962f5'
f = '0x80307b356ca65d93e9aba1a011901a8f858da76cac9995519cc5287887fdfa8b114da61f5b3f7e0bf02a3a96d3d3711f6b8f3f7ee4387fcda20d52ddacc4cfa72cd98b6b7360d037a7c8325cc25e7450ed4eb4e7c3d75a567f982584a438028b20397fc3f0c66e6682559d669fb22d12ca72c82965701370ee6c9e556c897569'
g = '0x47293d9cf232ebcbf2bfafed458903bbc8f02f9d3083bb5dc405cc0f659e833fa90d597bc79c4396fad89e16f655410de3c54caba4b2a96cf6555a05b5b6d93018b2636169522b048ebe7563e42ee2307700c87ab2935dab71431a70e34f96f46abba42cb7cf8ab6c97f1d636b2216641063c305291639a377dcc0e4af8f5e5d'
m = '0xa4519ca8fba424765f1b795e4ddbbc89e022c84ded4523d54a7fb881097305a196fc85b6f4f765a97d3ff30af17824a6d6dc2a91d181065df345ceb72144ea7d310563c5b72c155850617102b3e1179b942dfc05303e314c8649698c26102f4bab2b1444a08d215e60c561ff47bc14da6a5895bbdd3b473575afadbb15d962f5'
#d = '0x12341324152525252fff5454595506d03aa10718105e142814492ec01eff9facdd197ac451b624a5b7e35712d0caf3567b15944ed95099d3bc1c6b2e0da7c426250b7524cb1c96706250fc39d4a41664bea073695fb89e37d30c42c73e7ade345538c3e7279d33750f9fb1f94e6d53aafa0afa0c4d9c2e21a97e456ea82cc6a83fe6ffa5a5c99156990b9c1d605c105847b0c33d603f6fd8cc2a0deed7ca5eab92e838c10c930d4c2c04f7c8fab88d52c77391ddfdf25b8ac5a3f692331cc47d329b4e0100bf8b3f486f65c03b16af17efcbe53ab6b1eae18eaa185bcfb8f3e91321de981baa83efeaf753bbbc1865eb9dfbd4b67bf30af9c4e024f870e2523c'
#g = '0x72dbd34d03ad2be472af5faf19391c4a8'
#f = '0xd843387256f279383f067845aa'
#m = '0xc2289f575'
#d = '0xc3333905'
#ss =  [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#t =  [1, 0, 1]
gg = hexTo2_32(g)
ff = hexTo2_32(f)
mm = hexTo2_32(m)
#dd = hexTo2_32(d)
#cc = hexTo2_32(hex(c))
#print('longAdd: ' + base2_32toHex(longAdd(gg, ff)))
#print('longSub: ' + base2_32toHex(longSub(gg, ff)))
#print('longMul: ' + base2_32toHex(longMul(gg, ff)))
#print('longDivMod: ' + base2_32toHex(longDivMod(gg, ff)[0]))
#print('Остача від ділення longDivMod: ' + base2_32toHex(longDivMod(gg, ff)[1]))
#print('longPowerWindow: ' + base2_32toHex(longPowerWindow(gg, ff)))
print()
print('gcd: ' + base2_32toHex(gcd(gg, ff)))
print()
print('lcm: ' + base2_32toHex(lcm(gg, ff)))
print()
print('barrettReduction: ' + base2_32toHex(barrettReduction(gg, ff)))
print()
print('longModAddBarrett: ' + base2_32toHex(longModAddBarrett(gg, ff, mm)))
print()
print('longModSubBarrett: ' + base2_32toHex(longModSubBarrett(gg, ff, mm)))
print()
print('longModMulBarrett: ' + base2_32toHex(longModMulBarrett(gg, ff, mm)))
print()
print('longModSquarePowerBarrett: ' + base2_32toHex(longModSquarePowerBarrett(gg, mm)))
print()
print('longModPowerBarrett: ' + base2_32toHex(longModPowerBarrett(gg, ff, mm)))


'''gf = base2_32toHex(longAdd(gg, ff))
ggff = base2_32toHex(longSub(gg, ff))
gggfff = longCmp(gg, ff)
#gk = longMulOneDigit(gg, k)
ggggffff = base2_32toHex(longMul(gg, ff))
gggggfffff = base2_32toHex(longDivMod(gg, ff)[0])
gggggfffff2 = base2_32toHex(longDivMod(gg, ff)[1])
ggggggffffff = base2_32toHex(gcd(gg, ff))
gggggggfffffff = base2_32toHex(lcm(gg, ff))
print(gg)
print(ff)
print(gf)
print(ggff)
print(gggfff)
#print(gk)
print(ggggffff)
print(gggggfffff)
print(gggggfffff2)
print(ggggggffffff)
print(gggggggfffffff)
#print(base2_32toHex(ggggffff))
#print(barrettReduction(gg, ff))
print(base2_32toHex(longModAddBarrett(gg, ff, mm)))
print(base2_32toHex(longModSubBarrett(gg, ff, mm)))
print(base2_32toHex(longModMulBarrett(gg, ff, mm)))
print(base2_32toHex(longModSquarePowerBarrett(gg, mm)))
#print(base2_32toHex(longModPowerBarrett(gg, s, mm)))
#print(longPowerWindow(gg, t))'''
'''
sumGF = longAdd(gg, ff)
sumGFmulM = longMul(sumGF, mm)
mulMsumGF = longMul(mm, sumGF)
mulGM = longMul(gg, mm)
mulFM = longMul(ff, mm)
sumMulGMmulFM = longAdd(mulGM, mulFM)
if sumMulGMmulFM == mulMsumGF == sumGFmulM:
    print('Success')
else:
    print('Error')
mulOneDigitGC = longMulOneDigit(gg, c)
sumGGGG = [0]
for i in range(c):
    sumGGGG = longAdd(sumGGGG, gg)
if mulOneDigitGC == sumGGGG:
    print('Success')
else:
    print('Error')    
mSumGF = longModAddBarrett(gg, ff, mm)
mSumGFmulD = longModMulBarrett(mSumGF, dd, mm) 
mMulDSumGF = longModMulBarrett(dd, mSumGF, mm)
mMulGD = longModMulBarrett(gg, dd, mm)
mMulFD = longModMulBarrett(ff, dd, mm)
mSumMulGDMulFD = longModAddBarrett(mMulGD, mMulFD, mm)
if mSumGFmulD == mMulDSumGF == mSumMulGDMulFD:
    print('Success')
else:
    print('Error')
mMulGC = longModMulBarrett(gg, cc, mm)
sumGGGGG = [0]
for i in range(c):
    sumGGGGG = longModAddBarrett(sumGGGGG, gg, mm)
if mMulGC == sumGGGGG:
    print('Success')
else:
    print('Error')

if longCmp(gcd(ff, mm), [1]) == 0:
    phiN = longSub(mm, [1])
    result = longModPowerBarrett(ff, phiN, mm)
    if result == [1]:
        print("Success")
    else:
        print("Error")
else:
    print("Числа не є взаємно простими")



def timeSearch(f, *args, repeats=10):
    start = time.perf_counter()
    for _ in range(repeats):
        f(*args)
    end = time.perf_counter()
    avg_time = (end - start) / repeats
    return avg_time

avg = timeSearch(longAdd, gg, ff)
print(f"Середній час роботи longAdd: {avg:.10f} сек")
avg1 = timeSearch(longSub, gg, ff)
print(f"Середній час роботи longSub: {avg1:.10f} сек")
avg2 = timeSearch(longCmp, gg, ff)
print(f"Середній час роботи longCmp: {avg2:.10f} сек")
avg3 = timeSearch(longMulOneDigit, gg, k)
print(f"Середній час роботи longMulOneDigit: {avg3:.10f} сек")
avg4 = timeSearch(longMul, gg, ff)
print(f"Середній час роботи longMul: {avg4:.10f} сек")
avg5 = timeSearch(longDivMod, gg, ff)
print(f"Середній час роботи longDivMod: {avg5:.10f} сек")
avg6 = timeSearch(longPowerWindow, gg, t)
print(f"Середній час роботи longPowerWindow: {avg6:.10f} сек")
avg7 = timeSearch(gcd, gg, ff)
print(f"Середній час роботи gcd: {avg7:.10f} сек")
avg8 = timeSearch(lcm, gg, ff)
print(f"Середній час роботи lcm: {avg8:.10f} сек")
avg9 = timeSearch(longModAddBarrett, gg, ff, mm)
print(f"Середній час роботи longModAddBarrett: {avg9:.10f} сек")
avg10 = timeSearch(longModSubBarrett, gg, ff, mm)
print(f"Середній час роботи longModSubBarrett: {avg10:.10f} сек")
avg11 = timeSearch(longModMulBarrett, gg, ff, mm)
print(f"Середній час роботи longModMulBarrett: {avg11:.10f} сек")
avg12 = timeSearch(longModSquarePowerBarrett, gg, mm)
print(f"Середній час роботи longModSquarePowerBarrett: {avg12:.10f} сек")
avg13 = timeSearch(longModPowerBarrett, gg, s, ff)
print(f"Середній час роботи longModPowerBarrett: {avg13:.10f} сек")'''

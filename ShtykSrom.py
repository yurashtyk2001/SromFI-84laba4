def nadd(m, w):
    return m ^ w

def c_shift_l(m, n):
    if (n % 509 == 0):
        return m
    x = (m << n) & ((1 << 509) - 1)
    y = m >> (509 - n)
    return x | y

def c_shift_r(m, n):
    return c_shift_l(a, 509 - n)

def npow2(m):
    return c_shift_r(m, 1)

def trace(m):
    count = 0
    for i in range(m.bit_length()):
        count = count + m & 1
        m = m >> 1
    return count

def set_matrix():
    ret = []
    p = 1019
    indexes = [(1 << i) % p for i in range(509)]
    for i in range(509):
        s = 0
        for j in range(509):
            if ((indexes[i] + indexes[j]) % p == 1 or (indexes[i] - indexes[j]) % p == 1 or (-indexes[i] + indexes[j]) % p == 1 or (-indexes[i] - indexes[j]) % p == 1): 
                s = s | (1 << (509 - j - 1))
        ret.append(s)
    return ret

def nmul(m, w):
    L = set_matrix()
    ret = 0
    for i in range(509):
        u = c_shift_l(m, i)
        v = c_shift_l(w, i)
        s = 0
        for j in range(509):
            if v & (1 << (508 - j)):
                s = s ^ bin(u & L[j]).count('1') % 2
        if s != 0:
            ret = ret | (1 << (508 - i))
    return ret

def npown(m, w):
    ret = (1 << 509) - 1
    tmp = a
    for i in range(b.bit_length()):
        if b & (1 << i):
            ret = nmul(ret, tmp)
        tmp = npow2(tmp)
    return ret

def nrev(m):
    m = 508
    tmp = m
    count = 1
    t = m.bit_length() - 1
    for i in range(t - 1, -1, -1):
        tmp = nmul(c_shift_r(tmp, count), tmp)
        count = 2 * count
        if m & (1 << i):
            tmp = nmul(c_shift_r(tmp, 1), m)
            count = count + 1
    return c_shift_r(tmp, 1)

m = 0x13E33D8293AD74AC646A97CC7C8028E7DFADF30BAAF952A0F1242C36A1A07B8E0B622C2B1E8786B882011FDBED2F6B64D6060C8001D7B1FD2424DA2B27A2AA62
w = 0x04A27C9D3C497184839DF9BFC77646C792776E7A47A051B6E49720C698015A6E76C53C1BEA34EA83FC422B0D8D76ABC4A27809BBDA1C584168B6CFD85A02D9E9
n = 0x0A7F679D856C6F5380430BCCB82B2DB8DFC5254DC72F93FF67B07F13E82C6174F52C71861B72B1C467BF355DCC829C96356301490880C27595B1CC4FF90C82AE

print("\nA + B = ", hex(nadd(m, w)).upper()[2:])
print("A * B = ", hex(nmul(m, w)).upper()[2:])
print("Tr(A) = ", trace(m), "decimal")
print("A^2   = ", hex(npow2(m)).upper()[2:])
print("A^-1  = ", hex(nrev(m)).upper()[2:])
print("A^N   = ", hex(npown(m, n)).upper()[2:])


print(hex(nmul(n,nadd(m, w))) == hex(nadd(nmul(n, m), nmul(n, w))))
print(npown(trace(m), (npown(2, trace(m))-1)) ==1)
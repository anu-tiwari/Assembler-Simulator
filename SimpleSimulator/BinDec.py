def ToBinaryMem(decimal):
    # argument must be a decimal number in string datatype
    # returns the binary string of 8 bits (full of leading zeroes if required)
    # returns error if the number requires more than 8 bits or is negative
    decimal = int(decimal)
    if decimal>=256 or decimal<0:
        return 'overflow error'
    else:
        binary = ""
        n = int(decimal)
        while n != 0:
            binary += str(n % 2)
            n = n//2
        binary = binary[-1::-1]
        binary = binary.zfill(8)
        return binary

def ToBinary(decimal):
    # argument must be a decimal number in string datatype
    # returns the binary string of 16 bits (full of leading zeroes if required)
    # returns error if the number requires more than 16 bits or is negative
    decimal = int(decimal)
    if decimal>=65536 or decimal<0:
        return 'overflow error'
    else:
        binary = ""
        n = int(decimal)
        while n != 0:
            binary += str(n % 2)
            n = n//2
        binary = binary[-1::-1]
        binary = binary.zfill(16)
        return binary

def ToDecimal(binary):
    # argument must be a binary number in string datatype
    # returns the decimal value of the given binary string
    BIN = list(binary)
    BIN.reverse()
    decimal = 0
    for i in range(len(BIN)):
        if BIN[i] == '1':
            decimal += 2**i
        else:
            continue

    return decimal
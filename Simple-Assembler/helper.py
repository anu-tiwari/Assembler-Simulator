def tobinary(decimal):
    # argument must be a decimal number in string datatype
    # returns the binary string of 8 bits (full of leading zeroes if required) 
    # returns error if the number requires more than 8 bits or is negative
    decimal = int(decimal)
    if decimal>=256 or decimal<0:
        return 'overflow error'
    else:
        binary = ""

# QR Code Data Encoding Module: Handles string to binary data encoding conversion

from constant import char_cap, required_bytes, mindex, lindex, num_list, alphanum_list, grouping_list, mode_indicator
       
def encode(ver, ecl, str):
    """
    Encode a string
    ver: QR code version
    ecl: Error correction level
    str: String to encode
    return: Encoded string
    """
    # Four encoding modes: Numeric, Alphanumeric, Byte, Kanji 
    mode_encoding = {
            'numeric': numeric_encoding,           # Numeric encoding method
            'alphanumeric': alphanumeric_encoding, # Alphanumeric encoding method
            'byte': byte_encoding,                 # Byte encoding method
            'kanji': kanji_encoding                # Kanji encoding method
            }
          
    # Call analyse function to determine the most suitable encoding mode and version
    ver, mode = analyse(ver, ecl, str)
    print('line 16: mode:', mode)
    
    # Generate initial encoding (Mode Indicator + Character Count Indicator + Actual data encoding)
    code = mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding[mode](str)
    
    # Add terminator
    rqbits = 8 * required_bytes[ver-1][lindex[ecl]]  # Calculate required number of bits
    b = rqbits - len(code)
    code += '0000' if b >= 4 else '0' * b  # Add 4 zeros if space is sufficient, otherwise add maximum possible
    
    # Ensure encoding length is a multiple of 8 (byte alignment)
    while len(code) % 8 != 0:
        code += '0'
    
    # If the string is still too short, add padding bytes
    while len(code) < rqbits:    
        code += '1110110000010001' if rqbits - len(code) >= 16 else '11101100'
    
    # Convert binary string to byte array
    data_code = [code[i:i+8] for i in range(len(code)) if i%8 == 0]
    data_code = [int(i,2) for i in data_code]

    # Group data codewords according to version and error correction level
    g = grouping_list[ver-1][lindex[ecl]]
    data_codewords, i = [], 0
    for n in range(g[0]):
        data_codewords.append(data_code[i:i+g[1]])
        i += g[1]
    for n in range(g[2]):
        data_codewords.append(data_code[i:i+g[3]])
        i += g[3]
    
    return ver, data_codewords  # Return actual version used and data codewords
    
def analyse(ver, ecl, str):
    """
    Automatically determine the most suitable encoding mode
    ver: QR code version
    ecl: Error correction level
    str: String to encode
    return: Most suitable encoding mode
    """
    # Choose optimal encoding mode based on character content
    if all(i in num_list for i in str):
        mode = 'numeric'
    elif all(i in alphanum_list for i in str):
        mode = 'alphanumeric'
    else:
        mode = 'byte'
    
    # Determine the minimum version that can accommodate the current content
    m = mindex[mode]  # Get mode index
    l = len(str)      # String length
    for i in range(40):
        if char_cap[ecl][i][m] > l:  # Find the first version that can accommodate the current character count
            ver = i + 1 if i+1 > ver else ver  # Update if higher version is needed
            break
 
    return ver, mode

def numeric_encoding(str):
    """
    Numeric encoding
    str: String to encode
    return: Encoded string
    """
    str_list = [str[i:i+3] for i in range(0,len(str),3)]
    code = ''
    for i in str_list:
        rqbin_len = 10
        if len(i) == 1: 
            rqbin_len = 4
        elif len(i) == 2:
            rqbin_len = 7
        code_temp = bin(int(i))[2:]
        code += ('0'*(rqbin_len - len(code_temp)) + code_temp)
    return code
    
def alphanumeric_encoding(str):
    """
    Alphanumeric encoding
    str: String to encode
    return: Encoded string
    """
    code_list = [alphanum_list.index(i) for i in str]
    code = ''
    for i in range(1, len(code_list), 2):
        c = bin(code_list[i-1] * 45 + code_list[i])[2:]
        c = '0'*(11-len(c)) + c
        code += c
    if i != len(code_list) - 1:
        c = bin(code_list[-1])[2:]
        c = '0'*(6-len(c)) + c
        code += c
    
    return code
    
def byte_encoding(str):
    """
    Byte encoding
    str: String to encode
    return: Encoded string
    """
    code = ''
    for i in str:
        c = bin(ord(i.encode('iso-8859-1')))[2:]
        c = '0'*(8-len(c)) + c
        code += c
    return code
    
def kanji_encoding(str):
    """
    Kanji encoding
    str: String to encode
    return: Encoded string
    """
    pass
    
def get_cci(ver, mode, str):
    """
    Get Character Count Indicator
    ver: QR code version
    mode: Encoding mode
    str: String to encode
    return: Character Count Indicator
    """
    # Determine the bit length of the Character Count Indicator based on version range and encoding mode
    if 1 <= ver <= 9:
        cci_len = (10, 9, 8, 8)[mindex[mode]]  # Corresponding to Numeric, Alphanumeric, Byte, Kanji modes
    elif 10 <= ver <= 26:
        cci_len = (12, 11, 16, 10)[mindex[mode]]
    else:
        cci_len = (14, 13, 16, 12)[mindex[mode]]
        
    # Convert character count to binary, ensuring length meets requirements
    cci = bin(len(str))[2:]
    cci = '0' * (cci_len - len(cci)) + cci
    return cci

# Code for testing
if __name__ == '__main__':
    s = '123456789'
    v, datacode = encode(1, 'H', s)
    print(v, datacode)
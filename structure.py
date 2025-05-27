# QR Code Structure Module: Handles interleaving of data codewords and error correction codewords, generating the final binary bit stream

from constant import required_remainder_bits, lindex, grouping_list

def structure_final_bits(ver, ecl, data_codewords, ecc):
    """
    Generate the final binary data stream for QR code
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    data_codewords: List of data codewords
    ecc: List of error correction codewords
    return: Final binary bit stream string
    """
    final_message = interleave_dc(ver, ecl, data_codewords) + interleave_ecc(ecc)
    
    # Convert to binary and add remainder bits
    final_bits = ''.join(['0'*(8-len(i))+i for i in [bin(i)[2:] for i in final_message]]) + '0' * required_remainder_bits[ver-1]
    
    return final_bits

def interleave_dc(ver, ecl, data_codewords):
    """
    Interleave data codewords
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    data_codewords: Data codewords
    return: Interleaved data codewords
    """
    id = []
    for t in zip(*data_codewords):
        id += list(t)
    g = grouping_list[ver-1][lindex[ecl]]
    if g[3]:
        for i in range(g[2]):
            id.append(data_codewords[i-g[2]][-1])
    return id
    
def interleave_ecc(ecc):
    """
    Interleave error correction codewords
    ecc: Error correction codewords
    return: Interleaved error correction codewords
    """
    ie = []
    for t in zip(*ecc):
        ie += list(t)
    return ie